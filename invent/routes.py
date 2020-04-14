from flask import url_for, request, redirect, render_template
from invent import app
from invent.forms import Login


@app.route('/')
def index():
    form = Login()
    return render_template('index.html', title='Index', form=form)


@app.route('/login')
def login():
    return render_template('login.html')
