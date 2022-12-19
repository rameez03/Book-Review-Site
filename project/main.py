from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from . import db
from .models import LibraryModel, Comments, Ratings

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

main = Blueprint('main', __name__)

def num_sim(n1, n2):
    if n1==0 and n2==0:
        return 1
    return 1 - (abs(n1 - n2) / (n1 + n2))

def recommendation(bookid):
    #store data
    ids=[]
    titles = []
    img_urls = []
    authors = []
    subjects = []
    isbns = []
    publishers = []
    ratings = []
    
    books= LibraryModel.query.all()
    for b in books:
        ids.append(int(b.bookid))
        titles.append(b.title)
        img_urls.append(b.image_url)
        authors.append(b.authors)
        subjects.append(b.subjects)
        isbns.append(b.isbn)
        publishers.append(b.publisher)
        ratings.append(b.ratings)
        
    # fill the list

    df = pd.DataFrame()
    df['bookid']=ids
    df["title"] = titles
    df["image_url"] = img_urls
    df["authors"] = authors
    df["subjects"] = subjects
    df["isbn"] = isbns
    df["publisher"] = publishers
    df["ratings"] = ratings 
   
    def num_sim(n1, n2):
        """ calculates a similarity score between 2 numbers """
        if n1==0 and n2==0:
            return 1
        return 1 - (abs(n1 - n2) / (n1 + n2))

    features = []
    for i in range(0,df.shape[0]):
        features.append(df['title'][i] + ' '+df['authors'][i]+' '+df['publisher'][i])
    df['combined_features']=features
    z=df['combined_features'].apply(str).tolist()
    coun_vect = CountVectorizer(lowercase=False)
    cm=coun_vect.fit_transform(z)
    #get the cosine similarity matrix from the count matrix 
    cs=cosine_similarity(cm)

    number=4
    #Find the book id of the book that user likes
    Title=""
    for i in range(len(df)):
        if(df['bookid'][i]==bookid):
            Title=df['title'][i]
                    
    score_rate = []
    col=df['ratings']
    n1=df['ratings'][bookid-1]
    for i in range(len(col)):
        if(bookid-1 == i):
            score_rate.append(1)
        score_rate.append(num_sim(int(n1),int(col[i])))

    scores=list(enumerate(cs[bookid]))
    score_rate=list(enumerate(score_rate))

    scores.remove(scores[bookid-1])
    score_rate.remove(score_rate[bookid-1])

    #sort the list of similar books 
    score2=[]

    for i in range(len(scores)):
        score2.append(list(scores[i]))
        score2[i][1]=score2[i][1]*score_rate[i][1]
    sorted_scores=sorted(score2,key=lambda x:x[1],reverse=True)
    
    j=0
    book_title=''
    book_id=-1
    recommended_books = []
    for item in sorted_scores:
        for i in range(len(df)):
            if(df['bookid'][i]==item[0]):
                book_title=df['title'][i]
                book_id=df['bookid'][i]
        if Title == book_title:
            number=number+1
            continue
        if(book_title=='' or book_id==-1):
            continue
        recommended_books.append([book_id , book_title])
        j=j+1
        if(j>=number):
            break
    return recommended_books

@main.route('/')
def index():
    # return render_template('index.html')
    return redirect(url_for('auth.login'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/home')
@login_required
def home():
    return render_template('landing.html')    

@main.route('/books')
@login_required
def books():
    page = request.args.get('page', 1, type=int)
    # books= LibraryModel.query.all()
    books = LibraryModel.query.paginate(page=page, per_page=12)
    return render_template('booklist.html',books= books)

@main.route('/book/<bookid>')
@login_required
def retrievebooks(bookid):
    recommended_books = recommendation(int(bookid))

    book = LibraryModel.query.filter_by(bookid=bookid).first()
    comments = Comments.query.filter_by(bookid=bookid).all()
    
    if book:
        return render_template('viewbook.html', book=book, recommended_books=recommended_books, comments=comments)
        # return ('book page')
    return f"Book with id={id} does not exist"

@main.route("/addrating/<book_id>", methods=['POST'])
@login_required
def addraring(book_id):
    inputrating = int(request.form['rating'])
    current_rating = Ratings.query.filter_by(bookid=book_id).filter_by(username=current_user.name)
    book = LibraryModel.query.filter_by(bookid=book_id)
    if current_rating.first() is None:
        old_rating = float(book.first().ratings)
        old_count = int(book.first().rating_count)
        new_count = old_count + 1
        new_rating = ((old_rating * old_count) + inputrating) / new_count
        book.update(dict(ratings=new_rating, rating_count=new_count))
        rating = Ratings(bookid=book_id, username=current_user.name, rating=inputrating)
        db.session.add(rating)
        db.session.commit()
    else:
        user_oldrating = int(current_rating.first().rating)
        if inputrating != user_oldrating:
            old_rating = float(book.first().ratings)
            old_count = int(book.first().rating_count)
            new_rating = old_rating + ((inputrating - user_oldrating) / old_count)
            book.update(dict(ratings=new_rating))
            current_rating.update(dict(rating=inputrating))
            db.session.commit()
    
    return redirect(url_for('main.retrievebooks', bookid=book_id))


@main.route("/addcomment/<book_id>", methods=['POST'])
@login_required
def addcomment(book_id):
    text = request.form.get('review')
    print(text)
    print(book_id)

    if not text:
        flash('Review cannot be empty.', category='error')
    else:
        comment = Comments(bookid=book_id, username=current_user.name, comment=text)
        db.session.add(comment)
        db.session.commit()
        flash('Review added.', category='success')
    #     post = Post.query.filter_by(id=post_id)
    #     if post:
    #         comment = Comment(
    #             text=text, author=current_user.id, post_id=post_id)
    #         db.session.add(comment)
    #         db.session.commit()
    #     else:
    #         flash('Post does not exist.', category='error')

    return redirect(url_for('main.retrievebooks', bookid=book_id))