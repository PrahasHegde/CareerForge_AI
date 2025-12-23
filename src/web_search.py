from duckduckgo_search import DDGS
import time

def get_company_info(company_name):
    """
    Fetches company info using DuckDuckGo 'html' backend to avoid rate limits.
    Returns None if all attempts fail, triggering the AI fallback.
    """
    if not company_name:
        return None
    
    print(f"DEBUG: Searching web for {company_name}...") 

    try:
        results = []
        # Use DDGS context manager
        with DDGS() as ddgs:
            # FIX: backend="html" is slower but avoids the '202 Ratelimit' error
            # We request 3 results
            search_gen = ddgs.text(
                f"{company_name} company mission values tech stack recent news",
                region="wt-wt", 
                safesearch="off", 
                backend="html",  # <--- THIS IS THE KEY FIX
                max_results=3
            )
            
            if search_gen:
                results = list(search_gen)

        if not results:
            print("DEBUG: No results found via HTML backend.")
            return None

        # Format the output if successful
        context = "### 🏢 Company Intelligence (Live Web Data):\n"
        for result in results:
            title = result.get('title', 'News')
            body = result.get('body', '')
            link = result.get('href', '')
            context += f"- **{title}**: {body} ([Source]({link}))\n"
            
        return context

    except Exception as e:
        print(f"DEBUG: Search failed ({str(e)}). Switching to Internal Knowledge.")
        return None 