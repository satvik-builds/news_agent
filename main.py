"""
Main Entry Point for News Digest Agent

This script provides an easy way to start the agent using ADK.
Run this with: python main.py
Or use ADK web interface: adk web
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from news_digest_agent import root_agent, config

def main():
    """
    Main entry point for the News Digest Agent.
    
    This script can be used to:
    1. Verify the agent is properly configured
    2. Run the agent programmatically (if needed)
    3. Export the agent for ADK web interface
    """
    try:
        print("=" * 60)
        print("📰 News Digest Agent - Starting Up")
        print("=" * 60)
        print(f"✅ Agent loaded: {root_agent.name}")
        print(f"📦 Model: {config.worker_model}")
        print(f"📰 Max Articles: {config.max_articles}")
        print(f"🔁 Max Quality Iterations: {config.max_quality_iterations}")
        print("=" * 60)
        print("\n🚀 To start the agent, use one of these methods:")
        print("\n1. ADK Web Interface (Recommended):")
        print("   adk web")
        print("\n2. Programmatic Usage:")
        print("   from news_digest_agent import root_agent")
        print("   # Use root_agent with ADK session management")
        print("\n" + "=" * 60)
        
        # Export for ADK
        return root_agent
    except ValueError as e:
        print("=" * 60)
        print("❌ Configuration Error")
        print("=" * 60)
        print(str(e))
        print("\n📝 Quick Fix:")
        print("1. Create a .env file in the project root")
        print("2. Add: GOOGLE_API_KEY=your_actual_key_here")
        print("3. Get your key from: https://makersuite.google.com/app/apikey")
        print("=" * 60)
        return None

if __name__ == "__main__":
    agent = main()
    print(f"\n✅ Agent ready: {agent.name}")
    print("💡 Use 'adk web' to launch the interactive web interface")

