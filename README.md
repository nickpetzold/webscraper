# Webscraper

Python webscraper that scrapes a URL and creates a breakdown of all externally hosted resources on that page which is exported to a JSON file.

All hyperlinks are then scanned to find the Privacy Policy page which is then analysed to create a case insensitive word frequency dict for all visible text on that page. The result is exported to a JSON file.

## Running instructions

Install the required packages:

```
pip install -r path/to/requirements.txt
```

The script can then be run like a normal python script, passing in 1-2 arguments plus an optional flag `--valid`.

1. URL of the webpage you would like to scrape
2. [OPTIONAL] Directory in which the JSON files will be written to
3. [FLAG] Adding this flag makes the script check words found in the Privacy Policy page to ensure they are proper English (WARNING: this will slow down the script considerably).

Example:

```
python path/to/scraper.py ~/Desktop --valid
```
