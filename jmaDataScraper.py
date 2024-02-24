# Script to scrape data from JMA (Japan Meteorological Agency) website https://www.data.jma.go.jp

import requests
import os
import json
from chromedriver_py import binary_path
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.service import Service

JMA_URL = "https://www.data.jma.go.jp/multi/quake/index.html?lang=en"


def ParseQuakeHomeJMA(url):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(executable_path=binary_path), options=options)

    try:
        # Open the webpage
        driver.get(url)  # Replace with the actual URL

        # Wait for the dynamic content to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'quakeindex_table')))

        table = driver.find_element(By.ID, 'quakeindex_table')
        print(table)
        rows = table.find_elements(By.TAG_NAME, 'tr')
        print(rows)

        data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')  # or 'th' if you're extracting headers
            data.append([col.text for col in cols])

        driver.quit()

        # Convert list of lists to DataFrame
        df = pd.DataFrame(data)
        print(df)

        # If the first row contains your headers
        df.columns = df.iloc[0]  # Set the first row as header
        df = df[1:]  # Remove the first row from the data

    except Exception as e:
        logging.warning(f"Unable to find table html from url {url}: {e}")
        return ""


#ParseQuakeHomeJMA(JMA_URL)

url="https://www.data.jma.go.jp/multi/quake/index.html?lang=en"

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(executable_path=binary_path), options=options)


# Open the webpage
driver.get(url)  # Replace with the actual URL

# Wait for the dynamic content to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'quakeindex_table')))

table = driver.find_element(By.ID, 'quakeindex_table')
print(table)
rows = table.find_elements(By.TAG_NAME, 'tr')
print(rows)

data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, 'td')  # or 'th' if you're extracting headers
    data.append([col.text for col in cols])

#driver.quit()

# Convert list of lists to DataFrame
df = pd.DataFrame(data)
print(df)

# If the first row contains your headers
df.columns = df.iloc[0]  # Set the first row as header
df = df[1:]  # Remove the first row from the data