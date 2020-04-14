from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextField
from wtforms.validators import DataRequired


class Login(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')


class Order(FlaskForm):
    item = StringField('item', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    add = SubmitField('add to order')


class MakeOrder(FlaskForm):
    items_qty = TextField('cart', validators=[DataRequired()])
    item_types = TextField('categories/ tags', validators=[DataRequired()])
    submit = SubmitField('make order')
