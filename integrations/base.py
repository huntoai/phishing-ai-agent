"""Abstract base class for data sources."""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class DataSource(ABC):
    """Base interface for employee data sources."""
    
    @abstractmethod
    def enrich_organization(self, domain: str) -> Dict[str, Any]:
        """Fetch organization data by domain."""
        pass
    
    @abstractmethod
    def search_people(self, domain: str, per_page: int = 10) -> Dict[str, Any]:
        """Search for people by organization domain."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return data source name."""
        pass
