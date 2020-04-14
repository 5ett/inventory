from flask import url_for, request, redirect, render_template
from invent import app
from invent.forms import Login


@app.route('/')
def index():
    form = Login()
    return render_template('index.html', form=form)


@app.route('/order')
def order():
    return render_template('order.html', title='Make Order')


@app.route('/history')
def history():
    return render_template('history.html', title='Order History')


@app.route('/catalogue')
def catalogue():
    return render_template('catalogue.html', title='Catalogue')
