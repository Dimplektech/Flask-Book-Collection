from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import  DeclarativeBase,Mapped, mapped_column
from sqlalchemy import Integer,String,Float



# create the app
app = Flask(__name__)

# Create Database
class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


# Configure the SQLite database, relative to the app instance folder.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

# Create the Extension
db = SQLAlchemy(model_class=Base)

# Initialize the app with the extension
db.init_app(app)

# Create Table
class Book(db.Model):
    """
       Model for a book in the database.

       Attributes:
           id: Primary key of the book.
           title: Title of the book.
           author: Author of the book.
           review: User's rating for the book.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    review: Mapped[str] = mapped_column(Float, nullable=False)

    # Optional: This will allow each book object to be identified by it's title when printed
    def __repr__(self):
        return f"<Book {self.title}>"

# Create table schema in the database, Requires application context:
with app.app_context():
    db.create_all()


# all_books = []
# book = {}


@app.route('/')
def home():
    """
       Homepage that displays all books in the database.

       Returns:
           Rendered HTML template with a list of books.
       """
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = result.scalars().all()

    return  render_template('index.html',books=all_books)


@app.route("/add",methods=["GET","POST"])
def add():
    """
       Add a new book to the database.

       On GET: Renders the form to add a book.
       On POST: Adds the book to the database and redirects to the home page.

       Returns:
           Redirect to homepage on successful addition or rendered form on GET.
       """
    if request.method == "POST":
        # Create book record
        with app.app_context():
            new_book= Book(title=request.form["title"],
                           author=request.form["author"],
                           review = request.form["rating"])
            db.session.add(new_book)
            db.session.commit()
        # book={
        #     "title":request.form["title"],
        #     "author":request.form["author"],
        #     "rating":request.form["rating"]
        # }
        # all_books.append(book)
        # print(all_books)

            #print(all_books.all())
        return redirect(url_for('home'))

    return render_template('add.html')

@ app.route("/edit/<id>",methods=["GET","POST"])
def edit(id):
    """
       Edit the rating of an existing book.

       Args:
           id: The ID of the book to edit.

       Returns:
           Redirect to homepage on successful edit or rendered edit form on GET.
       """

    book_selected = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    if request.method == "POST":
        new_rating = request.form
        print(book_selected)
        book_selected.review= new_rating["new_rating"]
        db.session.commit()
        return redirect(url_for('home'))


    return render_template("edit_rating.html",book = book_selected)

@app.route("/delete/<id>")
def delete(id):
    """
        Delete a book from the database.

        Args:
            id: The ID of the book to delete.

        Returns:
            Redirect to homepage after deletion.
        """
    book_to_delete = db.session.execute(db.select(Book).where(Book.id==id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    print(f"Book {book_to_delete.title} has been Deleted!!")

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

