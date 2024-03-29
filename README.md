# Earthquake Event Scraping and Data Analysis

## Overview




## Project File Structure

This repository contains scripts and data related to scraping earthquake data. Below is the structure of the project:

### Scripts
- **daily_savedown.py**
- **data_scraper_jma.py**
- **utility_functions.py**


### Data
- **quake_JMA.csv**


## Python Scripts

This section details the Python scripts included in the `Scripts` directory, outlining their purposes and functionalities.

- **daily_savedown.py**: A Python script designed to save the scraped data systematically. It is intended to be executed as a scheduled task, such as a cron job, to ensure regular data updates without manual intervention.

- **data_scraper_jma.py**: Defines functions for scraping earthquake data from the Japan Meteorological Agency (JMA). For more information on the data source, visit [JMA Website](https://www.data.jma.go.jp).

- **utility_functions.py**: Contains utility functions that are used across the project. These functions provide common functionality needed by other scripts, enhancing code reusability and maintainability.


## Data Files:

### `quake_jma.csv`

This CSV file contains earthquake data scraped from the Japan Meteorological Agency (JMA). 
For more information on the data source, visit [JMA Website](https://www.data.jma.go.jp).

#### Schema

Below is the schema of the `quake_jma.csv` file, detailing the columns and their respective data types:

| Column Name      | Data Type       |
|------------------|-----------------|
| earthquake_ID    | object          |
| magnitude        | float64         |
| source           | object          |
| location         | object          |
| time             | datetime64[ns]  |
| source_event_ID  | object          |
| longitude        | float64         |
| latitude         | float64         |
| depth            | float64         |
| link             | object          |

Each row in the `quote_jma.csv` file represents a single earthquake event, with details such as the event ID, magnitude, source, location, time, and geographical coordinates.
