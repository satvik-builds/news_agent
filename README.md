## Overview

This repository contains the **Daily Insights Agent**, a news‑focused AI system built with Google’s **Agent Development Kit (ADK)**.  
You can think of it as a “3‑minute news digest” engine: you give it a topic and time range, and it:
- Finds recent articles
- Extracts and processes their content
- Summarizes each article
- Assembles everything into a short, high‑quality digest

The intent is not just to build a working agent, but to **teach ADK architecture** through a concrete, realistic example.  
I’ve structured the code so that you can map each concept (agents, tools, loops, validation, session state) to a specific file.

If you want a step‑by‑step, command‑by‑command guide to running the agent, see `WALKTHROUGH.md`.

---

## System architecture & file structure

At a high level, the system is organized as a single ADK package, `news_digest_agent`, which exposes a `root_agent` that ADK knows how to run. The rest of the files support that agent with configuration, tools, and specialized sub‑agents.

Here is the structure, with how I intend you to read it:

```text
News_Agent/
├── news_digest_agent/          # Main ADK package
│   ├── __init__.py             # Exports root_agent and config for easy import
│   ├── agent.py                # Main orchestrator agent definition
│   ├── config.py               # Central configuration & API key loading
│   ├── tools.py                # Custom tools wrapped in FunctionTool
│   ├── validation_checkers.py  # Small agents that control LoopAgent flow
│   │
│   └── sub_agents/             # Specialized sub‑agents
│       ├── __init__.py         # Re‑exports all sub‑agents
│       ├── scraper_agent.py    # Finds relevant articles (uses google_search)
│       ├── processor_agent.py  # Fetches & cleans article content
│       ├── summarizer_agent.py # Summarizes individual articles
│       ├── digest_generator.py # Assembles the final digest
│       └── quality_agents.py   # Checks and refines digest quality
│
├── main.py                     # Simple entry point to load & inspect the agent
├── .env                        # Your API key (git‑ignored)
├── .gitignore                  # Ignore rules for Python, env, and editor files
├── requirements.txt            # Python dependencies
├── README.md                   # High‑level explanation (this file)
└── WALKTHROUGH.md              # Step‑by‑step “how to run it” guide
```

When you read the codebase, a good path is:
1. Skim `news_digest_agent/agent.py` to see the **orchestrator**.
2. Dive into `news_digest_agent/sub_agents/` to understand each stage of the pipeline.
3. Look at `news_digest_agent/validation_checkers.py` to see how the **quality loop** is controlled.
4. Refer back to `news_digest_agent/config.py` to see which knobs you can tune (models, limits, etc.).

---

## Key concepts

In this project I intentionally lean into a handful of core ADK concepts and give each of them a clear place in the code.

### Multi‑agent system

Rather than a single, giant prompt, the system is designed as a **pipeline of specialized agents**:
- **LLM‑powered agents**: Every agent is backed by a Gemini model defined in `config.py`.
- **Sequential flow**: The main agent in `agent.py` defines the order: search → process → summarize → digest → improve.
- **Parallel work**: Processing multiple articles is handled in parallel by ADK under the hood (you don’t see threads here; ADK orchestrates it for you).
- **Looping behavior**: A `LoopAgent` wraps the digest generation stage so the system can iteratively improve quality.

### Tools

Tools are how the agent reaches outside “pure text reasoning” into the real world:
- **Built‑in tools** such as `google_search` handle web search for relevant news.
- **Custom tools** live in `tools.py` and are wrapped with `FunctionTool` so the agents can call them (for example, saving digests to files or extracting full article text).

You can read `tools.py` as “everything the agent is allowed to do beyond just talking.”

### ADK patterns

The code follows the same patterns you’ll see in Google’s ADK samples:
- The `Agent` class is used to define each agent with a **name**, **model**, **description**, and **rich natural‑language instructions**.
- `LoopAgent` gives you retry/improvement loops without writing manual `while` loops everywhere.
- **Validation checkers** in `validation_checkers.py` are tiny agents that look at session state and decide whether the loop should continue or stop.
- **Session state** is the shared memory that lets agents pass intermediate results (URLs, article texts, summaries, quality flags) between each other.

If you’re using this repo to learn, the key idea is: each concept is mapped to a small, focused file so you can study it in isolation.

---

## Architecture explanation

In this section I’ll walk you through how the system behaves at runtime and how the pieces in the file structure work together.

### The main orchestrator (`agent.py`)

The heart of the system is the `news_digest_agent` defined in `news_digest_agent/agent.py`. This agent:
- Sets the overall **instruction** (you are a News Digest Agent; here is your workflow and tone).
- Wires together the **sub‑agents** that handle each stage of the pipeline.
- Registers the **tools** the agent is allowed to call (for example, saving the final digest to disk).

From ADK’s perspective, this `news_digest_agent` is the “root brain” that coordinates everything else. In `__init__.py`, it is exported as `root_agent` so the ADK web UI and external code can discover it easily.

### Sub‑agents as specialists

Rather than asking one agent to do everything, each sub‑agent focuses on a single responsibility:
- `scraper_agent` handles **finding articles**, using Google’s search tooling.
- `processor_agent` takes raw URLs and **extracts cleaned article text**.
- `summarizer_agent` turns each article into a **concise summary**.
- `digest_generator` stitches those summaries into a **coherent digest** tuned to the requested reading time.
- Agents in `quality_agents.py` review and, if needed, **refine** that digest.

If you open `news_digest_agent/sub_agents/`, you can read each file almost like a small chapter: one file, one responsibility, one prompt.

### The quality loop (`LoopAgent` + validation checkers)

To keep the digest quality high without a lot of hand‑written control flow, the project uses ADK’s `LoopAgent`:
- The `LoopAgent` is configured with a sequence: generate digest → check quality → refine → check again.
- After each pass, a validation checker from `validation_checkers.py` examines the session state (for example, a `quality_approved` flag).
- If the checker decides the digest is good enough, it **escalates**, telling the loop to stop.
- If not, the loop runs another iteration, up to the limit in `config.max_quality_iterations`.

The important idea is that “should we do another pass?” is expressed declaratively in the validator, not buried in a big imperative loop.

### Configuration as a single source of truth

The file `news_digest_agent/config.py` centralizes the main knobs you can tune:
- Which models to use for workers and critics (`worker_model`, `critic_model`)
- How many articles to process (`max_articles`)
- How many quality‑improvement passes to allow (`max_quality_iterations`)
- Target reading time and parallelism settings

It also loads `GOOGLE_API_KEY` from `.env` and configures the environment for the Gemini API. If anything is misconfigured, it fails fast with a clear error so you know to fix your `.env` before going further.

### How everything fits together

Putting it all together, a typical run looks like this:
1. ADK (via the web UI or your own code) calls `root_agent` from `news_digest_agent`.
2. The main agent asks you what you care about (topic, time range) and stores that in session state.
3. It calls the sub‑agents in order: the scraper finds articles, the processor extracts text, the summarizer creates per‑article summaries.
4. The `LoopAgent` around `digest_generator` produces an initial digest, then cycles through quality checking and refinement until the validation checker is satisfied or the iteration limit is hit.
5. Finally, the main agent can call tools (for example, saving the digest to a file) if you ask it to persist the result.

As you read through the code, you can map each of these steps back to a specific file, which is exactly how this project is meant to be used as a learning resource.

### Main Agent (`agent.py`)

The `news_digest_agent` is the orchestrator that coordinates all sub-agents:

```python
news_digest_agent = Agent(
    name="news_digest_agent",
    model=config.worker_model,
    description="Creates personalized news digests",
    instruction="...",  # Detailed workflow instructions
    sub_agents=[...],    # List of specialized agents
    tools=[...],         # Tools the agent can use
)
```

### Sub-Agents Pattern

Each sub-agent is a specialist:
- `scraper_agent`: Finds articles (uses `google_search`)
- `processor_agent`: Extracts content (uses custom `extract_article_text` tool)
- `summarizer_agent`: Creates summaries (pure LLM)
- `digest_generator`: Builds structured digest
- `quality_checker` + `digest_refiner`: Improve quality

### LoopAgent for Quality Improvement

```python
robust_digest_generator = LoopAgent(
    name="robust_digest_generator",
    sub_agents=[
        digest_generator,
        quality_checker,
        digest_refiner,
        QualityCheckPassed(),  # Validator
    ],
    max_iterations=3,
)
```

The `LoopAgent` automatically:
1. Runs `digest_generator` 
2. Checks quality with `quality_checker`
3. If quality < 85, runs `digest_refiner`
4. Repeats until `QualityCheckPassed` escalates (or max iterations)

### Validation Checkers

Custom `BaseAgent` subclasses control the loop:

```python
class QualityCheckPassed(BaseAgent):
    async def _run_async_impl(self, context):
        if context.session.state.get("quality_approved"):
            yield Event(actions=EventActions(escalate=True))  # Success!
        else:
            yield Event(author=self.name)  # Continue loop
```

`EventActions(escalate=True)` tells the `LoopAgent` to move to the next stage.



