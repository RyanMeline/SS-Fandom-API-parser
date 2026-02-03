#Fetch info dumps from Shadow Slave's fandom site
import requests
import json
# "Sunny", "Nephis", "Shadow_Slave_Wiki", 
OUTPUT_FILE = "fandom_dump.json"
page_names = ["Sunny/Memories","Nephis/Memories","Cassie/Memories","Effie/Memories","Kai/Memories","Mordret/Memories","Morgan/Memories","Anvil/Memories","Rain/Memories"]
url = "https://shadowslave.fandom.com/api.php"
all_pages = {}

def get_page_text(url, page_name):
    params = {
        "action": "query",
        "titles": page_name,
        "prop": "revisions",
        "rvprop": "content",
        "format": "json"
    }
    headers = {
        "User-Agent": "WikiBot/1.0" 
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        revisions = page.get("revisions", [])
        if revisions:
            return revisions[0].get("*","")
    return None

for name in page_names:
    text = get_page_text(url, name)
    page_url = "https://shadowslave.fandom.com/wiki/" + name
    if text:
        all_pages[name] = {
            "title": name,
            "content": text,
            "source": page_url
        }

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_pages, f, ensure_ascii=False, indent=2)
# changed the all_pages -> text to isolate text


print(f"Downloaded {len(page_names)} pages.")
