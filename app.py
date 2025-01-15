from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Book, Cart
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong, random key

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

@app.route('/')
def home():
    books = Book.query.all()
    cart_items = []

    if "user_id" in session:
        # Query the cart items for the logged-in user
        cart_items = db.session.query(Cart, Book).join(Book).filter(Cart.userid == session["user_id"]).all()

    return render_template("home.html", books=books, cart_items=cart_items)


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

        if found_user and found_user.password == password:
            session['user_id'] = found_user.id
            session['is_admin'] = found_user.admin
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password. Please try again.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")




@app.route('/cart', methods=["POST", "GET"])
def cart():
    if "user_id" in session:
        # Query to get the books from the cart, including both 'Cart.loandate' and 'Book.loandate'
        cart_items = db.session.query(Cart, Book).join(Book).filter(Cart.userid == session["user_id"]).all()
        
        # Adjusting the cart's loandate by adding the number of days from the book's loandate
        for cart_item, book in cart_items:
                adjusted_loandate = cart_item.loandate + timedelta(days=book.loandate)
            
                # print(f"Adjusted loan date for {book.name}: {cart_item.loandate}")  # Log for debugging
            
        return render_template("home.html", cart_items=cart_items)
    else:
        flash("You are not logged in.", "danger")
        return redirect(url_for('home'))

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    # Ensure the user is logged in and is an admin
    if 'user_id' not in session or not session.get('is_admin', False):
        flash("You must be an admin to access this page.", "danger")
        return redirect(url_for('home'))  # Redirect to home if not an admin
    
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        amount = request.form['amount']
        loandate = request.form['loandate']
        image = request.files.get('image')  # Handle image upload

        # Save the image if uploaded
        image_filename = None
        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join('static/images', image_filename))

        # Create the new book and add it to the database
        new_book = Book(
            name=name,
            author=author,
            genre=genre,
            year=year,
            amount=amount,
            loandate=loandate,
            image=image_filename
        )

        db.session.add(new_book)
        db.session.commit()

        flash("New book added successfully!", "success")
        return redirect(url_for('home'))  # Redirect after adding the book

    return render_template('add_book.html')


@app.route('/return_book/<int:cart_item_id>', methods=["POST"])
def return_book(cart_item_id):
    if "user_id" in session:
        # Find the cart item by ID
        cart_item = Cart.query.get(cart_item_id)
        

        if cart_item and cart_item.userid == session["user_id"]:
            book = Book.query.get(cart_item.bookid)
            book.amount += 1
            db.session.commit()
            # Delete the cart item
            db.session.delete(cart_item)
            db.session.commit()

            flash("Book returned successfully!", "success")
        else:
            flash("Unable to return book. Invalid cart item or user.", "danger")

        return redirect(url_for('cart'))
    else:
        flash("You are not logged in.", "danger")
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/loan_book/<int:book_id>', methods=["POST"])
def loan_book(book_id):
    if "user_id" in session:
        user_id = session["user_id"]
        
        # Check if the book exists
        book = Book.query.get(book_id)
        if not book:
            flash("Book not found.", "danger")
            return redirect(url_for('home'))  # Ensure there's a redirect if book isn't found
        
        # Check if the user already has this book in their cart
        existing_cart_item = Cart.query.filter_by(userid=user_id, bookid=book_id).first()
        amount_cart_item = Cart.query.filter_by(userid=user_id, bookid=book_id).count()
        if existing_cart_item:
            flash(f"You already have '{book.name}' in your cart.", "danger")
            return redirect(url_for('home'))  # Return a redirect if book is already in the cart
        
        
        if amount_cart_item>3:
            flash(f"you have alredy loaned more then 3 books", "danger")
            return redirect(url_for('home'))  # Return a redirect if book is already in the cart
        
        cart_itemss = (db.session.query(Cart).join(Book, Cart.bookid == Book.id).filter(Cart.userid == user_id).options(joinedload(Cart.book)).all())
        for late in cart_itemss:
            if  (timedelta(days=late.book.loandate)+late.loandate<datetime.utcnow()):
                flash(f"you must return the late books before loaning new ones", "danger")
            return redirect(url_for('home'))

        if book.amount <= 0:
            flash(f"Sorry, '{book.name}' is currently unavailable.", "danger")
            return redirect(url_for('home'))

        # Add the book to the user's cart
        loan_date = datetime.now()  # Set loan date to current time
        new_cart_item = Cart(userid=user_id, bookid=book_id, loandate=loan_date)
        db.session.add(new_cart_item)
        
        # Decrease the book amount by 1 (loan the book out)
        book.amount -= 1
        db.session.commit()
        
        flash(f"You have successfully loaned '{book.name}'.", "success")
        return redirect(url_for('home'))  # Ensure there's a return to a valid route after adding the book
    else:
        flash("You need to log in to loan a book.", "danger")
        return redirect(url_for('login'))  # Ensure there's a return to the login page if user is not logged in

@app.route('/delete_book/<int:book_id>', methods=["POST"])
def delete_book(book_id):
    if 'user_id' not in session or not session.get('is_admin', False):
        flash("You must be an admin to delete books.", "danger")
        return redirect(url_for('home'))

    book = Book.query.get(book_id)
    if not book:
        flash("Book not found.", "danger")
        return redirect(url_for('home'))

    # Instead of fully deleting the book, mark it as inactive if desired
    db.session.delete(book)
    db.session.commit()

    flash(f"'{book.name}' has been deleted successfully.", "success")
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)

# app.jinja_env.globals['timedelta'] = timedelta