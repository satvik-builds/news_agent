"""
Validation Checkers for the News Digest Agent

Based on the ADK pattern from agent-shutton.
"""

from typing import AsyncGenerator
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions


class DigestValidationChecker(BaseAgent):
    """Checks if the digest is valid and complete."""
    
    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Check if digest exists in session state."""
        if context.session.state.get("final_digest"):
            # Digest exists! Signal success
            yield Event(
                author=self.name,
                actions=EventActions(escalate=True),  # This moves to next stage
            )
        else:
            # Digest doesn't exist yet, do nothing (LoopAgent will retry)
            yield Event(author=self.name)


class QualityCheckPassed(BaseAgent):
    """Checks if the quality score meets the threshold."""
    
    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Check if quality approval flag is set."""
        if context.session.state.get("quality_approved"):
            # Quality is good! Escalate to finish
            yield Event(
                author=self.name,
                actions=EventActions(escalate=True),
            )
        else:
            # Quality not approved yet, continue loop
            yield Event(author=self.name)
