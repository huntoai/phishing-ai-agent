"""
Knowledge base tools for fetching real-time intelligence data.
These tools provide dynamic context for the enrichment agent.
"""
import os
import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from core.logger import Logger


class PhishingTrendsFetcher:
    """Fetch latest phishing attack trends and techniques."""
    
    def __init__(self):
        self.logger = Logger.get_logger("PhishingTrendsFetcher")
        self.brave_api_key = os.getenv("BRAVE_API_KEY")
        self.cache = {}
        self.cache_duration = timedelta(hours=24)
    
    def get_latest_trends(self, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Fetch latest phishing trends from security research sources.
        Uses web search to get current phishing attack methods.
        """
        if year is None:
            year = datetime.now().year
        
        cache_key = f"trends_{year}"
        
        # Check cache
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                self.logger.info(f"Using cached phishing trends for {year}")
                return cached_data
        
        self.logger.info(f"Fetching latest phishing trends for {year}")
        
        # If Brave API is available, use it
        if self.brave_api_key:
            return self._fetch_from_brave(year)
        else:
            # Fallback to hardcoded recent trends
            self.logger.warning("No Brave API key - using fallback trends data")
            return self._get_fallback_trends()
    
    def _fetch_from_brave(self, year: int) -> List[Dict[str, Any]]:
        """Fetch trends using Brave Search API."""
        try:
            query = f"phishing attack trends {year} techniques methods"
            url = "https://api.search.brave.com/res/v1/web/search"
            
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": self.brave_api_key
            }
            
            params = {
                "q": query,
                "count": 10,
                "freshness": "pm"  # Past month
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            trends = []
            
            # Extract trends from search results
            for result in data.get("web", {}).get("results", [])[:5]:
                trends.append({
                    "title": result.get("title"),
                    "description": result.get("description"),
                    "source": result.get("url"),
                    "year": year
                })
            
            # Cache the results
            self.cache[f"trends_{year}"] = (trends, datetime.now())
            
            self.logger.info(f"Fetched {len(trends)} phishing trends from Brave Search")
            return trends
            
        except Exception as e:
            self.logger.error(f"Error fetching trends from Brave: {str(e)}")
            return self._get_fallback_trends()
    
    def _get_fallback_trends(self) -> List[Dict[str, Any]]:
        """Fallback to static trends if API unavailable."""
        return [
            {
                "technique": "QR Code Phishing (Quishing)",
                "description": "Malicious QR codes in emails and physical mail that bypass email security filters",
                "prevalence": "high",
                "year": 2024
            },
            {
                "technique": "AI-Generated Deepfakes",
                "description": "Voice and video deepfakes impersonating executives and colleagues",
                "prevalence": "high",
                "year": 2024
            },
            {
                "technique": "Microsoft Teams/Slack Phishing",
                "description": "Impersonation attacks through collaboration platforms",
                "prevalence": "high",
                "year": 2024
            },
            {
                "technique": "Supply Chain Compromise",
                "description": "Vendor and partner impersonation for credential theft",
                "prevalence": "medium",
                "year": 2024
            },
            {
                "technique": "MFA Bypass Techniques",
                "description": "Advanced methods to bypass multi-factor authentication",
                "prevalence": "medium",
                "year": 2024
            },
            {
                "technique": "Remote Work Tool Exploitation",
                "description": "Targeting VPN, RDP, and remote collaboration tools",
                "prevalence": "high",
                "year": 2024
            }
        ]


class RegionalIntelligenceFetcher:
    """Fetch regional information for location-specific phishing."""
    
    def __init__(self):
        self.logger = Logger.get_logger("RegionalIntelligenceFetcher")
        self.brave_api_key = os.getenv("BRAVE_API_KEY")
        self.cache = {}
        self.cache_duration = timedelta(days=30)
    
    def get_regional_context(self, city: Optional[str] = None, 
                            state: Optional[str] = None, 
                            country: Optional[str] = None) -> Dict[str, Any]:
        """
        Get regional context including holidays, culture, local brands, events.
        """
        location = f"{city or ''}, {state or ''}, {country or ''}".strip(", ")
        cache_key = f"region_{location}"
        
        # Check cache
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                self.logger.info(f"Using cached regional data for {location}")
                return cached_data
        
        self.logger.info(f"Fetching regional intelligence for {location}")
        
        context = {
            "location": location,
            "holidays": self._get_holidays(country, city),
            "local_brands": self._get_local_brands(city, state, country),
            "cultural_notes": self._get_cultural_notes(country),
            "timezone": self._get_timezone(city, country),
            "business_practices": self._get_business_practices(country)
        }
        
        # Cache the results
        self.cache[cache_key] = (context, datetime.now())
        
        return context
    
    def _get_holidays(self, country: Optional[str], city: Optional[str]) -> List[Dict[str, str]]:
        """Get holidays for the region."""
        if self.brave_api_key and country:
            try:
                query = f"{country} holidays {datetime.now().year} calendar"
                return self._search_brave(query, max_results=3)
            except Exception as e:
                self.logger.error(f"Error fetching holidays: {str(e)}")
        
        # Fallback
        return [{"note": "Use web search to find current holidays and cultural events"}]
    
    def _get_local_brands(self, city: Optional[str], state: Optional[str], country: Optional[str]) -> List[str]:
        """Get popular local brands and services."""
        if self.brave_api_key and country:
            try:
                location = f"{city or state or country}"
                query = f"popular brands services {location}"
                results = self._search_brave(query, max_results=3)
                return [r.get("title", "") for r in results]
            except Exception as e:
                self.logger.error(f"Error fetching local brands: {str(e)}")
        
        return []
    
    def _get_cultural_notes(self, country: Optional[str]) -> List[str]:
        """Get cultural communication patterns."""
        if not country:
            return []
        
        # This could be enhanced with API calls or a knowledge base
        cultural_patterns = {
            "India": ["Respect for hierarchy", "Formal communication", "Festival seasons important"],
            "United States": ["Direct communication", "Emphasis on urgency", "Professional but casual"],
            "Japan": ["Extreme formality", "Indirect communication", "Group harmony valued"],
            "Germany": ["Precision and punctuality", "Formal titles", "Direct but polite"],
            "Brazil": ["Relationship-focused", "Warm communication", "Flexible timing"]
        }
        
        return cultural_patterns.get(country, [])
    
    def _get_timezone(self, city: Optional[str], country: Optional[str]) -> str:
        """Get timezone information."""
        # This could be enhanced with a timezone API
        return f"Check timezone for {city or country or 'location'}"
    
    def _get_business_practices(self, country: Optional[str]) -> List[str]:
        """Get business practice patterns."""
        if not country:
            return []
        
        # Could be enhanced with real-time data
        practices = {
            "India": ["9 AM - 6 PM typical", "Saturday work common", "Email primary communication"],
            "United States": ["9 AM - 5 PM typical", "Email and Teams", "Fast response expected"],
            "Japan": ["Early start times", "Long working hours", "Formal email etiquette"],
        }
        
        return practices.get(country, [])
    
    def _search_brave(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """Helper to search Brave API."""
        try:
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": self.brave_api_key
            }
            params = {"q": query, "count": max_results}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return [
                {"title": r.get("title"), "description": r.get("description")}
                for r in data.get("web", {}).get("results", [])
            ]
        except Exception as e:
            self.logger.error(f"Brave search error: {str(e)}")
            return []


class IndustryIntelligenceFetcher:
    """Fetch industry-specific news and trends."""
    
    def __init__(self):
        self.logger = Logger.get_logger("IndustryIntelligenceFetcher")
        self.brave_api_key = os.getenv("BRAVE_API_KEY")
        self.cache = {}
        self.cache_duration = timedelta(hours=12)
    
    def get_industry_context(self, industry: Optional[str]) -> Dict[str, Any]:
        """Get industry-specific intelligence."""
        if not industry:
            return {"industry": None, "trends": [], "news": []}
        
        cache_key = f"industry_{industry}"
        
        # Check cache
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                self.logger.info(f"Using cached industry data for {industry}")
                return cached_data
        
        self.logger.info(f"Fetching industry intelligence for {industry}")
        
        context = {
            "industry": industry,
            "current_trends": self._get_industry_trends(industry),
            "recent_news": self._get_industry_news(industry),
            "common_tools": self._get_industry_tools(industry),
            "compliance_requirements": self._get_compliance_info(industry)
        }
        
        # Cache the results
        self.cache[cache_key] = (context, datetime.now())
        
        return context
    
    def _get_industry_trends(self, industry: str) -> List[Dict[str, Any]]:
        """Get current industry trends."""
        if self.brave_api_key:
            try:
                query = f"{industry} industry trends {datetime.now().year}"
                return self._search_brave(query, max_results=3)
            except Exception as e:
                self.logger.error(f"Error fetching industry trends: {str(e)}")
        
        return []
    
    def _get_industry_news(self, industry: str) -> List[Dict[str, Any]]:
        """Get recent industry news."""
        if self.brave_api_key:
            try:
                query = f"{industry} news latest"
                return self._search_brave(query, max_results=3)
            except Exception as e:
                self.logger.error(f"Error fetching industry news: {str(e)}")
        
        return []
    
    def _get_industry_tools(self, industry: str) -> List[str]:
        """Get common tools/platforms in the industry."""
        # This could be enhanced with a knowledge base or API
        tools_map = {
            "technology": ["Slack", "GitHub", "Jira", "AWS", "Docker"],
            "finance": ["Bloomberg Terminal", "SAP", "QuickBooks", "Salesforce"],
            "healthcare": ["Epic", "Cerner", "HIPAA compliance tools"],
            "education": ["Canvas", "Blackboard", "Zoom", "Google Classroom"],
            "cybersecurity": ["CrowdStrike", "Splunk", "Palo Alto", "SOC tools"]
        }
        
        # Fuzzy match
        for key, tools in tools_map.items():
            if key.lower() in industry.lower():
                return tools
        
        return []
    
    def _get_compliance_info(self, industry: str) -> List[str]:
        """Get compliance requirements for the industry."""
        compliance_map = {
            "finance": ["SOX", "PCI-DSS", "GLBA"],
            "healthcare": ["HIPAA", "HITECH"],
            "technology": ["SOC 2", "ISO 27001", "GDPR"],
            "education": ["FERPA", "COPPA"]
        }
        
        for key, reqs in compliance_map.items():
            if key.lower() in industry.lower():
                return reqs
        
        return []
    
    def _search_brave(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """Helper to search Brave API."""
        try:
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": self.brave_api_key
            }
            params = {"q": query, "count": max_results, "freshness": "pw"}  # Past week
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return [
                {"title": r.get("title"), "description": r.get("description")}
                for r in data.get("web", {}).get("results", [])
            ]
        except Exception as e:
            self.logger.error(f"Brave search error: {str(e)}")
            return []
