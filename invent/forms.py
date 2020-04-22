from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from invent import db


class Login(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')

    def validate_email(self, email):
        user = db.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(
                "the ujser you entered doesn't exist")


class New_Order(FlaskForm):
    item = StringField('search item', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    item_type = StringField('type', validators=[DataRequired()])
    add = SubmitField('add to order')


class MakeOrder(FlaskForm):
    # items_qty = TextAreaField('cart', validators=[DataRequired()])
    order_made_by = StringField('made by', validators=[DataRequired()])
    submit = SubmitField('make order')


class NewUser(FlaskForm):
    first_name = StringField('first name', validators=[DataRequired()])
    last_name = StringField('last name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[
                             DataRequired(), Length(min=8, max=15)])
    submit = SubmitField('add user')

    def validate_email(self, email):
        user = db.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'user already exists, redirect to login instead')
        elif email.errors:
            raise ValidationError('make sure you typed a correct email')
