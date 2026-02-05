import os
import json
import mwparserfromhell as mw
import re
from bs4 import BeautifulSoup

INPUT_FILE = "json_formatted.json"
OUTPUT_FILE = "memories_echoes_shadows.json"

def name_parse(name: str):
# For stripping leading id and data sort values
    name_split = []
    if "|" in name and "id=" in name or "data-sort-value=" in name:
        name_split = name.split("|", 1)
        name = ""
        if "id=" in name_split[0] or "data-sort-value=" in name_split[0]:
            name_split[0] = ""

# HTML STRIPPER
    for part in name_split:
        part = part.strip()
        soup = BeautifulSoup(part, "html.parser")
        name += soup.get_text()

# Stripping Templates and extra, unneeded data
    wikicode = mw.parse(name)
    for template in reversed(wikicode.filter_templates(recursive=True)): #undo from the inside out
        try:
            val = "" + str(template.get(1).value).strip()
        except ValueError:
            val = ""
        
        if template.name.strip().lower() == "c":
            val = " | " + val # for formatting / style lol. all the {{c| were bonus info, so separating them with a |
        wikicode.replace(template,val)

    return wikicode.strip_code().strip()

def chapter_parse(chapter: str):
    # do the check for id= and data-sort before a | and remove it
    # replace <br> with ", "
    # templace shananigans, can probably copy a lot from the names

    # can copy a lot (most) code from name_parse
    chapter_split = []
    if "|" in chapter and "id=" in chapter or "data-sort-value=" in chapter:
        chapter_split = chapter.split("|", 1)
        chapter = " "
        if "id=" in chapter_split[0] or "data-sort-value=" in chapter_split[0]:
            chapter_split[0] = " "

    chapter = chapter.replace("<br>", " | ")

    wikicode = mw.parse(chapter)
    for template in reversed(wikicode.filter_templates(recursive=True)): #undo from the inside out
        try:
            val = " " + str(template.get(1).value).strip()
        except ValueError:
            val = " "
        
        if template.name.strip().lower() == "c":
            val = " | " + val
        wikicode.replace(template,val)

    # strip [[ ]] from these
    return wikicode.strip_code().strip() 

def status_parse(status: str):
    status = re.sub("<(.*?)>", " ", status)
#    status = BeautifulSoup(status, "html.parser").get_text()

    wikicode = mw.parse(status)
    for template in reversed(wikicode.filter_templates(recursive=True)): #undo from the inside out
        try:
            val = " " + str(template.get(1).value).strip()
        except ValueError:
            val = " "
        
        if template.name.strip().lower() == "c":
            val = "|" + val
        wikicode.replace(template,val)
    return wikicode.strip_code().strip()

def desc_parse(desc):
    # Strip HTML
    desc = re.sub("<(.*?)>", " ", desc)

    # Strip templates
    wikicode = mw.parse(desc)
    for template in reversed(wikicode.filter_templates(recursive=True)): #undo from the inside out
        val = ""
        if template.name.strip().lower() == "c" or template.name.strip().lower() == "note":
            try:
                val = str(template.get(1).value)
            except ValueError:
                val = ""
        if template.name.strip().lower() == "scrollbox":
            try:
                val = (str(template.get("content").value))
            except ValueError:
                val = ""
        wikicode.replace(template,val)
    
    # Some random triple newlines, reduce anything 2 newlines or more down to 2 newlines    newline [anynumber of spaces, newlines]+  [ ]*\\n[[ ]*\\n]+
    wikicode = re.sub(r"[ ]*\n[ \n]+", "\\n\\n", str(wikicode))
    return wikicode.strip()


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)


    # set to ademndum mode, change to write once json structures are built (in ademndum bc adding in a loop, can add json all at once)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for page in data:
            for page_name, items in page.items():
                for item in items:
                    item["Name"] = name_parse(item["Name"])
                    
                    # inconsistant naming convention caused this
                    # can fix by making new json objects
                    # not doing that rn

                    if "Chapter Received" in item:
                        item["Chapter Received"] = chapter_parse(item["Chapter Received"])
                    elif "Chapter Appeared" in item:
                        item["Chapter Appeared"] = chapter_parse(item["Chapter Appeared"])    
                    else:
                        item["Chapter"] = chapter_parse(item["Chapter"])

                    if "Status" in item:
                        item["Status"] = status_parse(item["Status"])

                    if "Details" in item:
                        item["Details"] = desc_parse(item["Details"])
                    else:
                        item["Description"] = desc_parse(item["Description"])
        json.dump(data, f, ensure_ascii=False, indent = 2)
        os.remove(INPUT_FILE)

if __name__ == "__main__":
    main()

