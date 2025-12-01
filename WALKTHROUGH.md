## Walkthrough: Running the Daily Insights Agent 📰

This walkthrough explains, step by step, how **you** can install, configure, and run the Daily Insights Agent on your machine.

The goal is that if you follow this from top to bottom, you will:
- Have all dependencies installed
- Have your API key configured correctly
- Be able to talk to the agent through the ADK web interface

---

## 1. Install dependencies

From the project root (`News_Agent`):

```bash
pip install -r requirements.txt
```

This installs:
- `google-adk` – the Agent Development Kit the agent is built on
- `python-dotenv` – for loading your `.env` file
- `beautifulsoup4` and `requests` – used by the scraping tools

---

## 2. Configure your Google API key

The agent uses Gemini through the Google Generative AI API.

1. **Get an API key**
   - Go to: `https://makersuite.google.com/app/apikey`
   - Create a key (or reuse an existing one)

2. **Create a `.env` file in the project root**

   On Windows (PowerShell):

   ```bash
   echo "GOOGLE_API_KEY=your_actual_key_here" > .env
   ```

   Or create `.env` manually with this content:

   ```text
   GOOGLE_API_KEY=your_actual_key_here
   ```

3. **Replace** `your_actual_key_here` with your real key.

When `news_digest_agent/config.py` runs, it:
- Loads `.env`
- Reads `GOOGLE_API_KEY`
- Fails fast with a clear error if the key is missing or still set to a placeholder

---

## 3. Verify your setup with `main.py`

Before you open any UI, it’s useful to confirm that:
- The API key is visible
- The configuration loads
- The root agent can be imported

From the project root:

```bash
python main.py
```

If everything is configured correctly, you’ll see:
- The agent name
- The model being used
- Max articles
- Max quality iterations
- A short summary of how to start the agent

If there is a configuration error (for example, missing API key), `main.py` will print:
- A clear error message
- A short “Quick Fix” checklist telling you exactly how to fix your `.env`

---

## 4. Start the ADK web interface (recommended)

The nicest way to use this project is through the **ADK web UI**, which lets you chat with the agent and see how it behaves.

### 4.1. Install the ADK CLI

The `google-adk` package should already be installed from step 1. If you need to install it separately:

```bash
pip install google-adk
```

### 4.2. Run the web interface

**On Windows (PowerShell):**

The `adk` command might not be in your PATH. Try these methods in order:

**Method A: Direct command (if available)**
```powershell
adk web
```

**Method B: Via Python module (if Method A fails)**
```powershell
python -m google.adk.web
```

**Method C: Check Python Scripts folder**
If the above don't work, the `adk` executable might be in your Python Scripts folder. Try:
```powershell
python -m pip show -f google-adk | Select-String "adk"
```

Then run it with the full path, or add the Scripts folder to your PATH:
```powershell
# Find your Python Scripts folder (usually something like):
# C:\Users\YourName\AppData\Local\Programs\Python\Python310\Scripts\
# Then add it to PATH or run directly:
& "C:\path\to\Scripts\adk.exe" web
```

**On Linux/Mac:**
```bash
adk web
```

### 4.3. Troubleshooting: "adk is not recognized"

If you see `'adk' is not recognized as the name of a cmdlet, function, script file, or operable program`:

1. **Verify installation:**
   ```powershell
   python -m pip show google-adk
   ```

2. **Try the Python module approach:**
   ```powershell
   python -m google.adk.web
   ```

3. **Check if ADK has a different entry point:**
   - Some versions of `google-adk` may not include a CLI
   - Check the [official ADK documentation](https://ai.google.dev/adk) for the current way to start the web interface
   - You might need to use programmatic access instead (see section 5.2)

4. **Alternative: Use programmatic access**
   If the CLI isn't available, you can still use the agent programmatically (see section 5.2 below).

### 4.4. Once the web interface is running

1. **Open the URL** printed in the terminal (usually `http://localhost:8000`).

2. **Select your agent** (the exported `root_agent` from `news_digest_agent`) in the UI if needed.

3. **Start a conversation**, for example:
   - "Create a 3‑minute news digest about AI developments in the last 7 days."
   - "Give me a news digest on climate change from the last week."

Behind the scenes, the UI will:
- Call the `news_digest_agent` orchestrator
- Let it invoke the sub‑agents and tools
- Use the `LoopAgent` to refine the digest quality

---

## 5. Alternative ways to use the agent

### 5.1. Using `main.py` as a lightweight check

You can always rerun:

```bash
python main.py
```

to quickly confirm that:
- The project imports correctly
- The configuration is valid
- You’re pointing at the expected model

This is handy after you edit `config.py`.

---

### 5.2. Programmatic usage from Python

If you want to integrate this agent into another Python script or notebook, you can import it directly:

```python
from news_digest_agent import root_agent, config

print(f"Agent: {root_agent.name}")
print(f"Model: {config.worker_model}")
```

At this point you have full access to the ADK `Agent` object.  
You would typically:
- Create an ADK session
- Pass messages to the agent
- Let ADK handle orchestration, tools, and looping

For full details on session management, see the official ADK docs.

---

## 6. What to try once it’s running

Once your agent is live in the ADK UI, here are some example prompts you can use to explore the system:

- “Summarize the top 5 news stories about quantum computing from the last 3 days.”
- “Create a 3‑minute digest about global economic trends this week.”
- “Give me a concise digest of AI safety news this month.”

As you experiment, pay attention to:
- How the agent searches, processes, summarizes, and refines
- How the quality of the digest improves over iterations

That’s the complete walkthrough — from a clean clone of the repo to a fully running News Digest Agent you can talk to.


