from flask import Flask, request, render_template, redirect

from FlatsFromGratkaPage import parse_flats_from_gratka
from HouseDataScrapper import filter_by_field
from IPython.display import display
from FlatsFromGumtreePage import *
from FlatsFromGratkaPage import *

desired_width = 420

pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 12)

app = Flask(__name__)
# global df_flats
df_flats = pd.DataFrame(
    {'title': [], 'location': [], 'area': [], 'rooms': [], 'price': [],
     'additionalPrice': [], 'date': [], 'link': []})
counter = 0


def save_df(path):
    display(df_flats)
    global counter
    path = str(path) + "export_dataframe" + str(counter) + ".csv"
    counter += 1
    df_flats.to_csv(path, index=False, header=True)


def filter_data(from_price=None, to_price=None, from_area=None, to_area=None):
    display(df_flats)
    df_flats_price = filter_by_field(df_flats, int(from_price), int(to_price), 'price')
    df_flats_price_and_area = filter_by_field(df_flats_price, int(from_area), int(to_area), 'area')
    display(df_flats_price_and_area)
    return df_flats_price_and_area


@app.route('/')
def login():
    return render_template("startPage.html")


@app.route('/sendParams', methods=['POST', 'GET'])
def send_params():
    pages_number = request.form['pages_number']
    city = request.form['city']
    page_name = request.form['page_name']
    print(page_name)
    global df_flats
    if page_name == "gratka":
        df_flats = parse_flats_from_gratka(int(pages_number), str(city.strip()))
    else:
        df_flats = parse_flats_from_gumtree(int(pages_number), str(city.strip()))
    return render_template('startPage.html', tables=[df_flats.to_html(classes='data')], titles=df_flats.columns.values)


@app.route('/saveData', methods=['POST', 'GET'])
def save_data():
    path = request.form['path']
    print(path)
    save_df(path)
    return render_template('startPage.html', tables=[df_flats.to_html(classes='data')], titles=df_flats.columns.values)


@app.route('/getData', methods=['POST', 'GET'])
def form():
    from_price = request.form['from_price']
    to_price = request.form['to_price']
    from_area = request.form['from_area']
    to_area = request.form['to_area']
    global df_flats
    df_flats = filter_data(from_price, to_price, from_area, to_area)
    return render_template('startPage.html', tables=[df_flats.to_html(classes='data')], titles=df_flats.columns.values)


if __name__ == "__main__":
    # Launch the Flask dev server
    app.run(host="localhost", debug=True)
