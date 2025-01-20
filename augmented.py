import anthropic
import os
from dotenv import load_dotenv
import requests

load_dotenv(override=True)

client = anthropic.Anthropic()

def search_brave_news_ita(query: str) -> str:
    """Search news politics articles using Brave API"""
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": os.getenv("BRAVE_API_KEY")
    }
    
    url = f"https://api.search.brave.com/res/v1/news/search"
    params = {
        "q": query,
        "count": 5,  # Limit results to 5 articles
        "country": "IT",
        "search_lang": "it"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()
        
        # Format results into a readable string
        articles = []
        for article in results.get("results", []):
            articles.append(f"Title: {article.get('title')}\nURL: {article.get('url')}\nDescription: {article.get('description')}\n")
        
        return "\n".join(articles) if articles else "No results found."
    except Exception as e:
        return f"Error searching news: {str(e)}"

def search_brave_news(query: str) -> str:
    """Search news politics articles using Brave API"""
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": os.getenv("BRAVE_API_KEY")
    }
    
    url = f"https://api.search.brave.com/res/v1/news/search"
    params = {
        "q": query,
        "count": 5,  # Limit results to 5 articles
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()
        
        # Format results into a readable string
        articles = []
        for article in results.get("results", []):
            articles.append(f"Title: {article.get('title')}\nURL: {article.get('url')}\nDescription: {article.get('description')}\n")
        
        return "\n".join(articles) if articles else "No results found."
    except Exception as e:
        return f"Error searching news: {str(e)}"

def anthropic_tool_call_ita(prompt: str) -> str:
    """
    Make a tool-enabled call to Anthropic's Claude with Italian news search capability
    
    Args:
        prompt (str): The user's prompt to send to Claude
        
    Returns:
        str: Claude's final response after potential tool use
    """
    print(f"\n[DEBUG] Sending initial prompt to Claude: {prompt}")
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8000,
        tools=[{
            "name": "search_news",
            "description": "Search for recent news articles from Italian news sources using Brave Search API. Returns up to 5 relevant news articles with titles, descriptions and URLs.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for finding Italian news articles"
                    }
                },
                "required": ["query"]
            }
        }],
        messages=[{
            "role": "user", 
            "content": prompt
        }]
    )

    print(f"[DEBUG] Response stop reason: {response.stop_reason}")
    print(f"[DEBUG] Response content type: {response.content[0].type}")

    if response.stop_reason == "tool_use":
        tool_use = next(block for block in response.content if block.type == "tool_use")
        print(f"[DEBUG] Tool use detected. Search query: {tool_use.input['query']}")
            
        # Modified search query to focus on Italian news sources
        italian_query = f"site:corriere.it OR site:repubblica.it OR site:ilsole24ore.com OR site:ansa.it {tool_use.input['query']}"
        search_results = search_brave_news_ita(italian_query)
        print(f"[DEBUG] URLs results: {search_results}")
            
        final_response = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=8000,
                tools=[{
                    "name": "search_news",
                    "description": "Search for recent news articles from Italian news sources using Brave Search API. Returns up to 5 relevant news articles with titles, descriptions and URLs.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query for finding Italian news articles"
                            }
                        },
                        "required": ["query"]
                    }
                }],
                messages=[
                    {"role": "user", "content": prompt},
                    {
                        "role": "assistant",
                        "content": response.content
                    },
                    {
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": search_results
                        }]
                    }
                ]
            )
        print("[DEBUG] Final response received from Claude")
        return final_response.content[0].text
    
    print("[DEBUG] No tool use detected, returning initial response")
    return response.content[0].text

def anthropic_tool_call(prompt: str) -> str:
    """
    Make a tool-enabled call to Anthropic's Claude with news search capability
    
    Args:
        prompt (str): The user's prompt to send to Claude
        
    Returns:
        str: Claude's final response after potential tool use
    """
    print(f"\n[DEBUG] Sending initial prompt to Claude: {prompt}")
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8000,
        tools=[{
            "name": "search_news",
            "description": "Search for recent news articles on a specific topic using Brave Search API. Returns up to 5 relevant news articles with titles, descriptions and URLs.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for finding news articles"
                    }
                },
                "required": ["query"]
            }
        }],
        messages=[{
            "role": "user", 
            "content": prompt
        }]
    )

    print(f"[DEBUG] Response stop reason: {response.stop_reason}")
    print(f"[DEBUG] Response content type: {response.content[0].type}")

    if response.stop_reason == "tool_use":
        tool_use = next(block for block in response.content if block.type == "tool_use")
        print(f"[DEBUG] Tool use detected. Search query: {tool_use.input['query']}")
            
        search_results = search_brave_news(tool_use.input["query"])
        print(f"[DEBUG] URLs results: {search_results}")
        # print(f"[DEBUG] Search results obtained: {search_results[:1000]}...")  # Show first 200 chars
            
        final_response = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=8000,
                tools=[{
                    "name": "search_news",
                    "description": "Search for recent news articles on a specific topic using Brave Search API. Returns up to 5 relevant news articles with titles, descriptions and URLs.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query for finding news articles"
                            }
                        },
                        "required": ["query"]
                    }
                }],
                messages=[
                    {"role": "user", "content": prompt},
                    {
                        "role": "assistant",
                        "content": response.content
                    },
                    {
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": search_results
                        }]
                    }
                ]
            )
        print("[DEBUG] Final response received from Claude")
        return final_response.content[0].text
    
    print("[DEBUG] No tool use detected, returning initial response")
    return response.content[0].text

# translate the rich_content_summarized into italian
def translate_to_italian(english_content):
    italian_content = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8000,
        messages=[
            {"role": "user", "content": "You are an expert english to italian translator with a deep knowledge of italian politics. Translate the following text into italian maintaining the same structure and style: " + english_content}
        ]
    )
    return italian_content.content[0].text

# prompting to Claude and save result on rich_content_summarized
prompt_en = ("Imagine you are an Italian journalist with deep knowledge of politics. "
             "Create a report on today's most relevant news in the world of italian politics. "
             "Follow these steps: "
             "Search the web for news on the most prominent newspapers in Italy and around the world; "
             "Analyze the news and choose a maximum of 5 topics you want to cover; "
             "For each chosen topic, create a rich content that summarizes the main news.")

rich_content_summarized = anthropic_tool_call(prompt_en)
print(rich_content_summarized)
print(translate_to_italian(rich_content_summarized)) #traduci prima di stampare

promp_it = ("Immagina di essere un giornalista italiano con profonda conoscenza della politica. "
            "Creami un reportage della giornata odierna riguardo le notizie più rilevanti nel mondo della politica italiana. "
            "Ragiona attraverso questi step: "
            "Navigando sul web, cerca le notizie sui giornali italiani più di spicco; "
            "Analizza le notizie e scegli massimo 5 argomenti della quale ti vuoi occupare; "
            "Per ogni argomento scelto crea un contenuto ricco che riassume le principali notizie.")

italian_content = anthropic_tool_call_ita(promp_it)
print(italian_content)

def aggregator(content1, content2):
    final_content = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8000,
        messages=[
            {"role": "user", "content": "Sei un giornalista esperto con una profondaconoscenza della politica e una spiccata abilità nell'aggregare notizie da più fonti. Ti indico a seguire due flussi di notizie inerenti alla politica italiana. Dovrai analizzare i due contenuti, scegliere dai 3 ai 5 argomenti più di rilievo di essi e aggregarli sotto un unico reportage. Contenuto 1: " + content1 + " Contenuto 2: " + content2  }
        ]
    )
    return final_content.content[0].text

print("Ecco il report finale frutto dell'aggregazione: ")
print(aggregator(rich_content_summarized, italian_content))