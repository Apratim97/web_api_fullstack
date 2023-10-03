# from flask import Flask, jsonify, request
# import psycopg2
# from psycopg2 import sql

# app = Flask(__name__)

# # PostgreSQL database configuration
# db_config = {
#     'dbname': 'test',
#     'user': 'postgres',
#     'password': 'Apratim@97',
#     'host': 'localhost'
# }

# def connect_to_db():
#     try:
#         connection = psycopg2.connect(**db_config)
#         return connection
#     except Exception as e:
#         print("Error: Unable to connect to the database")
#         print(e)
#         return None

# def create_books_table():
#     connection = connect_to_db()
#     if connection:
#         try:
#             cursor = connection.cursor()
#             create_table_query = """
#                 CREATE TABLE IF NOT EXISTS books (
#                     id SERIAL PRIMARY KEY,
#                     title VARCHAR(80) NOT NULL
#                 );
#             """
#             cursor.execute(create_table_query)
#             connection.commit()
#         except Exception as e:
#             print("Error: Unable to create the books table")
#             print(e)
#         finally:
#             close_connection(connection)

# def close_connection(connection):
#     if connection:
#         connection.close()

# create_books_table()

# @app.route('/books', methods=['GET'])
# def get_books():
#     connection = connect_to_db()
#     if connection:
#         try:
#             cursor = connection.cursor()
#             cursor.execute("SELECT * FROM books;")
#             books = cursor.fetchall()
#             book_list = [{"id": book[0], "title": book[1]} for book in books]
#             return jsonify({"books": book_list})
#         except Exception as e:
#             print("Error: Unable to fetch books from the database")
#             print(e)
#             return jsonify({"message": "Error occurred while fetching data from the database"}), 500
#         finally:
#             close_connection(connection)
#     else:
#         return jsonify({"message": "Error occurred while connecting to the database"}), 500

# @app.route('/books', methods=['POST'])
# def add_book():
#     data = request.get_json()
#     title = data.get('title')
#     if not title:
#         return jsonify({"message": "Title is required"}), 400
    
#     connection = connect_to_db()
#     if connection:
#         try:
#             cursor = connection.cursor()
#             insert_query = sql.SQL("INSERT INTO books (title) VALUES (%s) RETURNING id;")
#             cursor.execute(insert_query, [title])
#             new_book_id = cursor.fetchone()[0]
#             connection.commit()
#             return jsonify({"message": "Book added", "book": {"id": new_book_id, "title": title}}), 201
#         except Exception as e:
#             print("Error: Unable to add book to the database")
#             print(e)
#             return jsonify({"message": "Error occurred while adding data to the database"}), 500
#         finally:
#             close_connection(connection)
#     else:
#         return jsonify({"message": "Error occurred while connecting to the database"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)



# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Apratim@97@localhost/test'
# app.config['SECRET_KEY'] = '12345'
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session:
#             flash('You must be logged in to access this page.', 'danger')
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#         new_user = User(username=username, password=hashed_password)

#         db.session.add(new_user)
#         db.session.commit()

#         flash('Account created successfully!', 'success')
#         return redirect(url_for('login'))

#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         user = User.query.filter_by(username=username).first()

#         if user and bcrypt.check_password_hash(user.password, password):
#             session['user_id'] = user.id
#             flash('Logged in successfully!', 'success')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid username or password. Please try again.', 'danger')

#     return render_template('login.html')

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     # Retrieve user data based on session['user_id']
#     return render_template('dashboard.html')

# @app.route('/logout')
# @login_required
# def logout():
#     session.pop('user_id', None)
#     flash('You have been logged out.', 'success')
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(host='localhost', port=80, debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps
import psycopg2
from psycopg2 import sql

db_config = {
    'dbname': 'test',
    'user': 'postgres',
    'password': 'Apratim@97',
    'host': 'localhost'
}

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname=db_config['dbname'],
    user=db_config['user'],
    password=db_config['password'],
    host=db_config['host']
)

cur = conn.cursor()
app = Flask(__name__, template_folder='D:/web gis/test_flask_rest')
bcrypt = Bcrypt(app)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']

        if not username or not password:
            flash('Both username and password are required.', 'danger')
        else:
            # Hash the password before storing it
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Insert user data into the database
            query = sql.SQL("INSERT INTO users (username, password) VALUES ({}, {});").format(
                sql.Literal(username),
                sql.Literal(hashed_password)
            )

            cur.execute(query)
            conn.commit()

            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']

        # Retrieve user data from the database based on the username
        query = sql.SQL("SELECT * FROM users WHERE username = {};").format(
            sql.Literal(username)
        )

        cur.execute(query)
        user = cur.fetchone()

        if user and bcrypt.check_password_hash(user[2], password):
            session['user_id'] = user[0]
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(host='localhost', port=80, debug=True)