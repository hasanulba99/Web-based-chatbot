from duckduckgo_search import DDGS

def search_web(query, max_results=5):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(r)
        if not results:
            return "❌ No web results found."

        output = f"🔍 Top results for: {query}\n\n"
        for res in results:
            title = res.get("title", "No Title")
            link = res.get("href", "")
            snippet = res.get("body", "")
            output += f"• {title}\n  {snippet}\n  {link}\n\n"

        return output.strip()
    except Exception as e:
        return f"⚠️ Error searching the web: {e}"