# 🧠 Intelligent Search Agent

[](https://www.python.org/downloads/)
[](https://opensource.org/licenses/MIT)

An AI-powered assistant built using **Google's Agent Development Kit (ADK)**. This agent can intelligently handle:

  - 🔍 External web research using the **Tavily API**
  - 🧭 Internal **Confluence document search**
  - 📄 **Webpage scraping** for content summarization
  - 🏗️ **Confluence page creation**
  - 💬 Natural, conversational responses

Ideal for developers and teams who want to automate research, documentation management, and contextual conversation using agent-based logic.

-----

## 📁 Project Structure

```
IntelligentSearchAgent/
├── .env                 # Your environment variables (private, not committed)
├── .gitignore           # Specifies files/folders to ignore from Git
├── README.md            # This file!
├── agent.py             # Main agent definitions and tool orchestration logic
├── requirements.txt     # Python dependencies
├── __init__.py          # Python package initialization (imports agent.py)
└── tools/
    ├── create_confluence_page.py
    ├── external_web_search.py
    ├── internal_confluence_search.py
    └── scrape_webpage_content.py
```

-----

## ⚙️ Setup Instructions

### 1\. 📦 Install Dependencies

Make sure Python 3.8+ is installed. It's recommended to use a virtual environment.

```bash
# Install dependencies
pip install -r requirements.txt
```

Your `requirements.txt` file should contain:

```
google-adk
requests
beautifulsoup4
tavily-python
python-dotenv
```

### 2\. 🛠️ Configure Environment Variables

Create a `.env` file in the root folder of your project (same level as `agent.py`) and add the following:

```env
# Gemini and Vertex AI settings
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your_google_cloud_project_id> # e.g., my-gemini-project-12345
GOOGLE_CLOUD_LOCATION=<gemini_model_location>       # e.g., us-central1
MODEL=<gemini_model_name>                            

# Tavily API (external search)
TAVILY_API_KEY=<your_tavily_api_key>

# Confluence integration (Optional, but required for Confluence tools)
# Your Confluence base API URL, e.g., https://your-domain.atlassian.net/wiki/rest/api
CONFLUENCE_API_BASE=<your_confluence_api_base_url>
# Your Confluence API Token (generated in Atlassian account settings)
CONFLUENCE_API_TOKEN=<your_confluence_token>
# The email associated with your Confluence API Token
CONFLUENCE_USER_EMAIL=<your_confluence_email>
```

**Important:** Add `.env` to your `.gitignore` file to ensure your sensitive credentials are not committed to source control.

-----

## 🚀 Features & Tools

| Feature                  | Tool / Function                   | Description                                                                 |
| :----------------------- | :-------------------------------- | :-------------------------------------------------------------------------- |
| 💬 Conversational Chat   | `conversational_agent`            | Handles greetings, jokes, and friendly interactions                         |
| 🔎 Internal Search       | `internal_confluence_search`      | Searches Confluence spaces for relevant pages and extracts clean content    |
| 🌐 Web Search            | `external_web_search`             | Performs external search using Tavily API                                   |
| 🧽 Web Scraping          | `scrape_webpage_content`          | Extracts readable text from user-provided URLs                              |
| 📄 Confluence Page Creator | `create_confluence_page_document` | Creates new Confluence pages with provided content                          |

-----

## 🧠 How It Works

The core `root_agent` is powered by **Gemini Pro (Vertex AI)**. It uses **strict decision protocols** to intelligently orchestrate tasks:

  * Routes casual conversations to a dedicated conversational sub-agent.
  * Prioritizes **internal Confluence document search** for factual queries.
  * Falls back to **external web search and content scraping** only if internal search yields no results or isn't applicable.
  * Creates Confluence pages **only after explicit user confirmation**.

All tool usage is **modular**, promoting clean separation of concerns and easy extensibility.

-----

## 🧪 Example Use Cases

  * "What's the latest cert-manager version on GKE?"
    → Agent searchesinternal confluence  → falls back to web if needed
  * "Create a page in PROD called 'Agent Logs' with content from this URL: \[URL]"
    → Agent scrapes URL → proposes page creation → creates on confirmation
  * "Summarize this article: \[URL]"
    → Agent scrapes article → summarizes content
  * "Hi, how are you?"
    → Agent provides a natural, friendly response

-----

## 🧰 Tech Stack

  * [Google ADK (Agent Development Kit)](https://github.com/google/agent-development-kit)
  * [Tavily API](https://docs.tavily.com)
  * [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
  * [Python Dotenv](https://pypi.org/project/python-dotenv/)
  * Gemini (via Vertex AI)

-----

## 🛡️ Safety Notes

  * Internal documentation (Confluence) is **prioritized** over external content sources.
  * External content is **sanitized and summarized**, never blindly displayed.
  * The agent will **not perform critical actions like creating pages** without **explicit user confirmation**.

-----

## ✅ Next Steps

To launch the agent's web interface for interaction:

```bash
adk web
```

Follow the instructions provided in your terminal after running this command to open the local web UI in your browser and start interacting with the agent.

-----

## 📬 Feedback & Contributions

Contributions are welcome\! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

