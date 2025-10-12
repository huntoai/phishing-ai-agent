"""Brave Search API enrichment source."""
import os
import requests
from typing import Dict, Any
from core.logger import Logger
from integrations.enrichment_base import EnrichmentSource


class BraveSearchEnrichment(EnrichmentSource):
    """Brave Search API for employee enrichment (direct API implementation)."""
    
    def __init__(self):
        self.logger = Logger.get_logger("BraveSearchEnrichment")
        self.api_key = os.environ.get("BRAVE_API_KEY")
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        
        if self.api_key:
            self.logger.info("Brave Search API configured (using direct API calls)")
        else:
            self.logger.info("Brave Search API not configured - set BRAVE_API_KEY env var")
    
    def get_source_name(self) -> str:
        return "Brave Search"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def enrich_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Search for employee information using Brave Search with multiple strategies."""
        if not self.is_available():
            self.logger.warning("Brave API key not configured")
            return {"error": "API key not configured"}
        
        name = f"{employee_data.get('first_name', '')} {employee_data.get('last_name', '')}".strip()
        company = employee_data.get('company_name', '')
        title = employee_data.get('title', '')
        linkedin_url = employee_data.get('linkedin_url', '')
        
        # Build multiple search strategies
        search_queries = []
        
        # Strategy 1: LinkedIn profile search
        if linkedin_url:
            search_queries.append(f'"{name}" site:linkedin.com/in')
        elif company:
            search_queries.append(f'"{name}" "{company}" site:linkedin.com/in')
        
        # Strategy 2: Professional profile with title
        if title and company:
            search_queries.append(f'"{name}" "{title}" "{company}" profile')
        
        # Strategy 3: General professional search
        if company:
            search_queries.append(f'"{name}" "{company}" professional background')
        
        # Strategy 4: Social media presence
        search_queries.append(f'"{name}" twitter OR github OR blog')
        
        all_results = []
        
        try:
            # Execute top 2 searches to avoid rate limits
            for query in search_queries[:2]:
                self.logger.info(f"Searching: {query}")
                
                # Direct API call
                headers = {
                    "Accept": "application/json",
                    "X-Subscription-Token": self.api_key
                }
                params = {"q": query, "count": 3}
                
                response = requests.get(self.base_url, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                results = data.get("web", {}).get("results", [])
                for result in results[:3]:
                    all_results.append({
                        "title": result.get("title"),
                        "description": result.get("description"),
                        "url": result.get("url"),
                        "query": query
                    })
            
            self.logger.info(f"Found {len(all_results)} total results across {len(search_queries[:2])} searches")
            
            return {
                "search_queries": search_queries[:2],
                "results_count": len(all_results),
                "search_results": all_results,
                "linkedin_found": any("linkedin.com" in r.get("url", "") for r in all_results),
                "social_media_found": any(
                    any(platform in r.get("url", "") for platform in ["twitter.com", "github.com", "medium.com"])
                    for r in all_results
                )
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Brave Search API error: {str(e)}")
            return {"error": str(e), "search_queries": search_queries[:2]}


