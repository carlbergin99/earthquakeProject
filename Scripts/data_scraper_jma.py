# Script to scrape data from JMA (Japan Meteorological Agency) website https://www.data.jma.go.jp

# General libraries
import pandas as pd
import logging
import sys
import time

# Chrome driver libraries
from selenium.webdriver.common.by import By
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.service import Service

# Custom scripts
from utility_functions import dataframe_preview, generate_earthquake_uid, convert_coord, convert_depth_to_float


def parse_quake_home_jma(url):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(executable_path=binary_path), options=options)

    try:
        # Open the webpage
        driver.get(url)

        # Wait for the webpage contents to load
        time.sleep(2)

        # Find the table by its ID
        quake_table = driver.find_element(By.ID, 'quakeindex_table')

        # Find all rows in the table
        rows = quake_table.find_elements(By.TAG_NAME, 'tr')

        links = []
        for row in rows:
            # Attempt to find a link within the row
            try:
                link = row.find_element(By.CSS_SELECTOR, 'td > a').get_attribute('href')
            except Exception:
                # If no link is found, use None or an empty string
                link = None
            links.append(link)

        # Extract the table HTML
        table_html = quake_table.get_attribute('outerHTML')

        # Close the WebDriver
        driver.quit()

        # Use pandas to read the HTML table data
        df = pd.read_html(table_html)[0]

        # If the first row is headers, adjust accordingly
        if df.shape[0] == len(rows) - 1:
            links = links[1:]  # Adjust if the first row of links is header and should be skipped

        # Assign links to DataFrame, ensuring alignment with rows
        df['Link'] = links

        return df

    except Exception as e:
        logging.warning(f"Unable to find table html from url {url}: {e}")
        driver.quit()  # Ensure the driver quits in case of an exception
        return None


def add_quake_detail_jma(df):
    # Check if the 'Link' column exists in the DataFrame
    if 'Link' in df.columns:
        quake_detail_df = pd.DataFrame()

        for index, row in df.iterrows():
            link = row['Link']
            if link is not None:
                df_per_row = get_quake_detail(link)

                if df is not None:
                    quake_detail_df = pd.concat([quake_detail_df, df_per_row], ignore_index=True)

        # Join quake detail with the main df
        df = pd.merge(df, quake_detail_df, how='left',
                      on=['Observed at', 'Magnitude', 'Place name of epicenter', 'Link'])

        return df

    else:
        logging.error("No 'Link' column found in the DataFrame.")
        return df


def get_quake_detail(url):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(executable_path=binary_path), options=options)

    try:
        # Open the webpage
        driver.get(url)

        # Wait for the webpage contents to load
        time.sleep(2)

        # Find the table by its ID
        quake_table = driver.find_element(By.ID, 'quakeindex_table')

        # Extract the table HTML
        table_html = quake_table.get_attribute('outerHTML')

        # Close the WebDriver
        driver.quit()

        # Use pandas to read the HTML table data
        df = pd.read_html(table_html)[0]

        # Add link for joining to original df
        df['Link'] = url

        return df

    except Exception as e:
        logging.warning(f"Unable to find table html from url {url}: {e}")
        driver.quit()  # Ensure the driver quits in case of an exception
        return None


def get_data_jma(url):
    logging.info(f"Running getJMA data for url: " + url)

    # Get general earthquake information
    df = parse_quake_home_jma(url)
    if df is not None:
        if len(df) > 1:
            logging.info(f"Successfully ran parse quake_home_JMA" + dataframe_preview(df))
        else:
            logging.warning(f"Empty data frame returned from parse quake_home_JMA, exiting...")
            sys.exit(0)
    else:
        logging.error(f"Failed to ran parse quake_home_JMA, exiting...")
        sys.exit(1)

    # TODO PLEASE REMOVE AFTER TESTING
    df = df.head(3)

    # Add extra detail using link column
    df = add_quake_detail_jma(df)

    # Standardize column names and formatting

    cols_to_keep = {
        'Observed at': 'time',
        'Place name of epicenter': 'location',
        'Magnitude': 'magnitude',
        'Link': 'link',
        'Latitude': 'latitude',
        'Longitude': 'longitude',
        'Epicenter depth': 'depth'
    }

    # Renaming columns
    df = df[list(cols_to_keep.keys())].rename(columns=cols_to_keep)

    # Fix types
    df['time'] = pd.to_datetime(df['time'])
    df['magnitude'] = df['magnitude'].astype(float)

    # Convert depth to float
    df['depth'] = df['depth'].apply(convert_depth_to_float)

    # Apply the conversion function to latitude and longitude columns
    df['latitude'] = df['latitude'].apply(convert_coord)
    df['longitude'] = df['longitude'].apply(convert_coord)

    # Add unique id earthquake_id to df
    df['source'] = "JMA"
    df['source_event_ID'] = ""
    df['earthquake_ID'] = df.apply(generate_earthquake_uid, axis=1)

    # Reorder table
    df_order = ['earthquake_ID',  'magnitude',  'source', 'location', 'time',
                'source_event_ID', 'longitude', 'latitude', 'depth', 'link']

    df = df[df_order]

    logging.info(f"Successfully ran parse get_data_JMA" + dataframe_preview(df))

    return df


# JMA Website URL
jma_url = "https://www.data.jma.go.jp/multi/quake/index.html?lang=en"
test = get_data_jma(jma_url)
