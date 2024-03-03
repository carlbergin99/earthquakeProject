# Utility Functions for Project

import logging
import re
import os


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


def generate_earthquake_uid(row):
    """
    Generate a unique identifier for an earthquake event from a DataFrame row.

    Assumes DataFrame columns for timestamp, magnitude, latitude, longitude, and source exist.
    Formats latitude and longitude to 1 decimal place.
    """
    time = row['time'].strftime('%Y%m%d%H%M%S')  # Assuming timestamp is in a datetime format
    magnitude = row['magnitude']
    latitude = f"{row['latitude']:.1f}"
    longitude = f"{row['longitude']:.1f}"
    source = row['source']

    uid = f"{time}_{magnitude}_{latitude}_{longitude}_{source}"
    return uid


# Define a function to convert the string to float and adjust the sign based on direction
def convert_coord(coord):
    # Check the last character for the direction
    direction = coord[-1]
    # Convert the numeric part to float
    numeric_value = float(coord[:-1])
    # Adjust the sign based on the direction
    if direction in ['S', 'W']:
        numeric_value *= -1
    return numeric_value


def convert_depth_to_float(depth_input):
    """
    Convert a depth input (string e.g., '50km', '100.5km' or float) to a float (e.g., 50.0, 100.5).
    This version checks the input type and uses regular expressions to extract the numeric part if it is a string.
    """
    # If the input is already a float, return it directly
    if isinstance(depth_input, float):
        return depth_input
    elif isinstance(depth_input, str):
        # Use regular expression to find all numeric characters and decimal points in a string
        numeric_part_match = re.search(r"[-+]?[0-9]*\.?[0-9]+", depth_input)

        if numeric_part_match:
            numeric_part = numeric_part_match.group()
            depth_float = float(numeric_part)
            return depth_float
        else:
            # Return None or raise an error if no numeric part is found
            return None
    else:
        # Handle other types, e.g., int or unexpected types
        try:
            # Attempt to convert to float directly
            return float(depth_input)
        except ValueError:
            # If conversion fails, return None or handle the error as appropriate
            return None


def read_list_from_txt(file_name):
    try:
        with open(file_name, 'r') as file:
            # Read all lines from the file and strip newline characters
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []
