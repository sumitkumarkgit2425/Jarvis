import wikipedia
import webbrowser
import urllib.parse

def search_wikipedia(query):

    try:

        search_term = query.replace("wikipedia", "").replace("search", "").strip()
        if not search_term:
            return "What would you like me to search on Wikipedia?"
        results = wikipedia.summary(search_term, sentences=2)
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        return "There are multiple results. Can you be more specific?"
    except Exception:
        return "I could not find anything on Wikipedia for that query."

def search_google(query):

    search_term = query.replace("google", "").replace("search", "").strip()
    if not search_term:
        return "What would you like me to search on Google?"

    url = f"https://www.google.com/search?q={urllib.parse.quote(search_term)}"
    webbrowser.open(url)
    return "I have opened Google search for you."

def process_knowledge(query):

    if "wikipedia" in query:
        return search_wikipedia(query)
    elif "google" in query:
        return search_google(query)
    return None
