from dotenv import load_dotenv
import os
import base64
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode


def internal_confluence_search(query: str, limit: int = 3):
    """
    Searches internal Confluence content based on a keyword or phrase,
    then fetches and extracts the full content for the top results.
    """
    CONFLUENCE_API_BASE = os.getenv("CONFLUENCE_API_BASE")
    CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
    CONFLUENCE_USER_EMAIL = os.getenv("CONFLUENCE_USER_EMAIL")


    if not (CONFLUENCE_API_BASE and CONFLUENCE_API_TOKEN and CONFLUENCE_USER_EMAIL):
        return {"error": "Confluence credentials are not configured in environment variables."}
   
   
   
    auth_header_value = base64.b64encode(f"{CONFLUENCE_USER_EMAIL}:{CONFLUENCE_API_TOKEN}".encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": f"Basic {auth_header_value}",
        "Content-Type": "application/json"
    }


    print(f"DEBUG: Confluence search query: '{query}'")
    print(f"DEBUG: Using API Base: {CONFLUENCE_API_BASE}")


    try:
        search_params = {
            "cql": f'text ~ "{query}"',
            "limit": limit,
        }
        print(f"DEBUG: Confluence search URL: {CONFLUENCE_API_BASE}/content/search?{urlencode(search_params)}")


        search_response = requests.get(f"{CONFLUENCE_API_BASE}/content/search", headers=headers, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()
        print(f"DEBUG: Confluence initial search response (raw JSON): {search_data}")


        found_results = search_data.get("results", [])
        print(f"DEBUG: Number of results from initial search: {len(found_results)}")


        if not found_results:
            print("DEBUG: No results found in initial search.")
            return {"response": "No relevant internal Confluence documents found."}


        final_results = []
        for result_meta in found_results:
            content_id = result_meta.get("id")
            title = result_meta.get("title", "No Title (from meta)")
            print(f"DEBUG: Processing result ID: {content_id}, Title: {title}")


            if not content_id:
                print(f"DEBUG: Skipping result due to missing ID: {result_meta}")
                continue


            content_url = f"{CONFLUENCE_API_BASE}/content/{content_id}"
            content_params = {"expand": "body.view,version"}
            print(f"DEBUG: Fetching full content from URL: {content_url}?{urlencode(content_params)}")


            content_response = requests.get(content_url, headers=headers, params=content_params)
            content_response.raise_for_status()
            full_content_data = content_response.json()
            print(f"DEBUG: Full content response (raw JSON) for ID {content_id}: {full_content_data}")


            raw_html_content = full_content_data.get("body", {}).get("view", {}).get("value", "")
            print(f"DEBUG: Raw HTML content length for ID {content_id}: {len(raw_html_content)}")


            content_text = BeautifulSoup(raw_html_content, "html.parser").get_text(separator="\n", strip=True)
            print(f"DEBUG: Cleaned text content length for ID {content_id}: {len(content_text)}")


            webui_link = full_content_data.get("_links", {}).get("webui")
            if webui_link:
                url = f"{CONFLUENCE_API_BASE.split('/wiki')[0]}/wiki{webui_link}"
            else:
                url = ""
            print(f"DEBUG: Generated URL for ID {content_id}: {url}")


            version = full_content_data.get("version", {}).get("number")


            if content_text.strip():
                final_results.append({
                    "id": content_id,
                    "title": title,
                    "url": url,
                    "content": content_text[:1000] + "..." if len(content_text) > 1000 else content_text,
                    "version": version
                })
            else:
                print(f"DEBUG: Skipped result ID {content_id} due to empty or minimal extracted content.")


        if not final_results:
            print("DEBUG: No final results after content extraction/filtering.")
            return {"response": "No relevant internal Confluence documents found after content extraction."}


        return {"results": final_results}


    except requests.exceptions.Timeout:
        print("DEBUG: Confluence request timed out.")
        return {"error": f"Request to Confluence timed out."}
    except requests.exceptions.RequestException as e:
        print(f"DEBUG: Confluence API request failed: {e}")
        return {"error": f"Confluence API request failed: {e}"}
    except Exception as e:
        print(f"DEBUG: An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred during Confluence search: {e}"}