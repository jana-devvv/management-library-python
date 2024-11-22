from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app import app,db
from app.models import Book, User, Loan
from app.forms import AddBookForm, RegisterForm, LoginForm

# Book
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

    return render_template('pages/home.html', title='Home | JD', books=books, search_query=search_query)

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
    return render_template('book/add_book.html', title='Add Book | JD', form=form)

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
    return render_template('book/edit_book.html', title='Edit Book | JD', form=form, book=book)

@app.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully', 'danger')
    return redirect(url_for('home'))

# Loan book
@app.route('/my_loans')
@login_required
def my_loans():
    loans = Loan.query.filter_by(user_id=current_user.id).all()
    return render_template('pages/my_loans.html', loans=loans, timedelta=timedelta)

@app.route('/loan/<int:book_id>', methods=['GET', 'POST'])
@login_required
def loan_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        new_loan = Loan(user_id=current_user.id, book_id=book.id)
        db.session.add(new_loan)
        db.session.commit()
        flash(f'Book {book.title} was successfully borrowed', 'success')
        return redirect(url_for('home'))
    return render_template('book/loan_book.html', book=book)

# Return book
@app.route('/return/<int:loan_id>', methods=['GET', 'POST'])
@login_required
def return_book(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    if loan.user_id == current_user.id:
        loan.status = 'returned'
        loan.return_date = datetime.utcnow()
        db.session.commit()
        flash(f'Book {loan.book.title} was returned', 'success')
        return redirect(url_for('home'))
    else:
        flash("You can't returned this book", 'danger')
        return redirect(url_for('home'))

# Auth
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your credentials!')
    return render_template('auth/login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout successfully', 'info')
    return redirect(url_for('pages/home'))