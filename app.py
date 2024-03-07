from math import e, log
import sqlite3
from flask import (
    Flask,
    current_app,
    g,
    render_template,
    request,
    flash,
    redirect,
    session,
    url_for,
)
from flask_restful import Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os



DATABASE = "identifier.sqlite"
app = Flask(__name__)
app.secret_key = "secret key"
app.instance_path = os.path.join(app.root_path, "instance")
os.makedirs(app.instance_path, exist_ok=True)
app.config["DATABASE"] = os.path.join(
    app.instance_path,
    "identifier.sqlite",
)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Add this line
    return db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()



@app.route("/")
def index():
    first_start = query_db("SELECT stat FROM flags WHERE flag_name = 'first_start'", one=True)
    if first_start and first_start['stat'] == 'true':
        return redirect(url_for("user_register_post"))
    else:
        return redirect(url_for("login_post"))


class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return str(self.id)  # unicode is not needed in Python 3

    @property
    def is_active(self):
        # This should return True unless the user has been deactivated
        return True

@app.route("/user_register", methods=["GET", "POST"])
def user_register_post():
    first_start = query_db("SELECT stat FROM flags WHERE flag_name = 'first_start'", one=True)
    if first_start and first_start['stat'] == 'true':
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            db = get_db()

            user_exists = db.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone() is not None

            if user_exists:
                flash("User already exists")
                return render_template("user_register.html")
            else:
                db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, 'admin'))
                db.commit()
                return redirect(url_for("login_post"))
    else:
        return redirect(url_for("login_post"))

    return render_template("user_register.html")

@login_manager.user_loader
def load_user(user_id):
    user = query_db("SELECT * FROM users WHERE user_id = ?", (user_id,), one=True)
    if user:
        return User(user_id)
    return None

@app.route("/login", methods=["GET","POST"])
def login_post():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = query_db("SELECT * FROM users WHERE username = ?", (username,))
        if users:
            user = users[0]
        else:
            flash("Please check your login details and try again.")
            return render_template("login.html")

        user_dict = dict(user)
        if user_dict.get("password") is not None and user_dict["password"] is not None and not check_password_hash(user_dict["password"], password):
            flash("Please check your login details and try again.")
            return render_template("login.html")

        # If the above check passes, then we know the user has the right credentials
        if 'user_id' in user_dict:
            session['user_id'] = user_dict['user_id']

        user = User(user_dict['user_id'])  # Create User object here
        login_user(user)    
    else:
        return render_template("login.html")

    return redirect(url_for('home'))


@app.route("/result")
def result():
    # Some code here to perform a database transaction and get a message
    msg = "Transaction successful"
    return render_template("result.html", msg=msg)

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/enternew')
@login_required
def enternew():
    return render_template('enternew.html', categories=categories)  # Add the "categories" variable to the render_template function

@app.route('/new_category', methods=['GET', 'POST'])  # Add a new route for creating a new category
@login_required
def new_category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        # Code to save the new category to the database
        flash('New category created successfully')
        return redirect(url_for('enternew'))
    return render_template('new_category.html')  # Create a new template for creating a new category

@app.route('/list')
def list():
    menu_items = query_db("SELECT * FROM menu_items")
    return render_template('list.html', menu_items=menu_items)

@app.route("/layout", methods=["GET", "POST"])
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
