#Turn unstructured data dump from wiki into structured json
import json
import mwparserfromhell as mw
import re

INPUT_FILE = "fandom_dump.json"
OUTPUT_FILE = "json_formatted.json"

TABLE_NAME =  " class=\"article-table datatable moddedTable\""
# " class=\"wikitable sortable\""

def clean(text: str) -> str:
    return mw.parse(text).strip_code().strip()

def parse_table(text: str):
    lines = text.splitlines()

    headers = []
    rows = []
    current_row = []
    div_count = 0 #there are nested div's in some descriptions

    # first line is usually the {| class= stuff, so skip first line if its that
    if lines[0].startswith("!"):
        i = 0
    else:
        i = 1
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("!"):
            header = line[1:].strip()
            # some are ! scope="col" | Name
            if "|" in header:
                header = header.split("|", 1)[1]
            headers.append(header)
            # clean(header) -> header
            i += 1
        else:
            break

    
    for line in lines[i:]:
        line = line.rstrip()

        if line.startswith("|-"):
            if current_row:
                rows.append(current_row)
                current_row = []
            continue
            
        if line.startswith("|") and div_count == 0:
            cell = line[1:].strip()
            current_row.append(cell)
            #replaced clean(cell) with cell

            div_count += cell.count("<div")
            div_count -= cell.count("</div>")
            continue

        if current_row and line:
            current_row[-1] += "\n" + line

            div_count += line.count("<div")
            div_count -= line.count("</div>")
            # removed clean(line) replaced with line
    
    if current_row:
        rows.append(current_row)

    return headers, rows


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
    
def make_json_obj(headers, rows):
    objs = []
    for row in rows:
        row2 = (row + [""] * len(headers))[:len(headers)]
        objs.append(dict(zip(headers, row2)))
    return objs

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for page_title, page_info in data.items():
    wiki_text = page_info.get("content", "")

    results = re.findall(r"\{\|(.*?)\|\}", wiki_text, re.DOTALL)
        
    tables = []
    for text in results:
        if text.startswith(TABLE_NAME):
            tables.append(text)
    
    json_objs = []

    for table in tables:
        headers, rows = parse_table(table)
        json_objs.extend(make_json_obj(headers, rows))

    # structured_json_obj = []
    
    # for i, table in enumerate(tables, start = 1):
    #     headers, rows




        # redirect_target = follow_redirect(wiki_text)
    # if redirect_target:
    #     print(f"{page_title} redirects to {redirect_target}, skipping for now")
    #     continue

    # parsed = mw.parse(wiki_text)
    # print("Templates: ", len(parsed.filter_templates()))

    # for i in parsed.filter_templates():
    #     print("Template: ", i)

    # print("Headings: ", len(parsed.filter_headings()))
#     entity = Entity(page_title)

#     for template in parsed.filter_templates():
#         entity.attributes.update({param.name.strip(): str(param.value).strip() for param in template.params})

#     entity.links = [
#         str(link.title).strip()
#         for link in parsed.filter_wikilinks()
#         if str(link.title).strip() and not str(link.title).strip().startswith("Category:")
#     ]

#     entity.categories = [
#         str(link.title).strip()[len("Category:"):]
#         for link in parsed.filter_wikilinks()
#         if str(link.title).strip().startswith("Category:")
#     ]

# #Causing some errors with what i am assuming is nested template stuff
#     # templates = list(parsed.filter_templates())
#     # for template in templates:
#     #     parsed.remove(template)

#     entity.description = parsed.strip_code().strip()
#     structured_entities.append(entity.to_dict())

with open (OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(json_objs, f, indent=2, ensure_ascii=False)

# print(f"Processed {len(structured_entities)} pages. Saved to {OUTPUT_FILE}")