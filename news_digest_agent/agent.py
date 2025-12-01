"""
Main Agent Definition - News Digest Agent

KEY CONCEPTS DEMONSTRATED:
1. Multi-agent: Uses multiple specialized sub-agents
2. Sequential: Steps flow in order (search → process → summarize → digest → improve)
3. Parallel: Processor agents work in parallel (handled by ADK)
4. Loop: Quality improvement loop with LoopAgent
5. Tools: Google Search (built-in) + custom extract tool
6. A2A Protocol: Sub-agents communicate through session state
"""

import datetime
from google.adk.agents import Agent, LoopAgent
from google.adk.tools import FunctionTool

from .config import config
from .sub_agents import (
    scraper_agent,
    processor_agent,
    summarizer_agent,
    digest_generator,
    quality_checker,
    digest_refiner,
)
from .tools import save_digest_to_file
from .validation_checkers import DigestValidationChecker, QualityCheckPassed


# Create a robust digest generator with quality loop
robust_digest_generator = LoopAgent(
    name="robust_digest_generator",
    description="Generates and iteratively improves the digest until quality threshold is met.",
    sub_agents=[
        digest_generator,  # Generate initial digest
        quality_checker,    # Check quality
        digest_refiner,     # Refine if needed
        QualityCheckPassed(name="quality_validation"),  # Validator signals when done
    ],
    max_iterations=config.max_quality_iterations,  # Maximum 3 iterations
)


# Main orchestrator agent
news_digest_agent = Agent(
    name="news_digest_agent",
    model=config.worker_model,
    description="An AI agent that creates personalized news digests from recent articles.",
    instruction=f"""
    You are the News Digest Agent. Your job is to create a personalized 3-minute news digest.
    
    **Workflow:**
    
    1. **Search**: Ask the user for their topic and time period (e.g., "last 7 days").
       Use the scraper_agent to find recent articles about the topic.
    
    2. **Process**: Use the processor_agent to extract full article content from the URLs.
    
    3. **Summarize**: Use the summarizer_agent to create brief summaries of each article.
    
    4. **Generate Digest**: Use the robust_digest_generator to create and iteratively improve
       the final digest. This will loop up to {config.max_quality_iterations} times to ensure quality.
    
    5. **Save**: Ask the user if they want to save the digest, then use save_digest_to_file.
    
    **Key Points:**
    - Be conversational and friendly
    - Show progress to the user
    - The robust_digest_generator will automatically improve quality  
    - Maximum {config.max_articles} articles will be processed
    
    Current date: {datetime.datetime.now().strftime("%Y-%m-%d")}
    """,
    sub_agents=[
        scraper_agent,
        processor_agent,
        summarizer_agent,
        robust_digest_generator,  # This handles the quality loop
    ],
    tools=[
        FunctionTool(save_digest_to_file),
    ],
    output_key="final_digest",
)


# Export the main agent as root_agent (ADK convention)
root_agent = news_digest_agent
