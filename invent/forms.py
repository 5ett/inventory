from flask_wtf import FlaskForm
from flask_login import current_user
from invent.other_functions import cap
from invent.models import User, Items, Tempdb
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField, BooleanField, SelectField, DateField


class Login(FlaskForm):
    email = StringField('username', validators=[
        DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(
                "the user you entered doesn't exist")

    def validate_password(self, password):
        if password.errors:
            raise ValidationError('invalid password, try again!')


class Checkout(FlaskForm):
    first_name = StringField('first name', validators=[DataRequired()])
    last_name = StringField('last name', validators=[DataRequired()])

    email = StringField('email', validators=[Email()])
    address_1 = StringField('address line 1', validators=[DataRequired()])
    address_2 = StringField('adress line 2')

    country = SelectField('country', choices=[('Choose...'), ('Ghana')], validators=[DataRequired()])
    state = SelectField('state',choices=[('Choose...'), ('Takoradi'), ('Accra')], validators=[DataRequired()] )
    zip_code = IntegerField('zip', validators=[DataRequired(), Length(min=3, max=3)])
    address_confirm = BooleanField()
    # save_confirm = BooleanField()

    credit_card = BooleanField()
    debit_card  = BooleanField()
    paypal = BooleanField()
    card_name = StringField('name on card', validators=[DataRequired()])
    card_number = StringField('card number', validators=[DataRequired()])
    card_expiry = DateField('expiration', format='%d-%m-%Y', validators=[DataRequired()])
    cvv = IntegerField('cvv', validators=[DataRequired()])
    promo_code = StringField('promo code')


    submit = SubmitField('complete order')


class NewUser(FlaskForm):
    first_name = StringField('first name', validators=[DataRequired()])
    last_name = StringField('last name', validators=[DataRequired()])
    username = StringField('username', validators=[
                           DataRequired(), Length(min=6, max=15)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[
                             DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('add user')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'user already exists, redirect to login instead')
        elif email.errors:
            raise ValidationError('make sure you typed a correct email')

    def validate_password(self, password):
        if password.errors:
            raise ValidationError(
                'invalid password. either it is too long or too short ')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username exists already, choose another!')


class Updateitems(FlaskForm):
    item = StringField('item', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    submit = SubmitField('update')

    def validate_item(self, item):
        item_check = Items.query.filter_by(item_name=item.data).first()
        if not item_check:
            raise ValidationError('this is a new item. use the second form')

    def validate_quantity(self, quantity):
        if quantity.data == 0:
            raise ValidationError('zero quantity cannot be added to inventory')


class AddnewItem(FlaskForm):
    item = StringField('item', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    item_type = StringField('item type', validators=[DataRequired()])
    item_description = StringField(
        'item description', validators=[DataRequired()])
    submit = SubmitField('add item')
    second_sub = SubmitField('Submit for review and purchase')

    def validate_item(self, item):
        item_check = Items.query.filter_by(item_name=item.data).first()
        if item_check:
            raise ValidationError(
                'item already in database. use the first form')
