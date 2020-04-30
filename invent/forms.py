from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from invent.models import User, Items, Tempdb
from flask_login import current_user


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


class New_Order(FlaskForm):
    item = StringField('search item', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    add = SubmitField('add to order')

    def validate_item(self, item):
        check_item = Items.query.filter_by(item_name=item.data).first()
        if not check_item:
            raise ValidationError("item is not in stock or dooesn't exist")


class MakeOrder(FlaskForm):
    # items_qty = TextAreaField('cart', validators=[DataRequired()])
    order_made_by = StringField('made by', validators=[DataRequired()])
    submit = SubmitField('make order')


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


class AddnewItem(FlaskForm):
    item = StringField('item', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    item_type = StringField('item type', validators=[DataRequired()])
    item_description = StringField(
        'item description', validators=[DataRequired()])
    submit = SubmitField('add item')

    def validate_item(self, item):
        item_check = Items.query.filter_by(item_name=item.data).first()
        if item_check:
            raise ValidationError(
                'item already in database. use the first form')
