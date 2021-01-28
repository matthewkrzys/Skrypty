import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import re

list_of_url = {
    'krakow': "https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/krakow/{}/page-{}/v1c9073l3200208a1dwp{}",
    'warszawa': "https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/warszawa/{}/page-{}/v1c9073l3200008p{}",
    'wroclaw': "https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/wroclaw/{}/page-{}/v1c9073l3200114a1dwp{}"}


def parse_flats_from_gumtree(number_of_page, city):
    links = []
    locations = []
    titles = []
    areas = []
    rooms = []
    dates = []
    prices = []
    add_prices = []

    for i in range(1, number_of_page):
        url = list_of_url[city].format('mieszkanie', i, i)
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        for element_of_page in soup.findAll("div", {"class": "tileV1"}):
            flat = element_of_page.findAll("a", {"class": "href-link tile-title-text"})[0]
            flat_link = "https://www.gumtree.pl" + flat['href']
            flat_title = flat.text
            category_location = element_of_page.findAll("div", {"class": "category-location"})[0]
            flat_location = category_location.findAll("span")[0].text.split(",")[1].strip()
            data = requests.get(flat_link)
            flat_soup = BeautifulSoup(data.text, 'html.parser')
            flat_params = flat_soup.findAll("ul", {"class": "selMenu"})
            flat_param_list = flat_params[0].findAll("div", {"class": "attribute"})

            flat_area = ""
            flat_rooms = ""
            for i in flat_param_list:
                if re.findall("Wielkość", str(i)):
                    flat_area = i.findAll("span", {"class": "value"})[0].text

                if re.findall("Liczba pokoi", str(i)):
                    flat_rooms = i.findAll("span", {"class": "value"})[0].text
                    if re.findall("Kawalerka lub garsoniera", str(i)):
                        flat_rooms = "1 pokój"

            if flat_area == "":
                continue
            flat_area = int(flat_area)
            flat_date = flat_param_list[0].findAll("span", {"class": "value"})[0].text
            flat_price = re.sub(r"\s+", "",
                                flat_soup.findAll("div", {"class": "price"})[0].findAll("span", {"class": "value"})[
                                    0].text[
                                :-3].strip())
            if not flat_price.isdigit():
                continue
            flat_additional_price = round(int(flat_price) / flat_area, 2)

            prices.append(flat_price)
            add_prices.append(flat_additional_price)
            links.append(flat_link)
            locations.append(flat_location.strip())
            titles.append(flat_title)
            areas.append(flat_area)
            dates.append(flat_date)
            rooms.append(flat_rooms)

    df_flats = pd.DataFrame(
        {'title': titles, 'location': locations, 'area': areas, 'rooms': rooms, 'price': prices,
         'additionalPrice': add_prices, 'date': dates, 'link': links})
    return df_flats


def parse_houses_from_gumtree(number_of_page, city):
    links = []
    locations = []
    titles = []
    areas = []
    rooms = []
    dates = []
    prices = []
    add_prices = []

    for i in range(1, number_of_page):
        url = list_of_url[city].format('dom', i, i)
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        for element_of_page in soup.findAll("div", {"class": "tileV1"}):
            flat = element_of_page.findAll("a", {"class": "href-link tile-title-text"})[0]
            flat_link = "https://www.gumtree.pl" + flat['href']
            flat_title = flat.text
            category_location = element_of_page.findAll("div", {"class": "category-location"})[0]
            flat_location = category_location.findAll("span")[0].text.split(",")[1].strip()
            data = requests.get(flat_link)
            flat_soup = BeautifulSoup(data.text, 'html.parser')
            flat_params = flat_soup.findAll("ul", {"class": "selMenu"})
            flat_param_list = flat_params[0].findAll("div", {"class": "attribute"})

            flat_area = ""
            flat_rooms = ""
            for i in flat_param_list:
                if re.findall("Wielkość", str(i)):
                    flat_area = i.findAll("span", {"class": "value"})[0].text

                if re.findall("Liczba pokoi", str(i)):
                    flat_rooms = i.findAll("span", {"class": "value"})[0].text
                    if re.findall("Kawalerka lub garsoniera", str(i)):
                        flat_rooms = "1 pokój"

            if flat_area == "":
                continue
            flat_area = int(flat_area)
            flat_date = flat_param_list[0].findAll("span", {"class": "value"})[0].text
            flat_price = re.sub(r"\s+", "",
                                flat_soup.findAll("div", {"class": "price"})[0].findAll("span", {"class": "value"})[
                                    0].text[
                                :-3].strip())
            if re.findall("Proszęokont", flat_price):
                continue
            flat_additional_price = round(int(flat_price) / flat_area, 2)

            prices.append(int(flat_price))
            add_prices.append(flat_additional_price)
            links.append(flat_link)
            locations.append(flat_location.strip())
            titles.append(flat_title)
            areas.append(flat_area)
            dates.append(flat_date)
            rooms.append(flat_rooms)

    df_flats = pd.DataFrame(
        {'title': titles, 'location': locations, 'area': areas, 'rooms': rooms, 'price': prices,
         'additionalPrice': add_prices, 'date': dates, 'link': links})
    return df_flats


def plot_flats_from_gumtree_depends_on_data(flats_from_gumtree):
    flats_from_gumtree['date'] = pd.to_datetime(flats_from_gumtree['date'], format='%d/%m/%Y')
    flats_from_gratka = flats_from_gumtree.sort_values(by=['date'])
    fig = plt.figure()
    plt.scatter(flats_from_gratka.date, flats_from_gratka.additionalPrice)
    fig.set_size_inches(15, 6)
    plt.xticks(rotation=45)
    plt.title('Mieszkania z Gumtree - Cena (zł) za m^2 w zależności od daty');
    plt.show()


def plot_flats_from_gratka_depends_on_area(flats_from_gumtree):
    flats_from_gumtree['date'] = pd.to_datetime(flats_from_gumtree['date'], format='%d/%m/%Y')
    flats_from_gratka = flats_from_gumtree.sort_values(by=['date'])
    fig = plt.figure()
    plt.scatter(flats_from_gratka.area, flats_from_gratka.additionalPrice)
    fig.set_size_inches(15, 6)
    plt.xticks(rotation=45)
    plt.xticks(np.arange(round(flats_from_gratka['area'].min(), 0), flats_from_gratka['area'].max() + 1, 50.0))
    plt.title('Mieszkania z Gumtree - Cena (zł) za m^2 w zależności od powierzchni');
    plt.show()


def plot_houses_from_gumtree_depends_on_data(houses_from_gumtree):
    houses_from_gumtree['date'] = pd.to_datetime(houses_from_gumtree['date'], format='%d/%m/%Y')
    houses_from_gumtree = houses_from_gumtree.sort_values(by=['date'])
    fig = plt.figure()
    plt.scatter(houses_from_gumtree.date, houses_from_gumtree.additionalPrice)
    fig.set_size_inches(15, 6)
    plt.xticks(rotation=45)
    plt.title('Domy z Gumtree - Cena (zł) za m^2 w zależności od daty');
    plt.show()


def plot_houses_from_gumtree_depends_on_area(houses_from_gumtree):
    houses_from_gumtree['date'] = pd.to_datetime(houses_from_gumtree['date'], format='%d/%m/%Y')
    houses_from_gumtree = houses_from_gumtree.sort_values(by=['date'])
    fig = plt.figure()
    plt.scatter(houses_from_gumtree.area, houses_from_gumtree.additionalPrice)
    fig.set_size_inches(15, 6)
    plt.xticks(rotation=45)
    plt.xticks(np.arange(round(houses_from_gumtree['area'].min(), 0), houses_from_gumtree['area'].max() + 1, 50.0))
    plt.title('Domy z Gumtree - Cena (zł) za m^2 w zależności od powierzchni');
    plt.show()
