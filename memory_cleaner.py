# when cleaning names
# id=\nStuff\n|{{tooltop|Stuff<br>}}
# Save after |
# delete {{tooltop|
# delete <br> or |
# whichever comes after the Name, check for both

import os
import json
import mwparserfromhell as mw
import re
from bs4 import BeautifulSoup


INPUT_FILE = "json_formatted.json"

def name_parse(name: str):
    
#doesnt work properly (check: wooden staff)
    name_split = []
    if "|" in name:
        name_split = name.split("|", 1)
        name = ""
        if "id=" in name_split[0] or "data-sort-value=" in name_split[0]:
            name_split[0] = ""


# formats to remove
# {{c|Name}}
# {{cName}}
# {{tooltip|Name|get rid of this}}
# can be nested (drop of ichor) {{tooltip|Name{{c|info I want to keep}}|trash everything to the right of this}}

# remove {{c and {{c| replace with a " " DO THIS FIRST BECAUSE NESTED {{}}
# if either of those, remove }}
# remove {{tooltip| (not case sensitive)



    # if "{{tooltip|" in name:
    #     name = name.split("{{tooltip|", 1)[1]
    # if "<br>" in name:
    #     name = name.split("<br>",1)[0]
    # if "|" in name:
    #     name = name.split("|",1)[0]

    testStr = ""
    for part in name_split:
        part = part.strip()
        soup = BeautifulSoup(part, "html.parser")
        testStr = soup.get_text()
        name += testStr

    wikicode = mw.parse(name)

    for template in wikicode.filter_templates(recursive=False):
        kept = []

        for param in template.params:
            value = param.value.strip()
            if value:
                kept.append(str(value))

        wikicode.replace(template, " ".join(kept))


    return str(wikicode)

def chapter_parse(chapter: str):
    return chapter

def status_parse(status: str):
    return status

def desc_parse(desc: str):
    return desc


def main():
    if os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # os.remove(INPUT_FILE)
        os.remove("text.txt")
        with open("text.txt", "a") as f:
            for page in data:
                for page_name, items in page.items():
                    for item in items:
                        f.write(name_parse(item["Name"]) + "\n")
    else:
        print(INPUT_FILE, "not found.")



if __name__ == "__main__":
    main()

