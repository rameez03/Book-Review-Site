from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class LibraryModel(db.Model):
    __tablename__ = "book_data"
 
    bookid=db.Column(db.Integer(),primary_key=True)
    title= db.Column(db.String())
    authors= db.Column(db.String())
    subjects= db.Column(db.String())
    isbn= db.Column(db.String())
    publisher= db.Column(db.String())
    image_url=db.Column(db.String())
    ratings= db.Column(db.Float(),default=0)
    rating_count=db.Column(db.Integer(),default=0)

    def __init__(self,title,image_url,authors,subjects,isbn,publisher,ratings):
        self.title= title
        self.authors= authors
        self.subjects= subjects
        self.isbn= isbn
        self.publisher=publisher
        self.image_url=image_url
        self.ratings=ratings
        self.rating_count=rating_count
        
 
    def __repr__(self):
        return f"{self.title}:{self.authors}"


class Comments(UserMixin, db.Model):
    __tablename__ = "comments"
 
    commentid=db.Column(db.Integer(),primary_key=True)
    bookid=db.Column(db.Integer())
    username= db.Column(db.String())
    comment= db.Column(db.String())

    def __init__(self, bookid, username, comment):
        self.bookid = bookid
        self.username = username
        self.comment = comment
 
    def __repr__(self):
        return f"{self.username}: {self.comment}"


class Ratings(UserMixin, db.Model):
    __tablename__ = "ratings"
 
    id=db.Column(db.Integer(),primary_key=True)
    bookid=db.Column(db.Integer())
    username= db.Column(db.String())
    rating= db.Column(db.Integer())

    def __init__(self, bookid, username, rating):
        self.bookid = bookid
        self.username = username
        self.rating = rating
 
    def __repr__(self):
        return f"{self.rating}"