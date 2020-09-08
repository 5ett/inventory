from flask_wtf import FlaskForm
from flask_login import current_user
from invent.other_functions import cap
from invent.models import User, Items, Tempdb
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField


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
        cap_item = cap(item.data)
        check_item = Items.query.filter_by(item_name=cap_item).first()
        check_order = Tempdb.query.filter_by(owner=current_user.id).all()
        if not check_item:
            raise ValidationError("item is out of stock or dooesn't exist")
        if check_order:
            for order in check_order:
                if cap_item in order.item:
                    raise ValidationError(
                        'you have already made a similar order')

            def validate_quantity(self, quantity):
                # check_item_quantity = Items.query.filter_by(
                #     item_name=item.data).first()
                if quantity.data > check_item.item_quantity or check_item.item_quantity == 0:
                    raise ValidationError(
                        'you request is absurd and cannot be provided')


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

    def validate_item(self, item):
        item_check = Items.query.filter_by(item_name=item.data).first()
        if item_check:
            raise ValidationError(
                'item already in database. use the first form')
