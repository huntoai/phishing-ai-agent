"""Abstract base class for enrichment sources."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class EnrichmentSource(ABC):
    """Base interface for employee enrichment sources."""
    
    @abstractmethod
    def enrich_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich employee with additional data."""
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """Return source name."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if source is available (API key configured, etc.)."""
        pass
