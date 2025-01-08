# Import models
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Book

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
# Initialize extensions
db.init_app(app)

# Routes
@app.route('/')
def home():
    books = Book.query.all()  # Fetch all books from the database
    return render_template("home.html", books=books)

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('searchTerm', '').lower()
    search_option = request.form.get('searchOption', '')

    if not search_term or not search_option:
        results = Book.query.all()
        return render_template("search_results.html", results=results)

    if search_option == "name":
        results = Book.query.filter(Book.name.ilike(f"%{search_term}%")).all()
    elif search_option == "author":
        results = Book.query.filter(Book.author.ilike(f"%{search_term}%")).all()
    elif search_option == "genre":
        results = Book.query.filter(Book.genre.ilike(f"%{search_term}%")).all()
    elif search_option == "year":
        try:
            search_year = int(search_term)
            results = Book.query.filter(Book.year == search_year).all()
        except ValueError:
            results = []
    else:
        results = []

    return render_template("search_results.html", results=results)

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        found_user = User.query.filter_by(username=username).first()

        if found_user(found_user.password, password):
            session['user_id'] = found_user.id  # Store user ID in session
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password. Please try again.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Clear user session
    return redirect(url_for('home'))

def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

@app.context_processor
def inject_current_user():
    return {'current_user': get_current_user()}

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    