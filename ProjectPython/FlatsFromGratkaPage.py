import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import bs4
import re

def parse_flats_from_gratka(number_of_pages, city):
    links = []
    locations = []
    titles = []
    areas = []
    rooms = []
    floors = []
    dates = []
    prices = []
    addPrices = []

    for i in range(1, number_of_pages):
        url = "https://gratka.pl/nieruchomosci/mieszkania/{}?page={}".format(city, i)
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')

        for flat in soup.findAll("article", {"class": "teaserEstate"}):

            flat_article_photo = flat.findAll("div", {"class": "teaserEstate__photo"})[0]
            flat_link = flat_article_photo.findAll('a', href=True)[0]['href']

            flat_article_mainInfo = flat.findAll("div", {"class": "teaserEstate__mainInfo"})[0]
            flat_location = flat_article_mainInfo.findAll("span", {"class": "teaserEstate__location"})[0].text.replace(
                ' ', '')

            flat_title_class = flat_article_mainInfo.findAll("h2", {"class": "teaserEstate__title"})[0]
            flat_title = flat_title_class.findAll('a')[0].text

            flat_params = flat_article_mainInfo.findAll("ul", {"class": "teaserEstate__offerParams"})[0].findAll('li')
            if len(flat_params) != 3:
                continue
            flat_area = float(flat_params[0].text.replace(",", ".")[:-3])
            flat_rooms = flat_params[1].text
            flat_floor = flat_params[2].text

            flat_date = \
            flat_article_mainInfo.findAll("ul", {"class": "teaserEstate__details"})[0].findAll('li')[0].text.split()[1]

            flat_article_aside = \
            flat.findAll("div", {"class": "teaserEstate__aside"})[0].findAll("p", {"class": "teaserEstate__price"})[0]
            flat_price = int(flat_article_aside.text.strip().split('\n')[0].replace(" ", "")[:-2])
            flat_additional_price = int(
                flat_article_aside.findAll('span', {"class": "teaserEstate__additionalPrice"})[0].text.strip().replace(
                    " ", "")[:-5])

            links.append(flat_link)
            locations.append(flat_location.strip())
            titles.append(flat_title)
            areas.append(flat_area)
            rooms.append(flat_rooms)
            floors.append(flat_floor)
            dates.append(flat_date)
            prices.append(flat_price)
            addPrices.append(flat_additional_price)

    df_flats = pd.DataFrame(
        {'title': titles, 'location': locations, 'area': areas, 'rooms': rooms, 'floor': floors, 'price': prices,
         'additionalPrice': addPrices, 'date': dates, 'link': links})
    return df_flats


def parse_houses_from_gratka(number_of_pages, city):
    links = []
    locations = []
    titles = []
    areas = []
    rooms = []
    dates = []
    prices = []
    addPrices = []

    for i in range(1, number_of_pages):
        url = "https://gratka.pl/nieruchomosci/domy/{}?page={}".format(city, i)
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        for house in soup.findAll("article", {"class": "teaserEstate"}):

            house_article_photo = house.findAll("div", {"class": "teaserEstate__photo"})[0]
            house_link = house_article_photo.findAll('a', href=True)[0]['href']

            house_article_mainInfo = house.findAll("div", {"class": "teaserEstate__mainInfo"})[0]
            house_location = house_article_mainInfo.findAll("span", {"class": "teaserEstate__location"})[
                0].text.replace(' ', '')

            house_title_class = house_article_mainInfo.findAll("h2", {"class": "teaserEstate__title"})[0]
            house_title = house_title_class.findAll('a')[0].text

            house_params = house_article_mainInfo.findAll("ul", {"class": "teaserEstate__offerParams"})[0].findAll('li')
            if len(house_params) != 2:
                continue
            house_area = float(re.findall(r'\d+', re.sub(r'\s+', "", house_params[0].text.replace(",", ".")))[0])
            house_rooms = house_params[1].text

            house_date = \
            house_article_mainInfo.findAll("ul", {"class": "teaserEstate__details"})[0].findAll('li')[0].text.split()[1]

            house_article_aside = \
            house.findAll("div", {"class": "teaserEstate__aside"})[0].findAll("p", {"class": "teaserEstate__price"})[0]
            house_price = int(house_article_aside.text.strip().split('\n')[0].replace(" ", "")[:-2])
            house_additional_price = int(
                house_article_aside.findAll('span', {"class": "teaserEstate__additionalPrice"})[0].text.strip().replace(
                    " ", "")[:-5])

            links.append(house_link)
            locations.append(house_location.strip())
            titles.append(house_title)
            areas.append(house_area)
            rooms.append(house_rooms)
            dates.append(house_date)
            prices.append(house_price)
            addPrices.append(house_additional_price)

    df_flats = pd.DataFrame({'title': titles, 'location': locations, 'area': areas, 'rooms': rooms, 'price': prices,
                             'additionalPrice': addPrices, 'date': dates, 'link': links})
    return df_flats

def plot_houses_from_gratka_depends_on_data(houses_from_gratka):
    houses_from_gratka['date'] = pd.to_datetime(houses_from_gratka['date'], format='%d.%m.%Y')
    houses_from_gratka = houses_from_gratka.sort_values(by=['date'])
    fig = plt.figure()
    plt.scatter(houses_from_gratka.date, houses_from_gratka.additionalPrice)
    fig.set_size_inches(15, 6)
    plt.xticks(rotation=45)
    plt.title('DOMY - Cena (zł) za m^2 w zależności od daty');
    plt.show()

def plot_houses_from_gratka_depends_on_area(houses_from_gratka):
    houses_from_gratka['date'] = pd.to_datetime(houses_from_gratka['date'], format='%d.%m.%Y')
    houses_from_gratka = houses_from_gratka.sort_values(by=['date'])
    fig = plt.figure()
    plt.scatter(houses_from_gratka.area, houses_from_gratka.additionalPrice)
    fig.set_size_inches(15, 6)
    plt.xticks(rotation=90)
    plt.xticks(np.arange(houses_from_gratka['area'].min(), houses_from_gratka['area'].max() + 1, 100.0))
    plt.title('DOMY - Cena (zł) za m^2 w zależności od powierzchni');
    plt.show()



def plot_flats_from_gratka_depends_on_data(flats_from_gratka):
    flats_from_gratka['date'] = pd.to_datetime(flats_from_gratka['date'], format='%d.%m.%Y')
    flats_from_gratka = flats_from_gratka.sort_values(by=['date'])
    fig = plt.figure()
    plt.scatter(flats_from_gratka.date, flats_from_gratka.additionalPrice)
    fig.set_size_inches(15, 6)
    plt.xticks(rotation=45)
    plt.title('MIESZKANIA - Cena (zł) za m^2 w zależności od daty');
    plt.show()

def plot_flats_from_gratka_depends_on_area(flats_from_gratka):
    flats_from_gratka['date'] = pd.to_datetime(flats_from_gratka['date'], format='%d.%m.%Y')
    flats_from_gratka = flats_from_gratka.sort_values(by=['date'])
    fig = plt.figure()
    plt.scatter(flats_from_gratka.area, flats_from_gratka.additionalPrice)
    fig.set_size_inches(15, 6)
    plt.xticks(rotation=45)
    plt.xticks(np.arange(round(flats_from_gratka['area'].min(), 0), flats_from_gratka['area'].max() + 1, 50.0))
    plt.title('MIESZKANIA - Cena (zł) za m^2 w zależności od powierzchni');
    plt.show()



