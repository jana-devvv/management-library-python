from flask import render_template, redirect, url_for, flash, request
from app import app,db
from app.models import Book
from app.forms import AddBookForm

@app.route('/')
def home():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    if search_query:
        books = Book.query.filter(
            Book.title.ilike(f'%{search_query}%') | Book.author.ilike(f'%{search_query}%')
        ).paginate(page=page, per_page=5, error_out=False)
    else:
        books = Book.query.paginate(page=page, per_page=5, error_out=False)

    return render_template('home.html', title='Home | JD', books=books, search_query=search_query)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            year=form.year.data,
        )

        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_book.html', title='Add Book | JD', form=form)

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id) 
    form = AddBookForm()

    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.year = form.year.data
        db.session.commit()
        flash('Book updated successfully.', 'success')
        return redirect(url_for('home'))
    
    form.title.data = book.title
    form.author.data = book.author
    form.year.data = book.year
    return render_template('edit_book.html', title='Edit Book | JD', form=form, book=book)

@app.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully', 'danger')
    return redirect(url_for('home'))