from flask import Flask, render_template, request, redirect, url_for
from models import db, AuthorModel, LibraryModel
 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def landing():
    return render_template('landing.html')

@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':
        # Book_id=request.form['Book_id']
        Bookname=request.form['Bookname']
        Authorname=request.form['Authorname']
        Subjects=request.form['Subjects']
        Isbnumber=request.form['Isbnumber']
        Publisher=request.form['Publisher']
        Link=request.form['Link']
        Ratings=request.form['Ratings']
        # rating_count=request.form['rating_count']
        book=LibraryModel(title=Bookname,authors=Authorname,subjects=Subjects,isbn=Isbnumber,publisher=Publisher,image_url=Link,ratings=Ratings)#,rating_count=rating_count)
        db.session.add(book)
        db.session.commit()
        print("done")
        return redirect('/data')
 

# @app.route('/createauthor' , methods = ['GET','POST'])
# def createauthor():
#     if request.method=='GET':
#         return render_template('createauthor.html')

#     if request.method == 'POST':
#         Authorname=request.form['Authorname']
#         # Dateofbirth=request.form['Dateofbirth']
#         Genre=request.form['Genre']
#         Place=request.form['Place']
#         Link=request.form['Link']
#         author=AuthorModel(Authorname=Authorname,Place=Place,Genre=Genre,Link=Link)
#         db.session.add(author)
#         db.session.commit()
#         return redirect('/data/auth')

@app.route('/books')
def books():
    page = request.args.get('page', 1, type=int)
    # books= LibraryModel.query.all()
    books = LibraryModel.query.paginate(page=page, per_page=12)
    return render_template('datalist.html',books= books)

 
# @app.route('/data/auth')
# def RetrieveAuthorList():
#     authors= AuthorModel.query.all()
#     return render_template('authlist.html',authors= authors)


@app.route('/data/<int:id>')
def RetrieveBooks(id):
    book=LibraryModel.query.filter(id == id).first()
    print(id)
    print(book)
    if book:
        return render_template('data.html', book=book)
    return f"Book with id={id} Does not exist"

# @app.route('/data/auth/<int:Author_id>')
# def RetrieveAuthors(Author_id):
#     author= AuthorModel.query.filter_by(Author_id=Author_id).first()
#     if author:
#         return render_template('author.html', author= author)
#     return f"Author with ={Author_id} Does not exist"
 
 
# @app.route('/data/<int:id>/update',methods = ['GET','POST'])
# def update(id):
#     employee = EmployeeModel.query.filter_by(employee_id=id).first()
#     if request.method == 'POST':
#         if employee:
#             db.session.delete(employee)
#             db.session.commit()
#             name = request.form['name']
#             age = request.form['age']
#             position = request.form['position']
#             employee = EmployeeModel(employee_id=id, name=name, age=age, position = position)
#             db.session.add(employee)
#             db.session.commit()
#             return redirect(f'/data/{id}')
#         return f"Employee with id = {id} Does not exist"
 
#     return render_template('update.html', employee = employee)
 
 
# @app.route('/data/<int:id>/delete', methods=['GET','POST'])
# def delete(id):
#     employee = EmployeeModel.query.filter_by(employee_id=id).first()
#     if request.method == 'POST':
#         if employee:
#             db.session.delete(employee)
#             db.session.commit()
#             return redirect('/data')
#         abort(404)
 
#     return render_template('delete.html')
 
app.run(host='localhost', port=5000, debug=True)