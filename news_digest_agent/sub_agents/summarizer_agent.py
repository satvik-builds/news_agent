"""
Summarizer Sub-Agent
"""

from google.adk.agents import Agent
from ..config import config


summarizer_agent = Agent(
    name="summarizer_agent",
    model=config.worker_model,
    description="Creates concise summaries of articles.",
    instruction="""
    You are a technical content summarizer. Your job is to create brief, informative summaries.
    
    For each article provided, create a 2-3 sentence summary that:
    - Captures the key points
    - Is relevant to the user's query
    - Is written in clear, engaging language
    
    Store summaries in session state under 'summaries'.
    Each summary entry should include the article title and the summary text.
    """,
    output_key="summaries",
)
