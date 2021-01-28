from flask import *
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/saveBook", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            price = request.form["price"]

            print(name)
            print(price)
            with sqlite3.connect("books.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Books (name, price) values (?,?)", (name, price))
                con.commit()
                msg = "Book successfully Added"
        except:
            con.rollback()
            msg = "We can not add the book to the list"
        finally:
            return render_template("success.html", msg=msg)
            con.close()


@app.route("/view")
def view():
    con = sqlite3.connect("books.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Books")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)


@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/deleteBook", methods=["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("books.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Books where id = ?", id)
            msg = "book successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_book.html", msg=msg)


if __name__ == "__main__":
    app.run(debug=True)