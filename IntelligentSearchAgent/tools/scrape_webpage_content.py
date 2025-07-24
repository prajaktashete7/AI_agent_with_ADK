import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()


def scrape_webpage_content(url: str):
    """
    Use this tool to extract clean, readable text from a specific web page URL.
    Provide the full URL as an argument.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()


        soup = BeautifulSoup(response.text, 'html.parser')


        for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'form', 'noscript', 'img', 'link', 'meta']):
            tag.decompose()


        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content') or soup.find('div', {'role': 'main'})
        if main_content:
            text = main_content.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)


        max_length = 8000
        if len(text) > max_length:
            return {"url": url, "content": text[:max_length] + "\n\n... (content truncated for brevity)"}
        else:
            return {"url": url, "content": text}


    except requests.exceptions.Timeout:
        return {"error": f"Request to {url} timed out after 15 seconds."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to retrieve content from {url}: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred while scraping {url}: {e}"}