#!/usr/bin/env python
"""
Visualization tools for LLM Literature Explorer results.
This script creates visualizations from the analysis results.
"""

import argparse
import json
import os
from typing import Dict, List, Optional

try:
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.ticker import MaxNLocator
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("WARNING: matplotlib not installed. Visualizations will not be available.")
    print("To install: pip install matplotlib")


class ResultsVisualizer:
    """Visualization tools for LLM Literature Explorer results."""
    
    def __init__(self, analysis_file: str, output_dir: str = "visualizations"):
        """
        Initialize the visualizer with analysis data.
        
        Args:
            analysis_file: Path to the analysis JSON file
            output_dir: Directory to save visualization images
        """
        if not HAS_MATPLOTLIB:
            raise ImportError("matplotlib is required for visualization")
        
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Load analysis data
        with open(analysis_file, 'r', encoding='utf-8') as f:
            self.analysis = json.load(f)
    
    def visualize_languages(self, limit: int = 10) -> str:
        """
        Create a bar chart of programming languages.
        
        Args:
            limit: Maximum number of languages to show
            
        Returns:
            Path to the saved visualization
        """
        languages = self.analysis["languages"]
        
        # Sort languages by count and take top 'limit'
        sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:limit]
        langs = [item[0] if item[0] else "Unknown" for item in sorted_langs]
        counts = [item[1] for item in sorted_langs]
        
        # Create the visualization
        plt.figure(figsize=(10, 6))
        plt.bar(langs, counts, color='skyblue')
        plt.title(f'Top {limit} Programming Languages in LLM-Literature Projects')
        plt.xlabel('Programming Language')
        plt.ylabel('Number of Repositories')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save the visualization
        output_path = os.path.join(self.output_dir, 'languages.png')
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def visualize_topics(self, limit: int = 15) -> str:
        """
        Create a horizontal bar chart of common topics.
        
        Args:
            limit: Maximum number of topics to show
            
        Returns:
            Path to the saved visualization
        """
        topics = self.analysis["topics"]
        
        # Sort topics by count and take top 'limit'
        sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:limit]
        topic_names = [item[0] for item in sorted_topics]
        counts = [item[1] for item in sorted_topics]
        
        # Create the visualization
        plt.figure(figsize=(10, 8))
        y_pos = np.arange(len(topic_names))
        plt.barh(y_pos, counts, color='lightgreen')
        plt.yticks(y_pos, topic_names)
        plt.title(f'Top {limit} Topics in LLM-Literature Projects')
        plt.xlabel('Number of Repositories')
        plt.tight_layout()
        
        # Save the visualization
        output_path = os.path.join(self.output_dir, 'topics.png')
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def visualize_stars_distribution(self) -> str:
        """
        Create a pie chart of stars distribution.
        
        Returns:
            Path to the saved visualization
        """
        stars = self.analysis["stars_distribution"]
        
        # Prepare data for pie chart
        labels = list(stars.keys())
        sizes = list(stars.values())
        
        # Filter out categories with zero count
        filtered_labels = []
        filtered_sizes = []
        for label, size in zip(labels, sizes):
            if size > 0:
                filtered_labels.append(label)
                filtered_sizes.append(size)
        
        # Create the visualization
        plt.figure(figsize=(10, 7))
        plt.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%', 
                startangle=140, shadow=True)
        plt.axis('equal')
        plt.title('Stars Distribution in LLM-Literature Projects')
        plt.tight_layout()
        
        # Save the visualization
        output_path = os.path.join(self.output_dir, 'stars_distribution.png')
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def visualize_creation_timeline(self) -> str:
        """
        Create a line chart of repository creation dates.
        
        Returns:
            Path to the saved visualization
        """
        dates = self.analysis["created_dates"]
        
        # Sort dates and prepare data
        years = sorted(dates.keys())
        counts = [dates[year] for year in years]
        
        # Create the visualization
        plt.figure(figsize=(12, 6))
        plt.plot(years, counts, marker='o', linestyle='-', color='purple')
        plt.title('Repository Creation Timeline for LLM-Literature Projects')
        plt.xlabel('Year')
        plt.ylabel('Number of Repositories Created')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Ensure x-axis shows all years
        ax = plt.gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        
        plt.tight_layout()
        
        # Save the visualization
        output_path = os.path.join(self.output_dir, 'creation_timeline.png')
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def create_all_visualizations(self) -> List[str]:
        """
        Create all available visualizations.
        
        Returns:
            List of paths to saved visualizations
        """
        output_paths = []
        
        output_paths.append(self.visualize_languages())
        output_paths.append(self.visualize_topics())
        output_paths.append(self.visualize_stars_distribution())
        output_paths.append(self.visualize_creation_timeline())
        
        return output_paths
    
    def create_html_report(self, output_file: str = "report.html") -> str:
        """
        Create an HTML report with all visualizations and analysis.
        
        Args:
            output_file: Output HTML filename
            
        Returns:
            Path to the HTML report
        """
        # Create visualizations
        self.create_all_visualizations()
        
        # Build HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>LLM-Literature Projects Analysis</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                .visualization {{
                    margin: 30px 0;
                    text-align: center;
                }}
                .visualization img {{
                    max-width: 100%;
                    height: auto;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 5px;
                }}
                .stats {{
                    background-color: #f9f9f9;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .footer {{
                    margin-top: 50px;
                    text-align: center;
                    font-size: 0.9em;
                    color: #7f8c8d;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>LLM-Literature Projects Analysis</h1>
                <p>This report provides an analysis of GitHub repositories at the intersection of Large Language Models and Literature.</p>
                
                <div class="stats">
                    <h2>Key Statistics</h2>
                    <p><strong>Total Repositories Analyzed:</strong> {self.analysis["total_count"]}</p>
                </div>
                
                <div class="visualization">
                    <h2>Programming Languages</h2>
                    <p>Distribution of programming languages used in LLM-Literature projects.</p>
                    <img src="visualizations/languages.png" alt="Programming Languages Distribution">
                </div>
                
                <div class="visualization">
                    <h2>Popular Topics</h2>
                    <p>Most common topics and tags in the repositories.</p>
                    <img src="visualizations/topics.png" alt="Popular Topics">
                </div>
                
                <div class="visualization">
                    <h2>Stars Distribution</h2>
                    <p>How repository popularity (by stars) is distributed.</p>
                    <img src="visualizations/stars_distribution.png" alt="Stars Distribution">
                </div>
                
                <div class="visualization">
                    <h2>Creation Timeline</h2>
                    <p>When repositories in this space were created over time.</p>
                    <img src="visualizations/creation_timeline.png" alt="Creation Timeline">
                </div>
                
                <div class="footer">
                    <p>Generated by LLM Literature Explorer on {self._get_current_date()}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Save HTML report
        output_path = os.path.join(self.output_dir, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _get_current_date(self) -> str:
        """Get current date formatted as string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")


def main():
    """Main function to run the visualizer."""
    parser = argparse.ArgumentParser(description="Visualize LLM Literature Explorer results")
    parser.add_argument("--analysis", default="llm_literature_repos_analysis.json", 
                       help="Path to analysis JSON file")
    parser.add_argument("--output-dir", default="visualizations", 
                       help="Directory to save visualizations")
    parser.add_argument("--report", default="report.html", 
                       help="Filename for HTML report")
    
    args = parser.parse_args()
    
    if not HAS_MATPLOTLIB:
        print("ERROR: matplotlib is required for visualization")
        print("Install it with: pip install matplotlib")
        return
    
    try:
        visualizer = ResultsVisualizer(args.analysis, args.output_dir)
        report_path = visualizer.create_html_report(args.report)
        print(f"Report generated at: {report_path}")
        
        print("Individual visualizations:")
        for viz_path in visualizer.create_all_visualizations():
            print(f"  - {viz_path}")
            
    except FileNotFoundError:
        print(f"ERROR: Analysis file '{args.analysis}' not found.")
        print("Run the search tool with --analyze flag first.")
    except json.JSONDecodeError:
        print(f"ERROR: '{args.analysis}' is not a valid JSON file.")
    except Exception as e:
        print(f"ERROR: {str(e)}")


if __name__ == "__main__":
    main()
