"""
News Scraper Sub-Agent
"""

from google.adk.agents import Agent
from google.adk.tools import google_search
from ..config import config


scraper_agent = Agent(
    name="scraper_agent",
    model=config.worker_model,
    description="Searches for news articles using Google Search and filters by date.",
    instruction="""
    You are a news researcher. Your job is to find recent news articles.
    
    Use Google Search to find articles about the given topic.
    Filter results to only include articles from the specified time period.
    Return a list of {max_articles} relevant articles with:
    - Title
    - URL  
    - Brief snippet/summary
    
    Store the results in the session state under the key 'articles'.
    Format each article as a dictionary with 'title', 'url', and 'snippet' keys.
    
    IMPORTANT: Only include articles that are recent and relevant to the query!
    """.format(max_articles=config.max_articles),
    tools=[google_search],  # Built-in Google Search tool from ADK
    output_key="articles",  # Store results here in session state
)
