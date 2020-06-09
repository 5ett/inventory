from invent import db, osyrus
from datetime import datetime
from flask_login import UserMixin


@osyrus.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)
    order = db.relationship('Order', backref='ordered_by', lazy='dynamic')
    made_by = db.relationship('Tempdb', backref='made_by', lazy='dynamic')


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, unique=True, nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)
    item_type = db.Column(db.String(100), nullable=False)
    item_description = db.Column(db.String(300), nullable=False)
    item_status = db.Column(db.String, nullable=False, default='In Stock')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items_n_quantities = db.Column(db.String, nullable=False)
    item_types = db.Column(db.String, nullable=False)
    order_status = db.Column(db.String, nullable=False, default='Pending')
    order_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow().date())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Tempdb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.Integer, db.ForeignKey('user.name'))
