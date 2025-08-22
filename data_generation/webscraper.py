# here the data is getting scraped
# imports
import requests
import time

from datetime import datetime

import pandas as pd

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

def webscraper():
    # this function will get the data from kicker.de
    # as of 14.07.2025 kicker.de/robots.txt does not disallow www.kicker.de/bundesliga/tabelle
    print("started webscraping")

    # get date strings
    today = datetime.today().strftime('%Y')

    lst_below_2000 = list(range(1995,2000))
    lst_below_2010 =  list(range(2000,2010))
    lst_rest = list(range(2010, int(today) + 2))

    lst_below_2000 = [str(item) for item in lst_below_2000] + ["00"]
    lst_below_2010 = ["0" + str(item) for item in lst_below_2010]
    lst_rest = [str(item) for item in lst_rest]

    lst_dates = lst_below_2000 + lst_below_2010 + lst_rest

    # get dicts for dfs
    dct_placing = {}
    dct_results = {}

    for i in range(1, len(lst_dates)):
        for j in range(1,35):
            print(f"{lst_dates[i-1]}-{lst_dates[i][2:]}/{j}" )

            date = f"{lst_dates[i-1]}-{lst_dates[i][2:]}/{j}"

            df_return_placing, df_return_results = get_match_day_data(date)

            dct_placing[date] = df_return_placing
            dct_placing[date] = df_return_results

    with open('dct_placing.pkl', 'wb') as f:  # open a text file
        pickle.dump(dct_placing, f)

    with open('dct_results.pkl', 'wb') as f:  # open a text file
        pickle.dump(dct_results, f)

    return dct_placing, dct_results


def get_match_day_data(date):
    #response = requests.get(f'http://www.kicker.de')
    options = Options()

    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    # Load the URL
    url = f"https://www.kicker.de/bundesliga/tabelle/{date}"
    driver.get(url)

    time.sleep(5)

    # click the banner
    driver.find_element('xpath', '/html/body/div[1]/div[2]/div/div/div/div/div/div[3]/div[1]/div/a').click()

    # get soup object and extract data
    html_source_code = driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(html_source_code, 'html.parser')

    # quit webdriver
    driver.quit()


    # first table are the placings, second table are the match day results
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

    df_return_placing = pd.DataFrame(lst_dct)

    # results
    # first table are the placings, second table are the match day results
    results = soup.find_all(attrs={"class": "kick__v100-gameCell kick__v100-gameCell--standard"})

    lst_dct =[]
    for match in results:
        teams = match.find_all(attrs={"class": "kick__v100-gameCell__team__shortname"})

        team_1 = teams[0].text
        team_2 = teams[1].text

        goals_scored = match.find_all(attrs={"class": "kick__v100-scoreBoard__scoreHolder__score"})

        score_team_1 = int(goals_scored[0].text)
        score_team_2 = int(goals_scored[1].text)

        dct_row = {"team_1": team_1, "team_2":team_2, "score_team_1": score_team_1, "score_team_2": score_team_2}
        lst_dct.append(dct_row)

    df_return_results = pd.DataFrame(lst_dct)

    # get wins, losses and ties here
    lst_wlt_team1 = []
    lst_wlt_team2 = []

    for nr, row in df_return_results.iterrows():
        score_team_1 = row["score_team_1"]
        score_team_2 = row["score_team_2"]

        if score_team_1 > score_team_2:
            lst_wlt_team1.append(1)
            lst_wlt_team2.append(-1)
        elif score_team_1 < score_team_2:
            lst_wlt_team1.append(-1)
            lst_wlt_team2.append(1)
        else:
            lst_wlt_team1.append(0)
            lst_wlt_team2.append(0)

    df_return_results["outcome_team_1"] = lst_wlt_team1
    df_return_results["outcome_team_2"] = lst_wlt_team2

    return df_return_placing, df_return_results







