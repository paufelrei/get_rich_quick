# in this file the function imported in the main file is defined
# imports
from data_generation.webscraper import webscraper

def data_gen():
    print("start data generation")

    # if necessary start webscraping
    webscraper()

