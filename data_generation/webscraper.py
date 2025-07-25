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

    lst_dct = []

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

            dct_row = {"name": a[3],"placement": int(a[0]), "matches": int(a[4]), "draws":int(a[6]), "losses":int(a[7]),
                       "goals_diff":int(a[9]), "points": int(a[10])}

            wins = dct_row["matches"] - dct_row["draws"] - dct_row["losses"]

            dct_row["wins"] = wins

            goals = a[8].split(':')

            dct_row["goals_shot"] = goals[0]
            dct_row["goals_received"] = goals[1]



            lst_dct.append(dct_row)

    df_return = pd.DataFrame(lst_dct)

    return df_return





