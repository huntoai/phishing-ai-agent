"""LinkedIn enrichment source."""
import os
import requests
from typing import Dict, Any
from core.logger import Logger
from integrations.enrichment_base import EnrichmentSource

try:
    from linkedin_api import Linkedin
    LINKEDIN_LIBRARY_AVAILABLE = True
except ImportError:
    LINKEDIN_LIBRARY_AVAILABLE = False


class LinkedInEnrichment(EnrichmentSource):
    """LinkedIn profile enrichment with proper library support."""
    
    def __init__(self):
        self.logger = Logger.get_logger("LinkedInEnrichment")
        
        # LinkedIn credentials (optional - for authenticated scraping)
        self.email = os.environ.get("LINKEDIN_EMAIL")
        self.password = os.environ.get("LINKEDIN_PASSWORD")
        
        self.client = None
        if LINKEDIN_LIBRARY_AVAILABLE and self.email and self.password:
            try:
                self.client = Linkedin(self.email, self.password)
                self.logger.info("LinkedIn API client initialized (authenticated)")
            except Exception as e:
                self.logger.warning(f"LinkedIn authentication failed: {str(e)}")
        elif not LINKEDIN_LIBRARY_AVAILABLE:
            self.logger.info("linkedin-api not installed - using basic profile checking")
        else:
            self.logger.info("LinkedIn credentials not provided - using basic profile checking")
    
    def get_source_name(self) -> str:
        return "LinkedIn"
    
    def is_available(self) -> bool:
        """LinkedIn enrichment available even without auth (basic checking)."""
        return True
    
    def enrich_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich employee data from LinkedIn with multiple strategies."""
        
        linkedin_url = employee_data.get('linkedin_url', '')
        name = f"{employee_data.get('first_name', '')} {employee_data.get('last_name', '')}".strip()
        company = employee_data.get('company_name', '')
        
        enrichment_data = {
            "linkedin_url": linkedin_url,
            "profile_accessible": False,
            "enrichment_method": "none"
        }
        
        # Strategy 1: Use authenticated linkedin-api for full profile scraping
        if self.client and linkedin_url:
            try:
                # Extract LinkedIn username from URL
                username = self._extract_linkedin_username(linkedin_url)
                if username:
                    self.logger.info(f"Fetching LinkedIn profile for: {username}")
                    profile = self.client.get_profile(username)
                    
                    if profile:
                        enrichment_data.update({
                            "profile_accessible": True,
                            "enrichment_method": "authenticated_api",
                            "headline": profile.get('headline'),
                            "summary": profile.get('summary'),
                            "location": profile.get('locationName'),
                            "industry": profile.get('industryName'),
                            "experience": self._parse_experience(profile.get('experience', [])),
                            "education": self._parse_education(profile.get('education', [])),
                            "skills": profile.get('skills', [])[:10],  # Top 10 skills
                            "connections": profile.get('connections'),
                            "profile_picture": profile.get('displayPictureUrl')
                        })
                        self.logger.info(f"Successfully enriched profile via API")
                        return enrichment_data
            except Exception as e:
                self.logger.error(f"LinkedIn API enrichment failed: {str(e)}")
        
        # Strategy 2: Basic profile URL accessibility check
        if linkedin_url:
            try:
                self.logger.info(f"Checking LinkedIn profile accessibility: {linkedin_url}")
                response = requests.head(linkedin_url, timeout=5, allow_redirects=True)
                
                enrichment_data.update({
                    "profile_accessible": response.status_code == 200,
                    "status_code": response.status_code,
                    "enrichment_method": "basic_check"
                })
                
                if response.status_code == 200:
                    self.logger.info("LinkedIn profile is publicly accessible")
                else:
                    self.logger.warning(f"LinkedIn profile returned status {response.status_code}")
                    
            except Exception as e:
                self.logger.error(f"LinkedIn URL check failed: {str(e)}")
                enrichment_data["error"] = str(e)
        else:
            enrichment_data["note"] = "No LinkedIn URL provided"
        
        return enrichment_data
    
    def _extract_linkedin_username(self, url: str) -> str:
        """Extract LinkedIn username from profile URL."""
        if not url:
            return ""
        
        # Handle different LinkedIn URL formats
        # https://www.linkedin.com/in/username/
        # https://linkedin.com/in/username
        # linkedin.com/in/username/
        
        try:
            if '/in/' in url:
                username = url.split('/in/')[-1].strip('/').split('?')[0].split('/')[0]
                return username
        except Exception:
            pass
        
        return ""
    
    def _parse_experience(self, experience_list: list) -> list:
        """Parse experience data to extract key information."""
        parsed = []
        for exp in experience_list[:5]:  # Top 5 positions
            parsed.append({
                "title": exp.get('title'),
                "company": exp.get('companyName'),
                "duration": f"{exp.get('timePeriod', {}).get('startDate', {})} - {exp.get('timePeriod', {}).get('endDate', 'Present')}",
                "location": exp.get('locationName'),
                "description": exp.get('description', '')[:200]  # First 200 chars
            })
        return parsed
    
    def _parse_education(self, education_list: list) -> list:
        """Parse education data to extract key information."""
        parsed = []
        for edu in education_list[:3]:  # Top 3 schools
            parsed.append({
                "school": edu.get('schoolName'),
                "degree": edu.get('degreeName'),
                "field": edu.get('fieldOfStudy'),
                "years": f"{edu.get('timePeriod', {}).get('startDate', {})} - {edu.get('timePeriod', {}).get('endDate', {})}"
            })
        return parsed


