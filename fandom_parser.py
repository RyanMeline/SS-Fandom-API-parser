#Turn unstructured data dump from wiki into structured json
import json
import mwparserfromhell as mw
import re
import os

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
    current_column = 0 # current column
    rowspan_count = 0 # if its above 0, then in rowspan
    rowspan_contents = "" # store what was said in the rowspan
    rowspan_col = 0 # stores which column the rowspan was on

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
        current_column += 1 # on a new column, so inc
        if line.startswith("|-"):
            div_count = 0
            current_column = 0
            if current_row:
                rows.append(current_row)
                current_row = []
            continue
            
        if rowspan_count > 0 and rowspan_col == current_column: # if we inside a rowspan
            print(rowspan_contents)
            current_row.append(rowspan_contents)
            current_column += 1
            rowspan_count -= 1


        if line.startswith("|") and div_count == 0:

            if "rowspan=" in line:
                rowspan_loc = line.find("rowspan=")
                rowspan_count = int(line[rowspan_loc + 9])-1 # has rowspan num
                rowspan_contents = line[1:] #cuts the | off the front
                rowspan_col = current_column

            current_column += 1
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
    
def make_json_obj(headers, rows):
    objs = []
    for row in rows:
        row_fixed = (row + [""] * len(headers))[:len(headers)]
        objs.append(dict(zip(headers, row_fixed)))
    return objs

def make_json_page(page_title, json_objs):
    return {page_title: json_objs}



def main():
    if os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        os.remove(INPUT_FILE)

        pages = []

        for page_title, page_info in data.items():
            wiki_text = page_info.get("content", "")

            results = re.findall(r"\{\|(.*?)\|\}", wiki_text, re.DOTALL)
            
            # titles = re.findall(r"==(.*?)==", wiki_text, re.DOTALL)
            # if I want to do something with the titles

            tables = []
            for text in results:
                if "table" in text:
                    tables.append(text)
            
            json_objs = []

            for table in tables:
                headers, rows = parse_table(table)
                json_objs.extend(make_json_obj(headers, rows))
            
            pages.append(make_json_page(page_title, json_objs))


        with open (OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(pages, f, indent=2, ensure_ascii=False)
    else:
        print(INPUT_FILE, "not found.")

if __name__ == "__main__":
    main()
