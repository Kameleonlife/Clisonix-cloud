"""
YouTube integration utilities
"""
from typing import Dict, Any
import httpx


async def _get_json(client: httpx.AsyncClient, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch JSON data from URL
    
    Args:
        client: HTTP client instance
        url: Target URL
        params: Query parameters
        
    Returns:
        JSON response as dictionary
    """
    response = await client.get(url, params=params)
    response.raise_for_status()
    return response.json()
