import pandas as pd
import os

def save_df_as_csv(df, filename, uid):
    """
    Save a DataFrame to a CSV file, appending new rows and avoiding duplicates based on UIDs.

    Parameters:
    - df: pd.DataFrame, the new data to append.
    - filename: str, the name of the CSV file.
    - uid: str, the name of the column containing unique identifiers.
    """

    logging.info(f"Saving down to file: {filename}")
    # Check if the file exists
    if os.path.exists(filename):
        logging.info(f"File {filename} exists, reading in file and filtering duplicates")
        # Read existing data
        csv_data = pd.read_csv(filename)

        # Extract existing UIDs
        csv_ids = csv_data[uid].unique()

        # Log information about duplicates if any
        duplicates = df[df[uid].isin(csv_ids)]
        if not duplicates.empty:
            logging.info(f"Removing {len(duplicates)} duplicate row(s) based on '{uid}'.")

        # Filter out duplicates from data frame before saving
        df_filtered = df[~df[uid].isin(csv_ids)]
    else:
        df_filtered = df

    if not df_filtered.empty:
        # Append new data to the file (create file if it doesn't exist)
        df_filtered.to_csv(filename, mode='a', header=not os.path.exists(filename), index=False)
    else:
        logging.info("No new rows were appended.")