from flask_sqlalchemy import SQLAlchemy
 
db =SQLAlchemy()
 
# class BookModel(db.Model):
#     __tablename__ = "book"
 
#     Book_id=db.Column(db.Integer(),primary_key=True)
#     Bookname= db.Column(db.String())
#     Authorname= db.Column(db.String())
#     Subjects= db.Column(db.String())
#     Isbnumber= db.Column(db.String())
#     Publisher= db.Column(db.String())
#     Link=db.Column(db.String())
#     Rating= db.Column(db.Integer(),default=0)
 
#     def __init__(self,Bookname ,Authorname,Subjects,Isbnumber,Publisher,Link,Ratings):
#         self.Bookname= Bookname
#         self.Authorname= Authorname
#         self.Subjects= Subjects
#         self.Isbnumber= Isbnumber
#         self.Publisher=Publisher
#         self.Link=Link
#         self.Rating=Ratings

 
#     def __repr__(self):
#         return f"{self.Bookname}:{self.Authorname}"

class LibraryModel(db.Model):
    __tablename__ = "book_data"
 
    id=db.Column(db.Integer(),primary_key=True)
    title= db.Column(db.String())
    authors= db.Column(db.String())
    subjects= db.Column(db.String())
    isbn= db.Column(db.String())
    publisher= db.Column(db.String())
    image_url=db.Column(db.String())
    ratings= db.Column(db.Integer(),default=0)
    rating_count=db.Column(db.Integer(),default=0)
    def __init__(self,title ,image_url,authors,subjects,isbn,publisher,ratings):
        self.title= title
        self.authors= authors
        self.subjects= subjects
        self.isbn= isbn
        self.publisher=publisher
        self.image_url=image_url
        self.ratings=ratings
        # self.rating_count=rating_count
        
 
    def __repr__(self):
        return f"{self.title}:{self.authors}"

class AuthorModel(db.Model):
    __tablename__ = "author"

    Author_id=db.Column(db.Integer(),primary_key=True)
    Authorname= db.Column(db.String())
    # Dateofbirth=db.Column(db.Date())
    Genre= db.Column(db.String())
    Place= db.Column(db.String())
    Link=db.Column(db.String())
 
    def __init__(self,Authorname,Place,Genre,Link):
        
        self.Authorname= Authorname
        # self.Dateofbirth=Dateofbirth
        self.Place=Place
        self.Genre = Genre
        self.Link=Link

 
    def __repr__(self):
        return f"{self.Authorname}"

class UserModel(db.Model):
    __tablename__ = "user"

    User_id=db.Column(db.Integer(),primary_key=True)
    Firstname= db.Column(db.String())
    Lastname= db.Column(db.String())
    Email= db.Column(db.String())
    Password=db.Column(db.String())

    def __init__(self,Firstname,Lastname,Email,Password):
        
        self.Firstname= Firstname
        self.Lastname= Lastname
        self.Email=Email
        self.Password=Password
 
    def __repr__(self):
        return f"{self.Firstname}:{self.Email}"