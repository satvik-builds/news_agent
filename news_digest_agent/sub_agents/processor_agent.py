"""
Article Processor Sub-Agent
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from ..config import config
from ..tools import extract_article_text


processor_agent = Agent(
    name="processor_agent",
    model=config.worker_model,
    description="Extracts clean text from article URLs.",
    instruction="""
    You are a content extractor. Your job is to fetch article content from URLs.
    
    For each article URL provided, use the extract_article_text tool to get the content.
    Store the extracted text along with the article metadata.
    
    If extraction fails for an article, note the error but continue with others.
    Store results in session state under 'processed_articles'.
    
    Each processed article should have:
    - title
    - url
    - content (the extracted text)
    - processed (True/False)
    """,
    tools=[FunctionTool(extract_article_text)],  # Our custom tool wrapped in FunctionTool
    output_key="processed_articles",
)
