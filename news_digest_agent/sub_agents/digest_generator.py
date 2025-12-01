"""
Digest Generator Sub-Agent
"""

from google.adk.agents import Agent
from ..config import config


digest_generator = Agent(
    name="digest_generator",
    model=config.worker_model,
    description="Generates a structured 3-minute news digest.",
    instruction="""
    You are a technical content editor. Create a cohesive {reading_time}-minute news digest.
    
    Use the article summaries provided to create a structured digest with:
    
    📰 **Your 3-Minute Digest: [Topic] (Last [N] Days)**
    
    🔍 **Overview**:
    [1-2 sentence overview of the main trend or theme]
    
    🚀 **Key Developments**:
    [3-4 bullet points of the most important developments]
    
    💡 **Notable Insights**:
    [2-3 key takeaways or implications]
    
    ⏱️ **Reading time**: ~{reading_time} minutes
    
    📎 **Sources**: [List article titles]
    
    Make it engaging, informative, and exactly {reading_time} minutes of reading.
    Target approximately 300-400 words.
    
    Store the digest in session state under 'current_digest' or 'final_digest'.
    """.format(reading_time=config.target_reading_time),
    output_key="current_digest",
)
