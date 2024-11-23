from app import db
from datetime import datetime, timedelta
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'
    
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_loan_user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', name='fk_loan_book_id'), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow())
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default="borrowed")
    loan_duration = 7

    user = db.relationship('User', backref=db.backref('loans', lazy=True))
    book = db.relationship('Book', backref=db.backref('loans', lazy=True, cascade='all, delete'))

    def __repr__(self):
        return f"Loan('{self.id}', '{self.book.title}', '{self.user.username}', '{self.loan_date}')"
    
    def get_due_date(self):
        return self.loan_date + timedelta(days=self.loan_duration)