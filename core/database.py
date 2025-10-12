from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.logger import Logger
from core.models import Base, Organization, Employee, AttackSimulation
from typing import Optional, List, Dict, Any
from datetime import datetime


class DatabaseAdapter:
    """Database adapter."""
    
    def __init__(self, db_url: str = "sqlite:///phishing_agent.db"):
        self.logger = Logger.get_logger("DatabaseAdapter")
        self.engine = create_engine(db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.logger.info(f"Database connected: {db_url}")
        
        Base.metadata.create_all(self.engine)
        self.logger.info("Database tables created")

    def get_session(self) -> Session:
        return self.Session()
    
    def add_organization(self, domain: str, name: Optional[str] = None,
                        industry: Optional[str] = None, employee_count: Optional[int] = None,
                        city: Optional[str] = None, state: Optional[str] = None,
                        country: Optional[str] = None, raw_data: Optional[Dict[str, Any]] = None) -> Organization:
        """Add or update organization."""
        org = self.session.query(Organization).filter_by(domain=domain).first()
        
        if org:
            if name:
                org.name = name
            if industry:
                org.industry = industry
            if employee_count:
                org.employee_count = employee_count
            if city:
                org.city = city
            if state:
                org.state = state
            if country:
                org.country = country
            if raw_data:
                org.raw_data = raw_data
            org.updated_at = datetime.utcnow()
        else:
            org = Organization(
                domain=domain,
                name=name,
                industry=industry,
                employee_count=employee_count,
                city=city,
                state=state,
                country=country,
                raw_data=raw_data
            )
            self.session.add(org)
        
        self.session.commit()
        self.session.refresh(org)
        self.logger.info(f"Organization saved: {domain}")
        return org
    
    def get_organization_by_domain(self, domain: str) -> Optional[Organization]:
        return self.session.query(Organization).filter_by(domain=domain).first()
    
    def add_employee(self, email: str, first_name: Optional[str] = None,
                    last_name: Optional[str] = None, title: Optional[str] = None,
                    linkedin_url: Optional[str] = None, **kwargs) -> Employee:
        """Add or update employee."""
        employee = self.session.query(Employee).filter_by(email=email).first()
        
        if employee:
            if first_name:
                employee.first_name = first_name
            if last_name:
                employee.last_name = last_name
            if title:
                employee.title = title
            if linkedin_url:
                employee.linkedin_url = linkedin_url
            
            for key, value in kwargs.items():
                if hasattr(employee, key) and value is not None:
                    setattr(employee, key, value)
        else:
            employee = Employee(
                email=email,
                first_name=first_name,
                last_name=last_name,
                title=title,
                linkedin_url=linkedin_url,
                **{k: v for k, v in kwargs.items() if hasattr(Employee, k)}
            )
            self.session.add(employee)
        
        self.session.commit()
        self.session.refresh(employee)
        self.logger.info(f"Employee saved: {email}")
        return employee
    
    def get_employee_by_email(self, email: str) -> Optional[Employee]:
        return self.session.query(Employee).filter_by(email=email).first()
    
    def add_attack_simulation(self, employee_email: str, attack_type: str,
                             subject_line: str, message_body: str,
                             sender_persona: str, attack_vector: str,
                             personalization_factors: List,
                             psychological_triggers: List,
                             created_by: str, was_executed: bool = False,
                             generation_context: Optional[Dict] = None,
                             content_metadata: Optional[Dict] = None):
        """Add attack simulation with generation context."""
        employee = self.get_employee_by_email(employee_email)
        if not employee:
            return
        
        simulation = AttackSimulation(
            employee_id=employee.id,
            attack_type=attack_type,
            attack_vector=attack_vector,
            subject_line=subject_line,
            message_body=message_body,
            sender_persona=sender_persona,
            personalization_factors=personalization_factors,
            psychological_triggers=psychological_triggers,
            created_by=created_by,
            was_executed=was_executed,
            generation_context=generation_context,
            content_metadata=content_metadata
        )
        
        self.session.add(simulation)
        self.session.commit()
        self.logger.info(f"Attack simulation saved for: {employee_email}")
        return simulation
