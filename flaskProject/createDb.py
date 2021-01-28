import sqlite3

con = sqlite3.connect("books.db")
print("Database opened successfully")

con.execute(
    "create table Books (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, price TEXT NOT NULL)")

print("Table created successfully")

con.close()