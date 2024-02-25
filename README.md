# earthquakeProject
Earthquake scraping and data analysis

Python Scripts:
- jmaDataScraper.py: Defines functions for scraping data scraping from JMA (Japan Meteorological Agency: https://www.data.jma.go.jp)
- utilFunctions.py: Defines utility functions used by other scripts
- dailySavedown.py: Python script to save down data - should be run as scheduled task (e.g. cronjob)

Data Files:

earthquakeJMA.csv:csv file containing earthquake data scraped from JMA (Japan Meteorological Agency: https://www.data.jma.go.jp)

