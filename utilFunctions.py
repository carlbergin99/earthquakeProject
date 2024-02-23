# Utility Functions for Project

########## Logging Functions ##########
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def dataframe_preview(df, num_rows=5):
    preview = (
        f"DataFrame Shape: {df.shape}\n"
        f"DataFrame Columns: {df.columns.tolist()}\n"
        f"First {num_rows} rows:\n{df.head(num_rows)}"
    )
    return preview
