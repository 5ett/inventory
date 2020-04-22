from invent import db
from datetime import datetime


# @osyrus.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, unique=True, nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)
    item_type = db.Column(db.String(100), nullable=False)
    item_description = db.Column(db.String(300), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    item_types = db.Column(db.String, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow().date())
    made_by = db.Column(db.String, nullable=False)


class Tempdb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tem_items = db.Column(db.String, nullable=False)
    made_by = db.Column(db.String, nullable=False)
