import sqlite3
from flask import (
    Flask,
    current_app,
    g,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from flask_restful import Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, UserMixin
import os


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


DATABASE = "identifier.sqlite"
app = Flask(__name__)
app.secret_key = "secret key"
app.config["DATABASE"] = os.path.join(
    app.instance_path,
    r"g:\Other computers\My Laptop\Documents\Repos\EasyPOS\EzPOS-server\identifier.sqlite",
)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def login():
    return render_template("login.html")


class User(UserMixin):
    def __init__(self, id):
        self.id = id

@app.route("/register", methods=["GET", "POST"])
def register_post():
    # Check if the app has been started for the first time
    first_start = query_db("SELECT stat FROM flags WHERE flag_name = 'first_start'", one=True)
    if first_start and first_start['value'] == 'true':
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            hashed_password = generate_password_hash(password, method='sha256')

            # Store the username and hashed_password in the database
            # ...

            # Set the 'first_start' flag to 'false'
            get_db().execute("UPDATE flags SET stat = 'false' WHERE name = 'first_start'")
            get_db().commit()

            return redirect(url_for("login"))
    else:
        # If the app has been started before, check if the user is an admin or manager
        user = query_db("SELECT * FROM users WHERE id = ?", (current_user.id,), one=True)
        if user and (user['role'] == 'admin' or user['role'] == 'manager'):
            if request.method == "POST":
                username = request.form.get("username")
                password = request.form.get("password")
                hashed_password = generate_password_hash(password, method='sha256')

                # Store the username and hashed_password in the database
                # ...

                return redirect(url_for("login"))
        else:
            # If the user is not an admin or manager, redirect them to the login page
            return redirect(url_for("login"))

    return render_template("register.html")

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    user = query_db("SELECT * FROM users WHERE username = ?", (username,))
    if not user or not check_password_hash(user["password"], password):
        flash("Please check your login details and try again.")
        return redirect(url_for("login"))

    # If the above check passes, then we know the user has the right credentials
    login_user(User(user["id"]))
    return redirect(
        url_for("layout")
    )  # if user doesn't exist or password is wrong, reload the page


# If the above check passes, then we know the user has the right credentials
# login_user(user)
# return redirect(url_for('dashboard'))


@app.route("/result")
def result():
    # Some code here to perform a database transaction and get a message
    msg = "Transaction successful"
    return render_template("result.html", msg=msg)


@app.route("/layout")
def layout():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM users")
    return render_template("layout.html", rows=cur.fetchall())


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


def init_db():
    """
    Initialize the database.

    Returns:
    - sqlite3.Connection: The database connection.
    """
    with app.app_context():
        db = get_db()

        with app.open_resource("schema.sql") as f:
            if (
                db.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='flags'"
                ).fetchone()
                is None
            ):
                db.executescript(f.read().decode("utf8"))
                db.commit()

init_db()

if __name__ == "__main__":
    app.run()
