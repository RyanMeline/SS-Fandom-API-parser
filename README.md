Fandom Wiki Parser Specifically for the Shadow Slave Fandom Site

At the moment: <br>
Designed to parse tables and put the results into a structured json file.



ingestion.py - Imports info dump from Shadow Slave's Fandom site
<br>
fandom_parser.py - Parse json dump and structure it
<br>
memory_cleaner.py - Cut out HTML and MediaWiki formatting to clean results for easier searching/reading

Using:
<br>
mwparserfromhell | MediaWiki parser
<br>
BeatifulSoup4 | HTML parser

<br>
<h3>TODO:</h3>
<ul>
    <li>Fix JSON parsing</li>
    <li>Export JSON to .csv</li>
</ul>
