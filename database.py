
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer,String,Float

from main import all_books

# create the app
app = Flask(__name__)

# Create Database
class Base(DeclarativeBase):
    pass

# Configure the SQLite database, relative to the app instance folder.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# Create the Extension
db = SQLAlchemy(model_class=Base)
# Initialize the app with the extension
db.init_app(app)

# Create Table
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str]= mapped_column(String(250), unique=True,nullable=False)
    author: Mapped[str]= mapped_column(String(250), nullable=False)
    review: Mapped[str]= mapped_column(Float,nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f"<Book {self.title}>"

# Create table schema in the database, Requires application context.
with app.app_context():
    db.create_all()
#
# # Create Record
# with app.app_context():
#     new_book = Book( title="Harry Potter", author="J. K. Rowling", review=9.3)
#     db.session.add(new_book)
#     db.session.commit()
# with app.app_context():
#     new_book = Book( title="Giant Man", author="D.K.Kaware", review=9.3)
#     db.session.add(new_book)
#     db.session.commit()


# Read all Records
with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()
    print(all_books.first())
#
# Read a Particular Record by Query
with app.app_context():
    book = db.session.execute(db.select(Book).where(Book.title=="Harry Potter")).scalar()

# # Update  a Particular Record by Query
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Book).where(Book.title=="Giant Man")).scalar()
#     book_to_update.title ="Giant Man and Tiny Girl"
#     db.session.commit()

# Update Record by Primary Key
book_id = 1
with app.app_context():
    book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    book_to_update.author = " J.K.Rowling-updated"
    db.session.commit()

# Delete a Particular record By Primary Key
book_id =1
with app.app_context():
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()











