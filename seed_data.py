# # seed_data.py

# from app import app, db
# from models import Book, User

# with app.app_context():  # Ensure app context is pushed
#     db.create_all()  # Create tables before inserting data





#     # Book data
#     books = [
#     {
#         "id":1,
#         "name":"To Kill a Mockingbird",
#         "author":"Harper Lee",
#         "genre":"Fiction",
#         "year":1960,
#         "amount":10,
#         "loandate":14,
#         "image":"to_kill_a_mockingbird.jpg"
#     },
#     {
#         "id":2,
#         "name":"1984",
#         "author":"George Orwell",
#         "genre":"Dystopian",
#         "year":1949,
#         "amount":8,
#         "loandate":7,
#         "image":"1984.jpg"
#     },
#     {
#         "id":3,
#         "name":"The Great Gatsby",
#         "author":"F. Scott Fitzgerald",
#         "genre":"Classic",
#         "year":1925,
#         "amount":5,
#         "loandate":14,
#         "image":"the_great_gatsby.jpg"
#     },
#     {
#         "id":4,
#         "name":"Pride and Prejudice",
#         "author":"Jane Austen",
#         "genre":"Romance",
#         "year":1813,
#         "amount":6,
#         "loandate":30,
#         "image":"pride_and_prejudice.jpg"
#     },
#     {
#         "id":5,
#         "name":"The Hobbit",
#         "author":"J.R.R. Tolkien",
#         "genre":"Fantasy",
#         "year":1937,
#         "amount":12,
#         "loandate":7,
#         "image":"the_hobbit.jpg"
#     },
#     {
#         "id":6,
#         "name":"Fahrenheit 451",
#         "author":"Ray Bradbury",
#         "genre":"Dystopian",
#         "year":1953,
#         "amount":4,
#         "loandate":30,
#         "image":"fahrenheit_451.jpg"
#     },
#     {
#         "id":7,
#         "name":"Moby Dick",
#         "author":"Herman Melville",
#         "genre":"Adventure",
#         "year":1851,
#         "amount":3,
#         "loandate":14,
#         "image":"moby_dick.jpg"
#     },
#     {
#         "id":8,
#         "name":"War and Peace",
#         "author":"Leo Tolstoy",
#         "genre":"Historical",
#         "year":1869,
#         "amount":7,
#         "loandate":30,
#         "image":"war_and_peace.jpg"
#     },
#     {
#         "id":9,
#         "name":"The Odyssey",
#         "author":"Homer",
#         "genre":"Epic",
#         "year":-800,
#         "amount":5,
#         "loandate":7,
#         "image":"the_odyssey.jpg"
#     },
#     {
#         "id":10,
#         "name":"Catch-22",
#         "author":"Joseph Heller",
#         "genre":"Satire",
#         "year":1961,
#         "amount":9,
#         "loandate":14,
#         "image":"catch_22.jpg"
#     },
#     {
#         "id":11,
#         "name":"The Chronicles of Narnia",
#         "author":"C.S. Lewis",
#         "genre":"Fantasy",
#         "year":1950,
#         "amount":6,
#         "loandate":7,
#         "image":"narnia.jpg"
#     },
#     {
#         "id":12,
#         "name":"Wuthering Heights",
#         "author":"Emily Bronte",
#         "genre":"Romance",
#         "year":1847,
#         "amount":4,
#         "loandate":30,
#         "image":"wuthering_heights.jpg"
#     },
#     {
#         "id":13,
#         "name":"Crime and Punishment",
#         "author":"Fyodor Dostoevsky",
#         "genre":"Philosophy",
#         "year":1866,
#         "amount":8,
#         "loandate":14,
#         "image":"crime_and_punishment.jpg"
#     },
#     {
#         "id":14,
#         "name":"The Lord of the Rings",
#         "author":"J.R.R. Tolkien",
#         "genre":"Fantasy",
#         "year":1954,
#         "amount":10,
#         "loandate":7,
#         "image":"lotr.jpg"
#     },
#     {
#         "id":16,
#         "name":"Jane Eyre",
#         "author":"Charlotte Bronte",
#         "genre":"Romance",
#         "year":1847,
#         "amount":4,
#         "loandate":14,
#         "image":"jane_eyre.jpg"
#     },
#     {
#         "id":17,
#         "name":"Animal Farm",
#         "author":"George Orwell",
#         "genre":"Satire",
#         "year":1945,
#         "amount":6,
#         "loandate":7,
#         "image":"animal_farm.jpg"
#     },
#     {
#         "id":18,
#         "name":"The Catcher in the Rye",
#         "author":"J.D. Salinger",
#         "genre":"Fiction",
#         "year":1951,
#         "amount":8,
#         "loandate":30,
#         "image":"catcher_in_the_rye.jpg"
#     },
#     {
#         "id":20,
#         "name":"The Bible",
#         "author":"Various Authors",
#         "genre":"Religious",
#         "year":-1500,
#         "amount":20,
#         "loandate":30,
#         "image":"bible.jpg"
#     },
#     {
#         "id":21,
#         "name":"Brave New World",
#         "author":"Aldous Huxley",
#         "genre":"Dystopian",
#         "year":1932,
#         "amount":9,
#         "loandate":14,
#         "image":"brave_new_world.jpg"
#     }
# ]

#     # Insert books
#     for book_data in books:
#         new_book = Book(**book_data)
#         db.session.add(new_book)

#     # Add test users
#     admin_user = User(username="admin", email="admin@example.com", password="password", admin=True)
#     regular_user = User(username="user", email="user@example.com", password="password", admin=False)

#     db.session.add(admin_user)
#     db.session.add(regular_user)

#     # Commit all changes
#     db.session.commit()
#     print("Books and users inserted successfully!")
from datetime import datetime
from app import app, db  # Ensure you import your app object here
from models import Cart, Book, User

# Assuming the user ID is 2 and the loan date is January 1, 2025
user_id = 2
loan_date = datetime(2025, 1, 1)

# Start an application context for Flask
with app.app_context():
    # Retrieve the book you want to add to the cart (replace the book_id with a valid ID)
    book_id = 1  # Use the correct book ID that you want to add
    book = Book.query.get(book_id)

    if book:
        # Create a new cart item
        new_cart_item = Cart(userid=user_id, bookid=book.id, loandate=loan_date)
        
        # Add to session and commit to the database
        db.session.add(new_cart_item)
        db.session.commit()

        print(f"Book '{book.name}' added to the cart for User ID {user_id}")
    else:
        print(f"Book with ID {book_id} not found!")
