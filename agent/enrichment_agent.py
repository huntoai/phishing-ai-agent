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


class EnrichmentAgent:
    """AI agent for enriching employee profiles with dynamic knowledge fetching."""
    
    def __init__(self):
        model_name = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
        
        self.trends_fetcher = PhishingTrendsFetcher()
        self.regional_fetcher = RegionalIntelligenceFetcher()
        self.industry_fetcher = IndustryIntelligenceFetcher()
        
        self.agent = Agent(
            model=OpenAIChatModel(model_name),
            system_prompt="""You are an expert social engineering analyst specializing in phishing attack planning.

Your task: Analyze employee and organization data to assess phishing vulnerability and recommend attack strategies.

IMPORTANT: You have access to tools that fetch real-time intelligence:
- get_phishing_trends: Fetches latest phishing attack techniques and trends
- get_regional_intelligence: Fetches location-specific holidays, culture, brands, events
- get_industry_intelligence: Fetches industry-specific news, trends, tools, compliance

USE THESE TOOLS to gather current intelligence before making your analysis. DO NOT rely on hardcoded knowledge.

Analysis Framework:
1. First, call get_phishing_trends to understand current attack methods
2. If employee has location data, call get_regional_intelligence
3. If organization has industry data, call get_industry_intelligence
4. Synthesize all gathered intelligence into vulnerability assessment

Return vulnerability assessment as JSON:
{
    "vulnerability_score": 0-100,
    "risk_level": "low/medium/high/critical",
    "risk_factors": ["specific reasons for vulnerability"],
    "recommended_vectors": ["specific attack vectors based on latest trends"],
    "psychological_triggers": ["applicable psychological principles"],
    "regional_insights": ["location-specific attack opportunities from real data"],
    "timing_recommendations": ["best times/events based on real holidays/events"]
}""",
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
        
        prompt = f"""Analyze this employee profile for phishing vulnerability:

=== CURRENT DATE ===
{current_date or datetime.now().strftime("%Y-%m-%d %B")}

=== EMPLOYEE PROFILE ===
{json.dumps(employee, indent=2)}

=== ORGANIZATION PROFILE ===
{json.dumps(organization or {}, indent=2)}

=== ANALYSIS INSTRUCTIONS ===

1. GATHER INTELLIGENCE USING TOOLS:
   - Call get_phishing_trends() to get current attack methods (REQUIRED)
   - If employee has city/state/country, call get_regional_intelligence() for location context
   - If organization has industry, call get_industry_intelligence() for industry context

2. ANALYZE VULNERABILITY:
   - Use the fetched phishing trends (not hardcoded knowledge) to recommend attack vectors
   - Use regional intelligence to identify location-specific opportunities
   - Use industry intelligence to identify industry-specific vectors
   - Assess technical sophistication based on role and organization
   - Evaluate psychological susceptibility patterns

3. RECOMMEND ATTACK STRATEGY:
   - Match attack vectors from current trends to employee profile
   - Identify optimal timing based on real regional holidays/events
   - Leverage industry-specific tools and compliance pressures
   - Consider cultural communication patterns from regional data

4. SCORE VULNERABILITY:
   - Calculate 0-100 score based on multiple risk factors
   - Set risk_level: low (<40), medium (40-65), high (65-85), critical (>85)
   - List specific, actionable risk factors
   - Provide psychological triggers that would work on this person

Remember: Use the tools to fetch real-time data. Don't rely on assumptions."""
        
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

    
    def enrich(self, employee: Dict[str, Any], organization: Optional[Dict[str, Any]] = None, current_date: Optional[str] = None) -> Dict[str, Any]:
        """Enrich employee with full context - AI determines regional relevance dynamically."""
        
        prompt = f"""Analyze this employee profile for phishing vulnerability:

=== CURRENT DATE ===
{current_date or 'Unknown'}

=== EMPLOYEE PROFILE (Complete Data) ===
{json.dumps(employee, indent=2)}

=== ORGANIZATION PROFILE (Complete Data) ===
{json.dumps(organization or {}, indent=2)}

=== YOUR ANALYSIS TASKS ===

1. LOCATION & REGIONAL ANALYSIS:
   - Research and identify relevant local festivals, holidays, and cultural events for their location
   - Consider regional business practices, communication styles, and trust patterns
   - Identify location-specific brands, services, and government agencies to impersonate
   - Analyze timezone and working hours for optimal attack timing

2. ROLE & RESPONSIBILITY ASSESSMENT:
   - Analyze job title and seniority for authority dynamics
   - Identify role-specific pressures (deadlines, reporting, compliance)
   - Determine likely daily workflows and tool usage
   - Assess decision-making authority and access levels

3. VULNERABILITY SCORING:
   - Technical sophistication indicators
   - Authority susceptibility patterns
   - Time pressure and urgency responsiveness
   - Social media exposure and personal information availability
   - Professional network size and connection patterns

4. ATTACK VECTOR RECOMMENDATIONS:
   - Consider LATEST phishing trends (2024-2025): QR codes, AI deepfakes, Teams/Slack, supply chain, crypto, MFA bypass
   - Match vectors to role, location, and organizational context
   - Prioritize vectors with highest success probability
   - Include both technical and social engineering approaches

5. PSYCHOLOGICAL TRIGGER IDENTIFICATION:
   - Authority (hierarchy, executive pressure)
   - Urgency (deadlines, time-sensitive issues)
   - Fear (job security, compliance violations)
   - Curiosity (career opportunities, industry news)
   - Greed (bonuses, rewards, exclusive offers)
   - Social proof (peer requests, team activities)
   - Reciprocity (gifts, favors, helpfulness)

6. TIMING & CONTEXT:
   - Seasonal opportunities (tax season, holidays, fiscal year-end)
   - Industry-specific cycles (earnings, conferences, product launches)
   - Current events and trending topics relevant to their location/industry
   - Optimal days/times based on role and timezone

Provide comprehensive, actionable intelligence for targeted phishing campaign design."""
        
        result = self.agent.run_sync(prompt)
        
        try:
            data = result.output.strip()
            if '```json' in data:
                data = data.split('```json')[1].split('```')[0].strip()
            elif '```' in data:
                data = data.split('```')[1].split('```')[0].strip()
            return json.loads(data)
        except Exception as e:
            return {
                "vulnerability_score": 50,
                "risk_level": "medium",
                "risk_factors": ["Analysis failed"],
                "recommended_vectors": ["generic_phishing"],
                "psychological_triggers": ["urgency"],
                "regional_insights": [],
                "timing_recommendations": []
            }
