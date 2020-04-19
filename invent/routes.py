from flask import url_for, request, redirect, render_template
from invent import app
from invent.forms import Login, Order, MakeOrder


@app.route('/')
def index():
    form = Login()
    return render_template('index.html', form=form)


@app.route('/order', methods=['GET', 'POST'])
def order():
    items = []
    form_1 = Order()
    form_2 = MakeOrder()
    if form_1.is_submitted():
        items.append(
            f'{form_1.item.data}({form_1.quantity.data} {form_1.item_type.data})')
    for element in items:
        form_2.items_qty.data = element
    return render_template('order.html', title='Make Order', form_1=form_1, form_2=form_2)


@app.route('/history')
def history():
    return render_template('history.html', title='Order History')


@app.route('/catalogue')
def catalogue():
    return render_template('catalogue.html', title='Catalogue')
