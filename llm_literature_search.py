#!/usr/bin/env python
"""
LLM Literature Explorer - A tool for exploring repositories at the intersection of LLMs and literature
"""

import argparse
import json
import os
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional, Union

# GitHub API constants
GITHUB_API_URL = "https://api.github.com"
SEARCH_REPOS_ENDPOINT = "/search/repositories"
SEARCH_CODE_ENDPOINT = "/search/code"

class GithubExplorer:
    """A class to search and explore GitHub repositories related to LLMs and literature."""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize the explorer with authentication token if provided.
        
        Args:
            token: GitHub personal access token
        """
        self.headers = {
            "Accept": "application/vnd.github+json"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def search_repositories(self, query: str, sort: str = "stars", 
                           order: str = "desc", per_page: int = 30, 
                           page: int = 1) -> Dict:
        """
        Search GitHub repositories based on a query.
        
        Args:
            query: Search query string
            sort: Sorting criteria (stars, forks, updated)
            order: Sort order (asc, desc)
            per_page: Number of results per page
            page: Page number
            
        Returns:
            Dict containing search results
        """
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page,
            "page": page
        }
        
        url = f"{GITHUB_API_URL}{SEARCH_REPOS_ENDPOINT}"
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return {"items": []}
        
        return response.json()
    
    def find_llm_literature_projects(self, page: int = 1, 
                                    per_page: int = 30) -> Dict:
        """
        Search for projects specifically at the intersection of LLMs and literature.
        
        Args:
            page: Page number for results
            per_page: Number of results per page
            
        Returns:
            Dict containing filtered search results
        """
        # Try different queries to capture the intersection
        queries = [
            "language models literature",
            "llm literature analysis",
            "gpt literary analysis",
            "natural language processing literature",
            "computational literary analysis",
            "llm poetry generation",
            "transformer models literature",
            "literary text generation",
            "nlp literary criticism",
            "ai storytelling",
        ]
        
        all_results = []
        
        for query in queries:
            print(f"Searching for: {query}")
            results = self.search_repositories(query, per_page=per_page, page=page)
            
            if "items" in results:
                all_results.extend(results["items"])
                
            # Respect GitHub API rate limits
            time.sleep(2)
        
        # Remove duplicates based on repository ID
        unique_repos = {}
        for repo in all_results:
            if repo["id"] not in unique_repos:
                unique_repos[repo["id"]] = repo
        
        return {"items": list(unique_repos.values())}
    
    def analyze_results(self, results: Dict) -> Dict:
        """
        Analyze search results to extract patterns and insights.
        
        Args:
            results: Search results from a GitHub search
            
        Returns:
            Dict containing analysis of the repositories
        """
        analysis = {
            "total_count": len(results["items"]),
            "languages": {},
            "topics": {},
            "created_dates": {},
            "stars_distribution": {
                "0-10": 0,
                "11-50": 0,
                "51-100": 0,
                "101-500": 0,
                "501-1000": 0,
                "1001+": 0
            }
        }
        
        for repo in results["items"]:
            # Analyze programming languages
            language = repo.get("language")
            if language:
                analysis["languages"][language] = analysis["languages"].get(language, 0) + 1
            
            # Analyze topics/tags
            topics = repo.get("topics", [])
            for topic in topics:
                analysis["topics"][topic] = analysis["topics"].get(topic, 0) + 1
            
            # Analyze creation dates (by year)
            if "created_at" in repo:
                year = datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ").year
                analysis["created_dates"][str(year)] = analysis["created_dates"].get(str(year), 0) + 1
            
            # Analyze stars distribution
            stars = repo.get("stargazers_count", 0)
            if stars <= 10:
                analysis["stars_distribution"]["0-10"] += 1
            elif stars <= 50:
                analysis["stars_distribution"]["11-50"] += 1
            elif stars <= 100:
                analysis["stars_distribution"]["51-100"] += 1
            elif stars <= 500:
                analysis["stars_distribution"]["101-500"] += 1
            elif stars <= 1000:
                analysis["stars_distribution"]["501-1000"] += 1
            else:
                analysis["stars_distribution"]["1001+"] += 1
        
        # Sort languages and topics by frequency
        analysis["languages"] = dict(sorted(analysis["languages"].items(), 
                                           key=lambda x: x[1], reverse=True))
        analysis["topics"] = dict(sorted(analysis["topics"].items(), 
                                        key=lambda x: x[1], reverse=True))
        analysis["created_dates"] = dict(sorted(analysis["created_dates"].items()))
        
        return analysis
    
    def save_results(self, results: Dict, filename: str) -> None:
        """
        Save search results to a JSON file.
        
        Args:
            results: Search results to save
            filename: Output filename
        """
        # Simplify and clean up results for saving
        simplified_results = []
        for repo in results["items"]:
            simplified_repo = {
                "id": repo["id"],
                "name": repo["name"],
                "full_name": repo["full_name"],
                "html_url": repo["html_url"],
                "description": repo["description"],
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"],
                "language": repo.get("language"),
                "stargazers_count": repo["stargazers_count"],
                "forks_count": repo["forks_count"],
                "topics": repo.get("topics", [])
            }
            simplified_results.append(simplified_repo)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(simplified_results, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to {filename}")

def main():
    """Main function to run the explorer."""
    parser = argparse.ArgumentParser(description="Explore LLM and literature repositories on GitHub")
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument("--output", default="llm_literature_repos.json", help="Output JSON filename")
    parser.add_argument("--analyze", action="store_true", help="Perform analysis on results")
    parser.add_argument("--per-page", type=int, default=30, help="Results per page")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    
    args = parser.parse_args()
    
    # Get token from env var if not provided
    token = args.token or os.environ.get("GITHUB_TOKEN")
    
    explorer = GithubExplorer(token)
    results = explorer.find_llm_literature_projects(page=args.page, per_page=args.per_page)
    
    print(f"Found {len(results['items'])} repositories")
    
    explorer.save_results(results, args.output)
    
    if args.analyze:
        analysis = explorer.analyze_results(results)
        analysis_file = args.output.replace(".json", "_analysis.json")
        
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"Analysis saved to {analysis_file}")
        
        # Print summary
        print("\n=== Analysis Summary ===")
        print(f"Total repositories: {analysis['total_count']}")
        
        print("\nTop 5 Programming Languages:")
        for i, (lang, count) in enumerate(list(analysis["languages"].items())[:5]):
            print(f"  {i+1}. {lang}: {count}")
        
        print("\nTop 5 Topics:")
        for i, (topic, count) in enumerate(list(analysis["topics"].items())[:5]):
            print(f"  {i+1}. {topic}: {count}")
        
        print("\nStars Distribution:")
        for stars_range, count in analysis["stars_distribution"].items():
            print(f"  {stars_range}: {count}")

if __name__ == "__main__":
    main()
