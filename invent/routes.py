from flask_login import login_user, logout_user, current_user, login_required
from invent.forms import Login, New_Order, NewUser, Updateitems, AddnewItem
from flask import url_for, request, redirect, render_template, flash
from invent.models import Order, Items, User, Tempdb
from invent.other_functions import cap
from invent import app, guard, db
from collections import Counter
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Login()
    if form.validate_on_submit():
        user_auth = User.query.filter_by(email=form.email.data).first()
        if user_auth and guard.check_password_hash(user_auth.password, form.password.data):
            login_user(user_auth)
        else:
            flash('invalid credentials, try logging in again', 'danger')
    in_stock = Items.query.order_by(Items.id.desc()).all()
    return render_template('index.html', form=form, in_stock=in_stock)


@app.route('/order', methods=['GET', 'POST'])
def order():
    form = New_Order()
    if form.validate_on_submit():
        order_item = cap(form.item.data)
        item_search = Items.query.filter_by(item_name=order_item).first()
        if item_search:
            new_temp_order = Tempdb(
                item=order_item, quantity=form.quantity.data)
            db.session.add(new_temp_order)
            db.session.commit()
    order_progress = Tempdb.query.filter_by(user_name=current_user.name).all()
    in_stock = Items.query.order_by(Items.id.desc()).all()
    out_of_stock = Items.query.filter_by(
        item_quantity=0).order_by(Items.id.desc()).all()
    return render_template('order.html', form=form, order_progress=order_progress, in_stock=in_stock, out_of_stock=out_of_stock, title='Make Order')


@app.route('/cancelorder/<int:order_id>', methods=['GET', 'POST'])
def cancelorder(order_id):
    cancel_items = Tempdb.query.get_or_404(order_id)
    db.session.delete(cancel_items)
    db.session.commit()
    return redirect(url_for('order'))


@app.route('/make_order')
def make_order():
    items_n_qtty = {}
    item_types_list = []
    temp = Tempdb.query.filter_by(made_by=current_user.name).all()
    for temporary_order in temp:
        items_n_qtty[temporary_order.item] = int(temporary_order.quantity)
        check_item_type = Items.query.filter_by(
            item_name=temporary_order.item).first()
        check_item_type.item_quantity = int(
            check_item_type.item_quantity) - int(temporary_order.quantity)
        item_types_list.append(check_item_type.item_type)
        db.session.delete(temporary_order)
    new_order = Order(items_n_quantities=items_n_qtty,
                      item_types=item_types_list)
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('order'))


@app.route('/pending_orders', methods=['POST', 'GET'])
def pending_orders():
    all_orders = Order.query.order_by(Order.id).all()
    return render_template('view_orders.html', all_orders=all_orders, title='Pending Orders')


@app.route('/history')
def history():
    receipts = Counter(Order.query.filter_by(
        user_id=current_user.id).order_by(Order.order_date.desc()).all())
    return render_template('history.html', receipts=receipts, title='Profile & History')


@app.route('/catalogue')
def catalogue():
    in_stock = Items.query.order_by(Items.id.desc()).all()
    return render_template('catalogue.html', title='Catalogue', in_stock=in_stock)


@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    form = NewUser()
    if form.validate_on_submit():
        fullname = f'{form.first_name.data} {form.last_name.data}'
        passwd = guard.generate_password_hash(
            form.password.data).decode('utf8')
        new_user = User(name=fullname, email=form.email.data,
                        username=form.username.data, password=passwd)

        db.session.add(new_user)
        db.session.commit()
        flash('user details added succesfully', 'success')
    else:
        flash('failed to add user, try again', 'succes')
    return render_template('adduser.html', title='Add User', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/users', methods=['GET', 'POST'])
def users():
    all_users = User.query.all()
    return render_template('manage_users.html', all_users=all_users, title='Users')


# adding items to and updating inventory
@app.route('/additem', methods=['GET', 'POST'])
def additem():
    form = Updateitems()
    form_2 = AddnewItem()
    if form.validate_on_submit():
        item = cap(form.item.data)
        item_update = Items.query.filter_by(item_name=item).first()
        if item_update:
            item_update.item_quantity = int(
                item_update.item_quantity) + int(form.quantity.data)
            db.session.commit()
            flash('item updated', 'success')
        else:
            flash('failed to update item', 'danger')
    elif form_2.validate_on_submit():
        item2 = cap(form_2.item.data)
        item_type = cap(form_2.item_type.data)
        item_desc = cap(form_2.item_description.data)
        new_item = Items(item_name=item2,
                         item_quantity=form.quantity.data, item_type=item_type, item_description=item_desc)
        # new_item = Items(item_name=form_2.item.data, item_quantity=form.quantity.data,
        #                  item_type=form_2.item_type.data, item_description=form_2.item_description.data)
        db.session.add(new_item)
        db.session.commit()
        flash('new item added to inventory', 'info')
    else:
        flash('failed to add new item to inventory', 'danger')
    added_stock = Items.query.order_by(Items.id.desc()).all()
    out_of_stock = Items.query.filter_by(
        item_quantity=0).order_by(Items.id.desc()).all()
    return render_template('additem.html', title='Update Iventory', form=form, form_2=form_2, out_of_stock=out_of_stock, added_stock=added_stock)
