import pandas as pd
import os
import logging

# Custom scripts
from utility_functions import dataframe_preview
from data_scraper_jma import get_data_jma


def save_df_as_csv(df, filename):
    """
    Save a DataFrame to a CSV file, appending new rows and avoiding duplicates based on UIDs.

    Parameters:
    - df: pd.DataFrame, the new data to append.
    - filename: str, the name of the CSV file.
    """

    logging.info(f"Saving down to file: {filename}")

    if 0 < len(df):
        # Append new data to the file (create file if it doesn't exist)
        df.to_csv(filename, mode='a', header=not os.path.exists(filename), index=False)
        logging.info(f"Save down for file {filename} success: {len(df)} rows were saved down")
    else:
        logging.info("No new rows were appended.")


def save_list_to_file(list_to_save, filename):
    """
    Saves a list to a text file. Appends to the file if it already exists.

    Parameters:
    - list_to_save: List of items to be saved.
    - filename: The name of the file (with path) where the list will be saved.
    """
    # Open the file in append mode ('a'). If the file doesn't exist, it will be created.
    with open(filename, 'a') as file:
        for item in list_to_save:
            # Write each item on a new line
            file.write(f"{item}\n")


# Database directory
save_dir = "C:\\Users\\carlb\\PycharmProjects\\earthquakeProject\\Data Files\\"

# JMA Website URL
jma_url = "https://www.data.jma.go.jp/multi/quake/index.html?lang=en"
jma_file_name = "quake_jma.csv"
jma_save_dir = save_dir + jma_file_name
jma_uid_file = "jma_uid.txt"
jma_uid_dir = save_dir + jma_uid_file

# Get data from JMA
logging.info(f"Scraping earthquake data from JMA {jma_url}")
jma_df = get_data_jma(jma_url, jma_uid_dir)

if 0 < len(jma_df):
    # Save down unique Links as txt file to avoid duplicates
    save_list_to_file(jma_df['link'].tolist(), jma_uid_dir)

    # Save down JMA data
    save_df_as_csv(jma_df, jma_save_dir)
else:
    logging.info("No data to save down.")

