from sqlalchemy.orm import backref
from cem_package import db
from flask_login import UserMixin 
from datetime import datetime

class users(db.Model, UserMixin):   
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    fname = db.Column(db.String(150), nullable=True)
    lname = db.Column(db.String(150), nullable=True)
    smh = db.Column(db.String(150), nullable=True)
    ph_no = db.Column(db.Numeric)
    inf_email = db.Column(db.String(150), unique=True)
    acc_handler_gender = db.Column(db.String(150), nullable=True)
    password = db.Column(db.String(150))
    ah_email = db.Column(db.String(150), nullable=True)
    comp_email = db.Column(db.String(150), nullable=True, unique=True)
    comp_website = db.Column(db.String(150), nullable=True)
    acc_handler_desig = db.Column(db.String(150), nullable=True)
    acc_handler_name = db.Column(db.String(150), nullable=True)
    comp_name = db.Column(db.String(150), unique=False)
    categories = db.Column(db.String(200), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(150))
    acc_type = db.Column(db.String(50))
    infl_pic = db.Column(db.Text, nullable=True)
    mimetype = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Update the relationship to use the 'user_id' foreign key in 'news'
    news = db.relationship('news', backref='owner', lazy=True)

class news(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)  # Category of the news
    headline = db.Column(db.String(255), nullable=False)  # Headline of the news article
    url = db.Column(db.String(500), nullable=False)  # URL to the full news article
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Publication date
    text = db.Column(db.Text, nullable=True)  # Full text of the news article
    text_summary = db.Column(db.Text, nullable=True)  # Summary of the article's text
    author = db.Column(db.String(150), nullable=True)  # Author of the article
    sentiment = db.Column(db.String(50), nullable=True)  # Sentiment analysis result (e.g., 'Positive', 'Negative', 'Neutral')
    
    # Add a foreign key that references 'users.id'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<News {self.headline}>'
