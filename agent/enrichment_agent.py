"""AI agent for enriching employee profiles with dynamic knowledge fetching."""
import os
import json
from typing import Dict, Any, Optional, List
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from datetime import datetime
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from integrations.knowledge_tools import (
    PhishingTrendsFetcher,
    RegionalIntelligenceFetcher,
    IndustryIntelligenceFetcher
)
from config import DEFAULT_MODEL, MAX_RETRIES
from agent.prompts import (
    ENRICHMENT_SYSTEM_PROMPT,
    get_enrichment_prompt_with_tools,
    get_enrichment_prompt_fallback
)


class EnrichmentAgent:
    """AI agent for enriching employee profiles with dynamic knowledge fetching."""
    
    def __init__(self):
        # Always set OPENAI_API_KEY in os.environ for all libraries
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            os.environ['OPENAI_API_KEY'] = openai_key

        model_name = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

        self.trends_fetcher = PhishingTrendsFetcher()
        self.regional_fetcher = RegionalIntelligenceFetcher()
        self.industry_fetcher = IndustryIntelligenceFetcher()

        self.agent = Agent(
            model=OpenAIChatModel(model_name),
            system_prompt=ENRICHMENT_SYSTEM_PROMPT,
            retries=MAX_RETRIES
        )
        
        self._register_tools()
    
    def _register_tools(self):
        """Register knowledge fetching tools with the Pydantic AI agent."""
        
        @self.agent.tool
        def get_phishing_trends(ctx: RunContext[None], year: Optional[int] = None) -> List[Dict[str, Any]]:
            """
            Fetch latest phishing attack trends and techniques.
            Use this to get current phishing methods, not hardcoded data.
            
            Args:
                year: Year to fetch trends for (defaults to current year)
            
            Returns:
                List of current phishing trends with techniques and descriptions
            """
            if year is None:
                year = datetime.now().year
            
            trends = self.trends_fetcher.get_latest_trends(year)
            return trends
        
        @self.agent.tool
        def get_regional_intelligence(ctx: RunContext[None], 
                                     city: Optional[str] = None,
                                     state: Optional[str] = None, 
                                     country: Optional[str] = None) -> Dict[str, Any]:
            """
            Fetch regional intelligence including holidays, culture, local brands, and business practices.
            Use this to understand location-specific attack opportunities.
            
            Args:
                city: City name
                state: State/province name
                country: Country name
            
            Returns:
                Regional context with holidays, brands, cultural notes, timezone, business practices
            """
            return self.regional_fetcher.get_regional_context(city, state, country)
        
        @self.agent.tool
        def get_industry_intelligence(ctx: RunContext[None], industry: str) -> Dict[str, Any]:
            """
            Fetch industry-specific intelligence including trends, news, tools, and compliance.
            Use this to understand industry-specific attack vectors.
            
            Args:
                industry: Industry name (e.g., "technology", "finance", "healthcare")
            
            Returns:
                Industry context with current trends, news, common tools, compliance requirements
            """
            return self.industry_fetcher.get_industry_context(industry)
    
    def enrich(self, employee: Dict[str, Any], organization: Optional[Dict[str, Any]] = None, current_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Enrich employee with full context - AI dynamically fetches knowledge using tools.
        The AI agent will call tools to fetch:
        - Latest phishing trends
        - Regional intelligence (holidays, culture, brands)
        - Industry intelligence (news, trends, tools)
        """
        current_date = current_date or datetime.now().strftime("%Y-%m-%d %B")
        prompt = get_enrichment_prompt_with_tools(
            json.dumps(employee, indent=2),
            json.dumps(organization or {}, indent=2),
            current_date
        )
        
        result = self.agent.run_sync(prompt)
        
        try:
            # Parse the AI response
            data = result.output.strip()
            if '```json' in data:
                data = data.split('```json')[1].split('```')[0].strip()
            elif '```' in data:
                data = data.split('```')[1].split('```')[0].strip()
            
            parsed_data = json.loads(data)
            
            # Add metadata about tool usage
            if hasattr(result, 'tool_calls'):
                parsed_data['_metadata'] = {
                    'tools_used': [call.tool_name for call in result.tool_calls],
                    'analysis_date': datetime.now().isoformat()
                }
            
            return parsed_data
            
        except Exception as e:
            # Fallback if parsing fails
            return {
                "vulnerability_score": 50,
                "risk_level": "medium",
                "risk_factors": [f"Analysis parsing failed: {str(e)}"],
                "recommended_vectors": ["generic_phishing"],
                "psychological_triggers": ["urgency"],
                "regional_insights": [],
                "timing_recommendations": [],
                "_error": str(e)
            }
