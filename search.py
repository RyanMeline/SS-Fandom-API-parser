import json
import os

def print_info(page_name, item, size):
    print(page_name)
    print("-" * len(page_name))
    print("Name: " + item["Name"])
    if "Chapter Received" in item:
        print("Chapter: " + item["Chapter Received"])
    elif "Chapter Appeared" in item:
        print("Chapter: " + item["Chapter Appeared"])   
    else:
        print("Chapter: " + item["Chapter"])
    
    if "Status" in item:
        print("Status: " + item["Status"])

    if "Details" in item:
        print("Details: " + item["Details"])
    else:
        print("Description: " + item["Description"])
    print("-" * size.columns)

# For making things pretty lol
size = os.get_terminal_size()

INPUT_FILE = "memories_echoes_shadows.json"
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

#maybe add an all tag, to get all the memories, all the echos, all the characters (available), things like that
mode = input("Section: memory | echo/shadow | character | creature | region | options | all |- ").strip().lower()
loop = True

no_input = False
while 1:
    if mode == "memory" or mode == 'm':
        mode = "m"
        break
    elif mode == "echo" or mode == "shadow" or mode == 'e' or mode == 's':
        mode = "e"
        break
    elif mode == "character" or mode == 'ch':
        mode = 'ch'
        break
    elif mode == "creature" or mode == 'c':
        mode = 'c'
        break
    elif mode == "region" or mode == 'r':
        mode == 'r'
        break;
    elif mode == "options" or mode == 'o':
        mode == 'o'
        no_input = True
        break
    elif mode == "all" or mode == 'a':
        mode == 'a'
        break
    else:
        print("Please enter either \"memory\", \"echo\", \"shadow\", \"character\", \"creature\", \"region\", \"options\", \"all\"")
        mode = input("Search for memory or an echo/shadow? ").strip().lower()

if not no_input:
    name = input("Enter name: ").strip().lower()
print("-" * size.columns)

#for future use
matches = []

for pages in data:
    for page_name, page_items in pages.items(): # page_name is like Sunny/Memories and Effie/Memories

        # Memories
        if mode == 'm' and 'memories' in page_name.lower():
            for item in page_items:
                if name in item["Name"].strip().lower():
                    print_info(page_name, item, size)
        
        # Shadows or Echoes
        elif mode == 'e' and ('echo' in page_name.lower() or 'shadow' in page_name.lower()):
            for item in page_items:
                if name in item["Name"].strip().lower():
                    print_info(page_name, item, size)

        # Creatures
        elif mode == 'c' and "creature" in page_name.lower():
            for item in page_items:
                if name in item["Name"].strip().lower():
                    print_info(page_name, item, size)

        # Characters
        elif mode == 'ch' and name in page_name.lower():
            for item in page_items:
                print_info(page_name, item, size)

        # Regions (Prints all creatures in given region)
        elif mode == 'r' and name in page_name.lower():
            for item in page_items:
                print_info(page_name, item, size)

        # Options (Prints page names)
        elif mode == 'o':
            print(page_name.strip())

        # All (your search is checked against each page)
        elif mode == 'a':
            for item in page_items:
                print_info(page_name, item, size)