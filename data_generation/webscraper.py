# here the data is getting scraped
# imports
import requests
import time

import pandas as pd

from selenium import webdriver
from bs4 import BeautifulSoup

def webscraper():
    # this function will get the data from kicker.de
    # as of 14.07.2025 kicker.de/robots.txt does not disallow www.kicker.de/bundesliga/tabelle
    print("started webscraping")
    date = "2022-23/3"

    get_table(date)



def get_table(date):
    #response = requests.get(f'http://www.kicker.de')

    driver = webdriver.Firefox()

    # Load the URL
    url = f"https://www.kicker.de/bundesliga/tabelle/2022-23/3"
    driver.get(url)

    time.sleep(3)

    # click the banner
    driver.find_element('xpath', '/html/body/div[1]/div[2]/div/div/div/div/div/div[3]/div[1]/div/a').click()

    # get soup object and extract data
    html_source_code = driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(html_source_code, 'html.parser')

    table = soup.find_all('table')[0]

    for row in table.findAll("tr"):
        cell = row.findAll("td")
        str_cells = str(cell )
        clean_text = BeautifulSoup(str_cells, "lxml").get_text()

        clean_text = clean_text.replace("\n" , '')

        if len(clean_text) > 2:
            a = []
            # Loop through each item in the split string
            for item in clean_text.split(','):
                item = item.replace("[", "")
                item = item.replace("]", "")
                a.append(item.strip())


        print("____________________________________________________________________________________________")




