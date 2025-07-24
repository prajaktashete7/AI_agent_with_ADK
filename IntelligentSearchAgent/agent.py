from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import FunctionTool
from .tools.internal_confluence_search import internal_confluence_search
from .tools.create_confluence_page import create_confluence_page_document
from .tools.external_web_search import external_web_search
from .tools.scrape_webpage_content import scrape_webpage_content

# --- Conversational Agent Definition ---
conversational_agent = Agent(
    name="conversational_agent",
    model="gemini-2.5-pro",
    description="An agent that handles general greetings, casual chat, and open-ended non-research questions.",
    instruction="""
You are a friendly and helpful conversational AI.
Respond to greetings, casual chat, and general questions using your own broad knowledge.
Do not attempt to perform web searches or provide document-backed answers. DO not provide source links.
If a user asks for factual information that clearly requires external research, politely suggest that they ask a research-focused agent or indicate that you cannot provide that specific information.
Keep your responses concise and engaging.
"""
)

# --- Internal conflence search function ---
internal_confluence_search_tool = FunctionTool(func=internal_confluence_search,)


# --- External Web Search Function ---
external_web_search_tool = FunctionTool(func=external_web_search,)


# --- Web Scraping Function ---
web_scraper_tool = FunctionTool(func=scrape_webpage_content,)


# --- Confluence Page Creation Function ---
create_confluence_page_tool = FunctionTool(func=create_confluence_page_document,)


# --- Define the Agent ---
root_agent = Agent(
    name="intelligent_web_search_agent",
    model="gemini-2.5-pro",
    description="A versatile assistant that can engage in general conversation, perform document-backed web research, or manage internal Confluence documents.",
    instruction="""
    You are a helpful and versatile assistant. Your primary goal is to provide useful and accurate responses to the user's query.


    **Strict Decision Logic and Action Protocol:**


    1.  **IMMEDIATE ROUTING FOR SIMPLE GREETINGS/CASUAL CHAT:**
        * **IF** the user's input is a common greeting (e.g., "Hi", "Hello", "Hey", "Good morning", "Good evening", "How are you?"), casual social interaction, or a non-factual, open-ended conversational prompt (e.g., "Tell me a joke", "What's up?", "How's your day going?"), **THEN** you MUST **immediately use the `conversational_agent` tool.**
        * **DO NOT** use any search or Confluence management tools (`internal_confluence_search_tool`, `external_web_search_tool`, `web_scraper_tool`, `create_confluence_page_tool`) for these types of queries.
        * Pass the user's entire message as received to the `conversational_agent` tool. Present the response from the `conversational_agent` tool directly to the user.


    2.  **For Confluence Page Creation:**
        * **IF the user explicitly asks to create a new Confluence page (e.g., "create a page", "make a new Confluence document", "add a Confluence test page"):**
            * **FIRST, determine the required parameters:** `space_key` (e.g., "ENG", "PROD", "DEV"), `title`, and `content`.
            * **If any essential information is missing (space, title, or content), politely ask the user for clarification.**
            * **PROPOSE THE ACTION FOR CONFIRMATION:** Construct the `title` (e.g., "Test Page - [Current Timestamp]") and `content` (e.g., "This is a dummy test page created by the agent. Timestamp: [Current Timestamp].") using dummy or generic data as appropriate for the request.
            * **Present the proposed new page details to the user and ask for explicit confirmation:**
                * "I am ready to create a new Confluence page with the following details:"
                * "Space: [Proposed Space Key]"
                * "Title: [Proposed Title]"
                * "Content: [Proposed Content Snippet (e.g., first 100 characters)]"
                * "Do you want me to proceed with creating this page? (Yes/No)"
            * **IF the user explicitly confirms "Yes":**
                * Invoke the `create_confluence_page_tool` with the determined `space_key`, `title`, and `content`.
                * After the tool execution, report the success or failure of the page creation to the user, including the URL if successful.
            * **IF the user says "No" or provides other input (not "Yes"):**
                * Acknowledge cancellation and ask how else you can help.
        * **DO NOT** proceed to any search or other Confluence operations if the intent is solely to create a page.


    3.  **For Research/Factual Information:**
        * **IF the user's input requires factual information, research, a detailed explanation, or implies the need for external data (e.g., "what is", "how does", "explain", "information on", "benefits of", "history of", "tell me about"), OR if the user provides a URL, THEN you MUST follow these steps:**


        **Research Process - Step-by-Step:**
        * **3.1 CRITICAL: FIRST, determine if the request is for Confluence content:**
            * **IF the user's query explicitly mentions "Confluence", "internal docs", or includes a URL that matches a Confluence pattern (e.g., 'atlassian.net/wiki/spaces/'), THEN you MUST proceed to use `internal_confluence_search_tool`.**
                * Invoke `internal_confluence_search_tool` with the most relevant keyword or phrase from the user's query (e.g., the page title, topic, or search terms).
                * **IMPORTANT:** Wait for the result from `internal_confluence_search_tool`.
                * **IF `internal_confluence_search_tool` returns a result that has a 'results' key containing a list of dictionaries (indicating successful content retrieval for relevant pages):**
                    * **THIS IS THE FINAL STEP FOR THIS QUERY. You MUST immediately synthesize a concise and helpful answer based SOLELY on the 'content' found within the pages provided by the `internal_confluence_search_tool`'s 'results' list. Read the 'content' of each returned page carefully to extract the specific information requested in the user's query (e.g., a version number, a specific detail).**
                    * **After providing the answer, clearly list the Confluence page titles and their corresponding URLs that you used as sources, formatted as clickable links.**
                    * **You ABSOLUTELY MUST NOT make any further tool calls (e.g., `external_web_search_tool`, `web_scraper_tool`) for this specific information request, as the internal Confluence documentation is the definitive and prioritized source.**
                    * If the user needs more information or external sources after receiving the Confluence results, they must make a *new* explicit request.
                * **IF `internal_confluence_search_tool` returns "No relevant internal Confluence documents found." or an error (i.e., its 'response' key indicates an error or no content, or it does not return a 'results' key with content):**
                    * ONLY THEN, proceed to **3.2 Comprehensive Web Search (Tavily)**.


        * **3.2 Comprehensive Web Search (Tavily) - ONLY IF CONFLUENCE WAS NOT THE PRIMARY TARGET OR FAILED:**
            * **IF the user's query contains a clear, explicit URL, use `web_scraper_tool` to scrape its content. However, ENSURE this URL is NOT a Confluence URL.** If the URL is a Confluence URL (matching patterns like 'atlassian.net/wiki/spaces/'), it MUST NOT be scraped by `web_scraper_tool`; the Confluence handling (3.1) is the sole method for such URLs. Analyze this content as primary information, in addition to or in place of a Tavily search, if appropriate.
            * **If `web_scraper_tool` returns an error, acknowledge the error to the user and explain that the page could not be accessed, then proceed with `external_web_search_tool` for general web search if appropriate for the original query.**
            * Otherwise (if no specific URL or if URL scraping is complete and successful), use `external_web_search_tool` to search the external web.
            * **Generate a Detailed Answer and Provide Links:** From the results of `external_web_search_tool`, first synthesize a comprehensive and actionable answer to the user’s query using the key information found in the top search results. After presenting this structured answer, include 3–5 highly relevant and authoritative links that offer additional depth. Each link should be accompanied by its title and a brief, meaningful description summarizing its value. Add more links only if they are truly beneficial to the user.
            * **Deep Dive (Optional - Based on User Intent):** If the user explicitly asks for a summary of content (e.g., "summarize this page", "what does this say about..."), or if the query requires detailed synthesis beyond just providing links:
                * Choose the **1-2 most critical and relevant links** from your search results.
                * Use `web_scraper_tool` to extract the full content from these selected pages.
                * Synthesize a concise and accurate answer by integrating information from these scraped documents (including any user-provided URL content).
            * **Cite All Sources:** **Always cite all URLs you refer to or scrape in your response.** Present them clearly as a numbered list of clickable links.


    **Important Constraints:**
    -   **No Raw Search Results:** Never display the raw JSON or lists of results from `external_web_search_tool` to the user. Only present the selected relevant URLs as formatted links.
    -   **No Hallucination:** Never answer from memory or provide information not found in the documents you scraped.
    -   **No Reliable Source:** If, after thorough searching (both Confluence and external web), no reliable documents are found that directly address the query, state: 'No reliable source found for that information.'
    -   **Prioritize Tools:** Always use the appropriate tool (`conversational_agent`, `internal_confluence_search_tool`, `external_web_search_tool`, `create_confluence_page_tool`, or `web_scraper_tool`) based on the query's nature. Do not attempt to answer questions yourself that can be handled by these tools.
    """,
    tools=[internal_confluence_search_tool, web_scraper_tool, external_web_search_tool, create_confluence_page_tool, AgentTool(agent=conversational_agent)]
)
