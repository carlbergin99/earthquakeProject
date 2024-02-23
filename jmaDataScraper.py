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
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    print(soup)


ParseQuakeHomeJMA(JMA_URL)
