from calendar import c
import sqlite3
from flask import g

DATABASE = "database.db"


def get_db():
    """
    Connect to the SQLite database.

    Returns:
    - sqlite3.Connection: The database connection.
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    """
    Close the database connection.

    Args:
    - exception (Exception): The exception that was thrown.
    """
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM users")


def make_dicts(cursor, row):
    """
    Convert the database row into a dictionary.

    Args:
    - cursor (sqlite3.Cursor): The database cursor.
    - row (sqlite3.Row): The database row.

    Returns:
    - dict: The database row as a dictionary.
    """
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


def query_db(query, args=(), one=False):
    """
    Query the database.

    Args:
    - query (str): The SQL query to execute.
    - args (tuple, optional): The arguments to pass to the query.
    - one (bool, optional): Whether to return one row or all rows.

    Returns:
    - list: The query results.
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


user = query_db("SELECT * FROM users WHERE username = ?", [username], one=True)
if user is None:
    print("No such user")
else:
    print(username, "has the id", user["id"])


def init_db():
    """
    Initialize the database.

    Returns:
    - sqlite3.Connection: The database connection.
    """
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()
