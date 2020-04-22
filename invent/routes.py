from flask import url_for, request, redirect, render_template
from invent import app
from invent.forms import Login, New_Order, MakeOrder, NewUser
from invent.models import Tempdb, Order, Items


@app.route('/')
def index():
    form = Login()
    return render_template('index.html', form=form)


@app.route('/order', methods=['GET', 'POST'])
def order():
    items = []
    form_1 = New_Order()
    form_2 = MakeOrder()
    if form_1.validate_on_submit():
        item_order = Order(
            items=form_1.item.data, quamtity=form_1.quantity.data, item_type=form_1.item_type.data)
    return render_template('order.html', title='Make Order', form_1=form_1, form_2=form_2)


@app.route('/history')
def history():
    return render_template('history.html', title='Order History')


@app.route('/catalogue')
def catalogue():
    return render_template('catalogue.html', title='Catalogue')


@app.route('/newuser')
def newuser():
    form = NewUser()
    return render_template('adduser.html', title='Add User', form=form)
