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
    order_owner = db.relationship('Order', backref='maker', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.name}', '{self.email}', '{self.username}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items_n_quantities = db.Column(db.String, nullable=False)
    item_types = db.Column(db.String, nullable=False)
    order_status = db.Column(db.String, nullable=False, default='Pending')
    order_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow().date())
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Order('{self.items_n_quantities}', '{self.item_types}', '{self.order_date}')"


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, unique=True, nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)
    item_type = db.Column(db.String(40), nullable=False)
    item_description = db.Column(db.String(40), nullable=False)
    item_status = db.Column(db.String, nullable=False, default='In Stock')

    def __repr__(self):
        return f"Items('{self.item_name}', {self.item_quantity}, '{self.item_type}', '{self.item_status}')"


class Tempdb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Tempdb('{self.item}', '{self.item_types}', '{self.temp_order_owner}')"
