"""Apollo.io API integration using OpenAPI path-based requests."""
import os
import requests
from typing import Dict, List, Any, Optional
from core.logger import Logger
from integrations.base import DataSource


class ApolloAPI(DataSource):
    """Apollo.io API client using direct HTTP requests."""
    
    BASE_URL = "https://api.apollo.io/v1"
    
    def __init__(self):
        self.logger = Logger.get_logger("ApolloAPI")
        self.api_key = os.environ.get("APOLLO_API_KEY")
        if not self.api_key:
            raise ValueError("APOLLO_API_KEY not set")
        self.headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": self.api_key
        }
    
    def get_name(self) -> str:
        return "Apollo.io"
    
    def enrich_organization(self, domain: str) -> Dict[str, Any]:
        """Enrich organization data using Apollo API."""
        url = f"{self.BASE_URL}/organizations/enrich"
        
        payload = {"domain": domain}
        
        try:
            self.logger.info(f"Enriching organization: {domain}")
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            org = data.get("organization", {})
            self.logger.info(f"Organization enriched: {org.get('name', 'Unknown')}")
            return data
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Apollo API error (org enrichment): {str(e)}")
            return {"error": str(e), "organization": {}}
    
    def search_people(self, domain: str, per_page: int = 10) -> Dict[str, Any]:
        """Search people by organization domain using Apollo API."""
        url = f"{self.BASE_URL}/mixed_people/search"
        
        payload = {
            "q_organization_domains": domain,
            "page": 1,
            "per_page": per_page
        }
        
        try:
            self.logger.info(f"Searching people for domain: {domain}")
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            people_count = len(data.get("people", []))
            self.logger.info(f"Found {people_count} people")
            return data
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Apollo API error (people search): {str(e)}")
            return {"error": str(e), "people": []}
