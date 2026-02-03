#Turn unstructured data dump from wiki into structured json
import json
import mwparserfromhell as mw
import re

INPUT_FILE = "fandom_dump.json"
OUTPUT_FILE = "json_formatted.json"

TABLE_NAME = " class=\"article-table datatable moddedTable\""
TABLE_NAME1 = " class=\"wikitable sortable\""

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
            headers.append(clean(header))
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
            # removed clean(line) replaced with line

            div_count += line.count("<div")
            div_count -= line.count("</div>")
    
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

with open (OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(json_objs, f, indent=2, ensure_ascii=False)
