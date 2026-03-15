"""
Search module for ScriptForge (Pro Features)
Handles Brave Search integration for trend analysis
"""

import requests
import json
from typing import List, Dict, Any, Optional
import config

def search_trending_topics(query: str, count: int = 5) -> Optional[List[str]]:
    """
    Search for trending topics related to a query using Brave Search
    
    Args:
        query: Search query
        count: Number of results to return
        
    Returns:
        List of trending topics or None if failed
    """
    
    if not config.BRAVE_API_KEY:
        print("Brave Search API key not configured")
        return None
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": config.BRAVE_API_KEY
    }
    
    params = {
        "q": query,
        "count": min(count, config.SEARCH_COUNT),
        "freshness": f"pd{config.TREND_ANALYSIS_DAYS}"  # Past X days
    }
    
    try:
        response = requests.get(
            config.BRAVE_SEARCH_URL,
            headers=headers,
            params=params,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            return extract_trending_topics(data)
        else:
            print(f"Brave Search API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Brave Search API call failed: {e}")
        return None

def extract_trending_topics(search_data: Dict[str, Any]) -> List[str]:
    """
    Extract trending topics from Brave Search results
    
    Args:
        search_data: JSON response from Brave Search API
        
    Returns:
        List of trending topics
    """
    
    topics = []
    
    try:
        # Extract from web results
        if "web" in search_data and "results" in search_data["web"]:
            for result in search_data["web"]["results"][:5]:  # Top 5 results
                title = result.get("title", "")
                if title and len(title) > 10:  # Filter out very short titles
                    topics.append(title)
        
        # Extract from news results if available
        if "news" in search_data and "results" in search_data["news"]:
            for result in search_data["news"]["results"][:3]:  # Top 3 news
                title = result.get("title", "")
                if title and len(title) > 10:
                    topics.append(f"📰 {title}")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_topics = []
        for topic in topics:
            if topic not in seen:
                seen.add(topic)
                unique_topics.append(topic)
        
        return unique_topics[:10]  # Return top 10 unique topics
        
    except Exception as e:
        print(f"Error extracting topics: {e}")
        return []

def analyze_competition(query: str) -> Optional[Dict[str, Any]]:
    """
    Analyze competition for a topic
    
    Args:
        query: Search query
        
    Returns:
        Competition analysis data or None if failed
    """
    
    if not config.BRAVE_API_KEY:
        return None
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": config.BRAVE_API_KEY
    }
    
    params = {
        "q": query,
        "count": 10
    }
    
    try:
        response = requests.get(
            config.BRAVE_SEARCH_URL,
            headers=headers,
            params=params,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            return analyze_search_results(data)
        else:
            return None
            
    except Exception as e:
        print(f"Competition analysis failed: {e}")
        return None

def analyze_search_results(search_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze search results for competition insights
    
    Args:
        search_data: JSON response from Brave Search API
        
    Returns:
        Analysis dictionary
    """
    
    analysis = {
        "total_results": 0,
        "top_domains": [],
        "content_types": [],
        "estimated_competition": "Low"  # Low, Medium, High
    }
    
    try:
        # Count total results
        if "web" in search_data:
            analysis["total_results"] = search_data["web"].get("total", 0)
        
        # Analyze top domains
        domains = {}
        if "web" in search_data and "results" in search_data["web"]:
            for result in search_data["web"]["results"][:10]:
                url = result.get("url", "")
                if url:
                    # Extract domain
                    domain = url.split('/')[2] if '//' in url else url.split('/')[0]
                    domain = domain.replace('www.', '')
                    domains[domain] = domains.get(domain, 0) + 1
        
        # Sort domains by frequency
        sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)
        analysis["top_domains"] = [domain for domain, count in sorted_domains[:5]]
        
        # Estimate competition level
        total_results = analysis["total_results"]
        if total_results < 100000:
            analysis["estimated_competition"] = "Low"
        elif total_results < 1000000:
            analysis["estimated_competition"] = "Medium"
        else:
            analysis["estimated_competition"] = "High"
        
        return analysis
        
    except Exception as e:
        print(f"Error analyzing search results: {e}")
        return analysis

def suggest_content_angles(topic: str) -> List[str]:
    """
    Suggest content angles for a given topic
    
    Args:
        topic: Main topic
        
    Returns:
        List of content angle suggestions
    """
    
    angles = [
        f"How to {topic} (Step-by-step tutorial)",
        f"5 Common Mistakes When {topic} (And How to Avoid Them)",
        f"The Future of {topic} (Trends and Predictions)",
        f"{topic} for Beginners (Complete Guide)",
        f"Advanced Techniques for {topic} (Pro Tips)",
        f"{topic} vs. [Alternative] (Comparison)",
        f"How I {topic} (Personal Story/Case Study)",
        f"Tools and Resources for {topic}",
        f"{topic} on a Budget (Cost-Effective Solutions)",
        f"{topic} Myths Debunked (Fact vs Fiction)"
    ]
    
    return angles[:5]  # Return top 5 angles