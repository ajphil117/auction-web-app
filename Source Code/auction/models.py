from . import db
from datetime import datetime
from flask_login import UserMixin

# User table in database
class User(db.Model, UserMixin ):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(), nullable=False)
    user_name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    address_line1 = db.Column(db.String(50), nullable=False)
    address_line2 = db.Column(db.String(50))
    state = db.Column(db.String(3), nullable=False)
    zip = db.Column(db.String(), nullable=False)

    comments = db.relationship('Comment', backref='user')
    watchlist = db.relationship('Watchlist', backref='user')
    items = db.relationship('Item', backref='user')

# Item table in database
class Item(db.Model):
    __tablename__ = 'items'
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(400))
    image = db.Column(db.String(400))
    genre = db.Column(db.String(20), nullable=False)
    platform = db.Column(db.String(20), nullable=False)
    classification = db.Column(db.String(5), nullable=False)
    release_year = db.Column(db.String(4), nullable=False)

    current_bid = db.Column(db.Numeric)
    starting_bid = db.Column(db.Numeric, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    date_listed = db.Column(db.DateTime, default=datetime.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='item')
    watchlist = db.relationship('Watchlist', backref='item')
    bids = db.relationship('Bid', backref='item')

    def __repr__(self):
        return "<name: {}>".format(self.title)

# Bid table in database
class Bid(db.Model):
    __tablename__='bids'
    id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Numeric, nullable=False)

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Watchlist table in database
class Watchlist(db.Model):
    __tablename__='watchlist'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

# Comment table in database
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    def __repr__(self):
        return "<comment: {}>".format(self.name)