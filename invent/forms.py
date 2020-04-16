from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class Login(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')


class Order(FlaskForm):
    item = StringField('search item', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    item_type = StringField('type', validators=[DataRequired()])
    add = SubmitField('add to order')


class MakeOrder(FlaskForm):
    items_qty = TextAreaField('cart', validators=[DataRequired()])
    order_made_by = StringField('made by', validators=[DataRequired()])
    submit = SubmitField('make order')
