#Turn unstructured data dump from wiki into structured json
import json
import mwparserfromhell
import re

INPUT_FILE = "fandom_dump.json"
OUTPUT_FILE = "json_formatted.json"

class Entity:
    def __init__(self, name):
        self.name = name
        self.attributes = {}
        self.links = []
        self.categories = []
        self.description = ""
    
    def to_dict(self):
        return {
            "name": self.name,
            "attributes": self.attributes,
            "links": self.links,
            "categories": self.categories,
            "description": self.description
        }
    
def follow_redirect(wiki_text):
    # if (#REDIRECT [[Target]]), return target page name. else return none

    match = re.match(r'#REDIRECT\s+\[\[(.*?)\]\]', wiki_text, re.IGNORECASE)
    if match:
        return match.group(1).replace(" ", "_")
    return None

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

structured_entities = []

for page_title, page_info in data.items():
    wiki_text = page_info.get("content", "")

    redirect_target = follow_redirect(wiki_text)
    if redirect_target:
        print(f"{page_title} redirects to {redirect_target}, skipping for now")
        continue

    parsed = mwparserfromhell.parse(wiki_text)
    entity = Entity(page_title)

    for template in parsed.filter_templates():
        entity.attributes.update({param.name.strip(): str(param.value).strip() for param in template.params})

    entity.links = [
        str(link.title).strip()
        for link in parsed.filter_wikilinks()
        if str(link.title).strip() and not str(link.title).strip().startswith("Category:")
    ]

    entity.categories = [
        str(link.title).strip()[len("Category:"):]
        for link in parsed.filter_wikilinks()
        if str(link.title).strip().startswith("Category:")
    ]

#Causing some errors with what i am assuming is nested template stuff
    # templates = list(parsed.filter_templates())
    # for template in templates:
    #     parsed.remove(template)

    entity.description = parsed.strip_code().strip()
    structured_entities.append(entity.to_dict())

with open (OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(structured_entities, f, indent=2, ensure_ascii=False)

print(f"Processed {len(structured_entities)} pages. Saved to {OUTPUT_FILE}")