"""
Quality Checker Sub-Agent
"""

from google.adk.agents import Agent
from ..config import config


quality_checker = Agent(
    name="quality_checker",
    model=config.critic_model,  # Use critic model for assessment
    description="Assesses digest quality and provides improvement feedback.",
    instruction="""
    You are a content quality assessor. Evaluate news digests for quality.
    
    Assess the digest on:
    1. Clarity and readability (Is it easy to understand?)
    2. Structure and organization (Is it well-organized?)
    3. Completeness (Does it cover the topic well?)
    4. Engagement (Is it interesting to read?)
    5. Length (Is it appropriate for a 3-minute read?)
    
    Provide a score from 0-100 and specific feedback.
    
    If score >= 85, set 'quality_approved' to True in session state.
    If score < 85, provide specific improvement suggestions.
    
    Store your assessment in 'quality_score' and 'quality_feedback'.
    """,
    output_key="quality_feedback",
)


digest_refiner = Agent(
    name="digest_refiner",
    model=config.worker_model,
    description="Refines the digest based on quality feedback.",
    instruction="""
    You are a content editor. Improve the digest based on feedback provided.
    
    Take the current digest and the quality feedback.
    Make specific improvements to address the feedback while maintaining structure and format.
    
    Store the improved digest in 'current_digest' (which will become 'final_digest' when approved).
    """,
    output_key="current_digest",
)
