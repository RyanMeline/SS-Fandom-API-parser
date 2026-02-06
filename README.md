# Wiki Table Data Extraction & Parsing Tool

## Overview
This is a Python-based tool that downloads pages from a Fandom (MediaWiki) wiki,
parses inconsistent wiki markup and embedded HTML, and converts the content of stored tables
into structured, searchable JSON data.

It is built to handle irregular formatting that stems from inconsistent naming conventions
and structure commonly found in community wikis

## Features
- Downloads wiki pages via the MediaWiki (Fandom) API
- Saves raw page content locally in JSON format
- Parses MediaWiki markup using `mwparserfromhell`
- Extracts and cleans HTML using `BeautifulSoup`
- Uses regex-based processing for edge cases and irregular formatting
- Normalizes data into structured JSON objects
- Includes a basic keyword search script for querying parsed content

## Project Structure
- `download_pages.py` – Fetches pages from the Fandom (MediaWiki) API and stores raw content as JSON
- `fandom_parser.py` – Parses wiki markup and embedded HTML to separate tables into semi-structured data
- `json_cleaner.py` – Parses json structure to clean results of HTML and wiki markup 
   *(Specifically designed for the Shadow Slave wiki due to inconsistent and unconventional logic)
- `search.py` – Provides basic keyword search over parsed results

## Tech Stack
- Python
- MediaWiki / Fandom API
- mwparserfromhell
- BeautifulSoup4
- re (regex)
- JSON

## How It Works
1. Pages are fetched from the wiki API and saved locally
2. Raw wiki markup is parsed and table data is extracted
3. Data is serialized into structured JSON objects
4. Embedded HTML is cleaned or removed
5. Inconsistent formatting is normalized through custom parsing logic
6. A search script allows querying across parsed pages

## Usage
1. Install dependencies
2. Run the download script
3. The download script automatically runs the parsing and cleaning scripts
4. Use the search script to query results

## Limitations
- Parsing logic is tailored to a specific wiki's formatting conventions
- Limited to extracting and formatting information stored in tables
- Not intended to be a universal MediaWiki parser
- Search functionality is intentionally limited

## Future Improvements
- Generalize for multiple wikis
- Add indexing for faster search
- Export to CSV or database formats
- Improve error handling and logging
- Add some sort of fuzzy finding to search descriptions
- Create a GUI to search parsed data
- Implement a search function in a discord bot using discord.py, as well as sqlite, to allow for community use (interest has been shown)
