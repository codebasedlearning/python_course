# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about sqlite3 - a database connector.

Teaching focus
  - connect to sqlite database
  - read from database
  - closing context manager

Preparations
  - .env file with credentials (if you use ones), not part of the project;
  - the sqlite3 module is part of Python's standard library, so no pip needed
"""


import sqlite3
from contextlib import closing


def read_from_sqlite_database():
    """ query sqlite database """
    print("\nread_from_sqlite_database\n=========================")

    with closing(sqlite3.connect('./sql/mhist_products.sqlite')) as connection:
        with closing(connection.cursor()) as cursor:
            print(f" 1| select * from produkt")
            rows = cursor.execute("select * from produkt")  # .fetchall()
            for row in rows:
                print(f" a| - {row=}")
            print()

            print(f" 2| select [...] where bezeichnung is Spinat")
            rows = cursor.execute("select * from produkt where bezeichnung=?", ("Spinat",))  # .fetchall()
            for row in rows:
                print(f" b| - {row=}")


if __name__ == "__main__":
    read_from_sqlite_database()


"""
sqlite3
From https://docs.python.org/3/library/sqlite3.html
  - SQLite is a C library that provides a lightweight disk-based database 
    that doesn’t require a separate server process and allows accessing 
    the database using a nonstandard variant of the SQL query language. 
    Some applications can use SQLite for internal data storage. It’s 
    also possible to prototype an application using SQLite and then port 
    the code to a larger database such as PostgreSQL or Oracle.
  - In our focus, the library uses 'with' for the management of database 
    resources such as connections or cursors.
    
closing
  - remember, closing is a context manager for functions that, e.g., 
    return database resources, like connections or cursors. It ensures 
    that the resources are properly closed after their use.
"""
