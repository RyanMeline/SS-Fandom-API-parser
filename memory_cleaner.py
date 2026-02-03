# when cleaning names
# id=\nStuff\n|{{tooltop|Stuff<br>}}
# Save after |
# delete {{tooltop|
# delete <br> or |
# whichever comes after the Name, check for both

import os
import json
import mwparserfromhell
import re


INPUT_FILE = "json_formatted.json"

def name_parse(name: str):
    
#doesnt work properly (check: wooden staff)

    if "|" in name:
        name = name.split("|", 1)[1]
    if "{{tooltip|" in name:
        name = name.split("{{tooltip|", 1)[1]
    if "<br>" in name:
        name = name.split("<br>",1)[0]
    if "|" in name:
        name = name.split("|",1)[0]

    return name

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

        for page in data:
            for page_name, items in page.items():
                for item in items:
                    print(name_parse(item["Name"]))
    else:
        print(INPUT_FILE, "not found.")



if __name__ == "__main__":
    main()

