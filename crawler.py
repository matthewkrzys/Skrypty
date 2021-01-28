from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
import concurrent.futures
import requests
from bs4 import BeautifulSoup


Base = declarative_base()
db_uri = 'sqlite:///db.sqlite'
engine = create_engine(db_uri)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Things(Base):
    __tablename__ = 'Things'

    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    price = Column(Float)
    review = Column(String(30))

    def __init__(self, title, price, review):
        self.title = title
        self.price = price
        self.review = review

    def get_name(self):
        return self.title


def add_new_thing(title, price, review):
    thing = Things(title=str(title), price=float(price), review=str(review))
    session.add(thing)
    session.commit()


def save_things(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'}

    page = requests.get("https://allegro.pl/kategoria/akcesoria-laptop-pc-stacje-dokujace-77781?string=usb%20c")

    soup = BeautifulSoup(page.text, 'html.parser')
    findElements = soup.find_all(class_='mpof_ki mqen_m6 mp7g_oh mh36_0 mvrt_0 mg9e_8 mj7a_8 m7er_k4 _1y62o _9c44d_1I1gg')

    for f in findElements:
        findTitle = f.find(class_='_w7z6o _uj8z7 meqh_en mpof_z0 mqu1_16 _9c44d_2vTdY')
        findPrice = f.find(class_='_1svub _lf05o')
        add_new_thing(findTitle.text.strip(), float(findPrice.text.strip().replace(" zł", "").replace(",",".").replace(" ","")), "Eh")
        print("Title: " + findTitle.text.strip() + " \nPrice: " + findPrice.text.strip())




def save_books_from_url():
    urls = ["https://allegro.pl/kategoria/akcesoria-laptop-pc-stacje-dokujace-77781?string=usb%20c"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(save_things, urls)


def setup_db():
    Base.metadata.create_all(engine)


def show_all():
    session.query(Things).all()

# if __name__ == '__main__':
#     if "setupdb" in sys.argv:
#         setup_db()
#     else:
#         save_books_from_url()
#         # show_all()

setup_db()
# save_books_from_url()
save_things("")
show_all()
