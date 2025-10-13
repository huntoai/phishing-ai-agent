from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

from integrations.base import DataSource
from integrations.apollo_tool import ApolloAPI
from integrations.enrichment_base import EnrichmentSource
from integrations.brave_search import BraveSearchEnrichment
from integrations.linkedin_enrichment import LinkedInEnrichment
from core.database import DatabaseAdapter
from core.logger import Logger
from core.models import Organization, Employee
from agent import EnrichmentAgent, ContentGenerator, EmailSender

load_dotenv()


class PhishingWorkflow:
    """Modular workflow orchestrator with independent methods."""
    
    def __init__(self, data_source: Optional[DataSource] = None, enrichment_sources: Optional[List[EnrichmentSource]] = None):
        self.logger = Logger.get_logger("PhishingWorkflow")
        self.db = DatabaseAdapter()
        self.data_source = data_source or ApolloAPI()
        self.enricher = EnrichmentAgent()
        self.generator = ContentGenerator()
        self.sender = EmailSender()
        
        # Initialize enrichment sources
        if enrichment_sources:
            self.enrichment_sources = enrichment_sources
        else:
            self.enrichment_sources = []
            # Add available enrichment sources
            brave = BraveSearchEnrichment()
            if brave.is_available():
                self.enrichment_sources.append(brave)
            linkedin = LinkedInEnrichment()
            if linkedin.is_available():
                self.enrichment_sources.append(linkedin)
        
        self.logger.info(f"Using data source: {self.data_source.get_name()}")
        if self.enrichment_sources:
            source_names = [s.get_source_name() for s in self.enrichment_sources]
            self.logger.info(f"Enrichment sources: {', '.join(source_names)}")
    
    def enrich_organization(self, domain: str, force_refresh: bool = False) -> Organization:
        """Enrich organization data (with caching)."""
        self.logger.info(f"[ORG ENRICH] Checking organization cache for {domain}")
        org = self.db.get_organization_by_domain(domain)
        
        if org and not force_refresh:
            self.logger.info(f"[ORG ENRICH] Using cached data for {org.name} ({domain})")
            return org
        
        self.logger.info(f"[ORG ENRICH] Fetching organization data from {self.data_source.get_name()}")
        org_data = self.data_source.enrich_organization(domain)
        
        if org_data.get('organization'):
            org_info = org_data['organization']
            org = self.db.add_organization(
                domain=domain,
                name=org_info.get('name'),
                industry=org_info.get('industry'),
                employee_count=org_info.get('estimated_num_employees'),
                city=org_info.get('city'),
                state=org_info.get('state'),
                country=org_info.get('country'),
                raw_data=org_info
            )
            return org
        
        return None
    
    def gather_employees(self, domain: str, max_employees: int = 10) -> List[Employee]:
        """Gather employees from data source and save to database."""
        self.logger.info(f"[GATHER] Searching employees at {domain}")
        response = self.data_source.search_people(domain, per_page=max_employees)
        people = response.get('people', [])
        
        if not people:
            self.logger.error(f"No employees found for {domain}")
            return []
        
        self.logger.info(f"[GATHER] Found {len(people)} employees")
        employees = []
        
        for person in people:
            email = person.get('email')
            first_name = person.get('first_name', '')
            last_name = person.get('last_name', '')
            
            if not email:
                continue
            
            # Generate proper email if locked
            if email == "email_not_unlocked@domain.com" and first_name and last_name:
                email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
                self.logger.info(f"Generated email pattern: {email}")
            
            # Save to database
            employee = self.db.add_employee(
                email=email,
                first_name=first_name,
                last_name=last_name,
                title=person.get('title'),
                city=person.get('city'),
                state=person.get('state'),
                country=person.get('country'),
                linkedin_url=person.get('linkedin_url')
            )
            employees.append(employee)
        
        return employees
    
    def enrich_employee(self, employee: Employee, organization: Organization) -> Employee:
        """
        Enrich employee data with vulnerability analysis using multiple sources.
        Pass complete employee and organization data to AI for dynamic analysis.
        """
        employee_name = f"{employee.first_name} {employee.last_name}".strip()
        self.logger.info(f"Enriching employee: {employee_name}")
        
        # Get current date for temporal context
        current_date = datetime.now().strftime("%Y-%m-%d %B")
        
        # Build complete employee data (ALL fields)
        employee_data = {
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "name": employee_name,
            "email": employee.email,
            "title": employee.title,
            "seniority": employee.seniority if hasattr(employee, 'seniority') else None,
            "departments": employee.departments if hasattr(employee, 'departments') else None,
            "city": employee.city,
            "state": employee.state,
            "country": employee.country,
            "linkedin_url": employee.linkedin_url,
            "company_name": organization.name if organization else None
        }
        
        # Build complete organization context (ALL fields)
        org_context = {
            "name": organization.name,
            "domain": organization.domain,
            "industry": organization.industry,
            "employee_count": organization.employee_count,
            "city": organization.city,
            "state": organization.state,
            "country": organization.country,
            "raw_data": organization.raw_data
        } if organization else {}
        
        # Collect enrichment from multiple sources
        raw_data = {}
        sources_used = []
        
        for enrichment_source in self.enrichment_sources:
            try:
                source_name = enrichment_source.get_source_name()
                self.logger.info(f"Calling enrichment source: {source_name}")
                
                source_data = enrichment_source.enrich_employee(employee_data)
                if source_data:
                    raw_data[source_name] = source_data
                    sources_used.append(source_name)
                    self.logger.info(f"Got data from {source_name}")
            except Exception as e:
                self.logger.error(f"Error in enrichment source {enrichment_source.get_source_name()}: {str(e)}")
        
        # Call enrichment agent with current date
        enrichment_result = self.enricher.enrich(employee_data, org_context, current_date)
        
        # Merge all enrichment data
        complete_enrichment = {
            "vulnerability_analysis": enrichment_result,
            "external_sources": raw_data,
            "enrichment_date": current_date
        }
        
        # Get the employee in our session (to avoid cross-session issues)
        local_employee = self.db.get_employee_by_email(employee.email)
        
        # Update employee with all enrichment data
        local_employee.vulnerability_score = enrichment_result.get("vulnerability_score", 0.0)
        local_employee.risk_level = enrichment_result.get("risk_level", "unknown")
        local_employee.enrichment_data = complete_enrichment
        local_employee.enrichment_sources = sources_used
        local_employee.raw_data = raw_data
        local_employee.last_enriched = datetime.utcnow()
        
        self.db.session.commit()
        self.logger.info(f"Employee enriched - Risk Level: {local_employee.risk_level}, Score: {local_employee.vulnerability_score}, Sources: {', '.join(sources_used)}")
        
        return local_employee
    
    def generate_content(self, email: str, organization: Optional[Organization] = None) -> Dict[str, Any]:
        """Generate phishing content - pass complete data to AI for dynamic content generation."""
        self.logger.info(f"[GENERATE] Creating attack for {email}")
        
        employee = self.db.get_employee_by_email(email)
        if not employee:
            self.logger.error(f"Employee {email} not found")
            return {}
        
        if not employee.enrichment_data:
            self.logger.error(f"Employee {email} not enriched")
            return {}
        
        # Get current date for timely/trending context
        current_date = datetime.now().strftime("%Y-%m-%d %B")
        
        # Build COMPLETE employee dict (all available data)
        employee_name = f"{employee.first_name} {employee.last_name}".strip()
        employee_dict = {
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'name': employee_name,
            'email': employee.email,
            'title': employee.title,
            'city': employee.city,
            'state': employee.state,
            'country': employee.country,
            'linkedin_url': employee.linkedin_url,
            'vulnerability_score': employee.vulnerability_score,
            'risk_level': employee.risk_level
        }
        
        # Get COMPLETE enrichment data (all sources, all analysis)
        enrichment_dict = employee.enrichment_data
        
        # Build COMPLETE org dict (all available data)
        org_dict = None
        if organization:
            org_dict = {
                'name': organization.name,
                'domain': organization.domain,
                'industry': organization.industry,
                'employee_count': organization.employee_count,
                'city': organization.city,
                'state': organization.state,
                'country': organization.country,
                'raw_data': organization.raw_data
            }
        
        # Generate content with current date - AI has full context

        content = self.generator.generate(employee_dict, enrichment_dict, org_dict, current_date)
        
        # Build generation context
        generation_context = {
            'date': current_date,
            'enrichment_sources': employee.enrichment_sources or [],
            'risk_level': employee.risk_level,
            'vulnerability_score': employee.vulnerability_score
        }
        
        # Save attack simulation
        self.db.add_attack_simulation(
            employee_email=email,
            attack_type="AI-Generated",
            subject_line=content.get('subject'),
            message_body=content.get('body'),
            sender_persona=content.get('sender'),
            attack_vector=content.get('attack_vector', 'Automated Campaign'),
            personalization_factors=["AI-Generated"],
            psychological_triggers=content.get('psychological_triggers', []),
            created_by="PhishingWorkflow",
            was_executed=False,
            generation_context=generation_context,
            content_metadata={
                'pretext': content.get('pretext'),
                'psychological_triggers': enrichment_dict.get('psychological_triggers', []),
                'recommended_vectors': enrichment_dict.get('recommended_vectors', [])
            }
        )
        
        return content
    
    def send_email(self, email: str, attack_id: Optional[int] = None) -> bool:
        """Send phishing email to employee."""
        self.logger.info(f"[SEND] Delivering to {email}")
        
        # Get latest attack for this employee
        from core.models import AttackSimulation
        if attack_id:
            attack = self.db.session.query(AttackSimulation).filter_by(id=attack_id).first()
        else:
            employee = self.db.get_employee_by_email(email)
            if not employee or not employee.attack_simulations:
                self.logger.error(f"No attacks found for {email}")
                return False
            attack = employee.attack_simulations[-1]
        
        if not attack:
            self.logger.error(f"Attack not found")
            return False
        
        # Send email
        result = self.sender.send(
            email,
            attack.subject_line,
            attack.message_body,
            attack.sender_persona
        )
        
        # Mark as executed
        if result:
            attack.was_executed = True
            self.db.session.commit()
        
        return result
    
    def run(self, domain: str, max_employees: int = 10, send_emails: bool = False):
        """Execute complete workflow: Org Enrich -> Gather -> Enrich -> Generate -> Send"""
        
        # Step 0: Enrich organization
        org = self.enrich_organization(domain)
        
        # Step 1: Gather employees
        employees = self.gather_employees(domain, max_employees)
        
        if not employees:
            return
        
        # Steps 2-4: Process each employee
        for employee in employees:
            # Enrich
            self.enrich_employee(employee, org)
            
            # Generate content
            self.generate_content(employee.email, org)
            
            # Send (if enabled)
            if send_emails:
                self.send_email(employee.email)
            
            self.logger.info(f"✓ Completed workflow for {employee.email}")
        
        self.logger.info(f"[COMPLETE] Processed {len(employees)} employees")


if __name__ == "__main__":
    workflow = PhishingWorkflow()
    workflow.run("tikaj.com", max_employees=2, send_emails=False)
