from sqlalchemy import func
from app import db

class Accountants(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    hash = db.Column(db.Text, unique=True, nullable=False)
    current_balance = db.Column(db.Float, nullable=False, default=0)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    email_address = db.Column(db.Text, unique=True, nullable=False)
    hash = db.Column(db.Text, unique=True, nullable=False)
    accountant_id = db.Column(db.Integer, db.ForeignKey('accountants.id'), nullable=False)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    transaction = db.Column(db.Text, nullable=False)
    product_name = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Float, nullable=True)
    price = db.Column(db.Float, nullable=True)
    value = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, default=func.now(), nullable=False)
    accountant_id = db.Column(db.Integer, db.ForeignKey('accountants.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
     
class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    product_name= db.Column(db.Text, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=True)
    price = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    accountant_id = db.Column(db.Integer, db.ForeignKey('accountants.id'), nullable=False)

db.create_all()