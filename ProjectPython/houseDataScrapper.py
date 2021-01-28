from IPython.display import display
from FlatsFromGumtreePage import *
from FlatsFromGratkaPage import *

desired_width = 420

pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 12)


def filter_by_field(dataset, min, max, field):
    filter1 = (dataset[field] >= min)
    filter2 = (dataset[field] <= max)
    return dataset.where(filter1 & filter2).dropna()

# houses_from_gumtree = parse_houses_from_gumtree(2, 'krakow')
houses_from_gumtree = parse_houses_from_gumtree(2, 'warszawa')
display(houses_from_gumtree)

flats_from_gumtree = parse_flats_from_gumtree(2, 'krakow')
display(flats_from_gumtree)

houses_from_gratka = parse_houses_from_gratka(2, 'krakow')
display(houses_from_gratka)

flats_from_gratka = parse_flats_from_gratka(2, 'krakow')
display(flats_from_gratka)

plot_flats_from_gumtree_depends_on_data(flats_from_gumtree)

plot_flats_from_gratka_depends_on_area(flats_from_gratka)

display(filter_by_field(flats_from_gratka, 200000, 350000, 'price'))