import os
import base64
import json
import requests
from dotenv import load_dotenv
load_dotenv()


def create_confluence_page_document(space_key: str, title: str, content: str):
    """
    Use this tool to create a new page in a specified Confluence space.
    Provide the 'space_key' (e.g., 'engineering'), the 'title' for the new page,
    and the 'content' for the page body in standard HTML (storage format).
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


    page_data = {
        "type": "page",
        "title": title,
        "space": {
            "key": space_key
        },
        "body": {
            "storage": {
                "value": f"<p>{content}</p>",
                "representation": "storage"
            }
        }
    }


    try:
        print(f"DEBUG: Attempting to create Confluence page: '{title}' in space '{space_key}'")
        create_response = requests.post(f"{CONFLUENCE_API_BASE}/content", headers=headers, json=page_data)
        create_response.raise_for_status()
        response_data = create_response.json()
        new_page_url = f"{CONFLUENCE_API_BASE.split('/wiki')[0]}/wiki" + response_data.get("_links", {}).get("webui", "")
        new_page_title = response_data.get("title", title)


        return {
            "success": True,
            "message": f"Successfully created Confluence page: '{new_page_title}'",
            "url": new_page_url,
            "id": response_data.get("id")
        }


    except requests.exceptions.RequestException as e:
        print(f"DEBUG: Failed to create Confluence page: {e}")
        error_details = ""
        try:
            error_json = e.response.json()
            error_message = error_json.get("message", "")
            error_details = f"Details: {error_message}"
        except (AttributeError, json.JSONDecodeError):
            pass
        return {"error": f"Failed to create Confluence page: {e}. {error_details}"}
    except Exception as e:
        print(f"DEBUG: An unexpected error occurred during Confluence page creation: {e}")
        return {"error": f"An unexpected error occurred: {e}"}


