import os
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()


def external_web_search(query: str, search_depth: str = "basic"):
    """
    Searches the external web using the Tavily API to find relevant pages.
    Takes a `query` string and returns a list of dictionaries, each with
    'title', 'link', and 'snippet' for relevant web pages.
    Use `search_depth='advanced'` for more comprehensive results when needed.
    """
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    if not TAVILY_API_KEY:
        return {"error": "Tavily API key is not set."}


    try:
        tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
        results_json = tavily_client.search(
            query=query.strip(),
            search_depth=search_depth,
            max_results=5,
            include_answer=False,
            include_raw_content=False,
        )


        results = results_json.get("results", [])
        if not results:
            return {"response": "No reliable source found for that information."}


        links_md = ""
        for idx, item in enumerate(results, 1):
            title = item.get("title", "No Title")
            url = item.get("url", "No URL")
            snippet = item.get("content", "")
            links_md += f"{idx}. [{title}]({url}) – {snippet[:150]}...\n"


        return {"response": f"Here are some relevant sources:\n\n{links_md}"}


    except Exception as e:
        return {"response": f"External web search failed: {e}"}


