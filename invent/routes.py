from flask_login import login_user, logout_user, current_user, login_required
from invent.forms import Login, New_Order, NewUser, Updateitems, AddnewItem
from flask import url_for, request, redirect, render_template, flash
from invent.models import Order, Items, User, Tempdb
from invent.other_functions import cap, check_item, today

from invent import app, guard, db
from collections import Counter


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
    return render_template('index.html', form=form, in_stock=in_stock, title='The Inventory')


# fill order form
@app.route('/order', methods=['GET', 'POST'])
def order():
    new_request = AddnewItem()
    form = New_Order()
    if form.validate_on_submit():
        order_item = cap(form.item.data)
        item_search = Items.query.filter_by(item_name=order_item).first()
        referenced_type = item_search.item_type
        # refrenced_description = item_search.item_description

        if item_search:
            new_temp_order = Tempdb(
                item=order_item, quantity=form.quantity.data, owner=current_user.id)
            db.session.add(new_temp_order)
            db.session.commit()
            # flash('Item Successfully Added', "success")
            return redirect(url_for('order'))

    if new_request.validate_on_submit():
        new_request_item = cap(new_request.item.data)
        new_request_type = cap(new_request.item_type.data)
        new_request_description = cap(new_request.item_description.data)
        add_new_request = Items(
            item_name=new_request_item, item_quantity=new_request.quantity.data, item_type=new_request_type, item_description=new_request_description, item_status='Request', referenced_type=referenced_type, today=today
        )
        db.session.add(add_new_request)
        db.session.commit()
        flash('Your Request Has Been Received', 'success')

    order_progress = Tempdb.query.filter_by(owner=current_user.id).all()
    order_size = len(order_progress)
    in_stock = Items.query.order_by(Items.id.desc()).all()
    out_of_stock = Items.query.filter_by(
        item_quantity=0).order_by(Items.id.desc()).all()
    user_orders = Order.query.filter_by(
        owner=current_user.id).order_by(Order.order_date.desc()).all()
    return render_template('order.html', form=form, order_progress=order_progress, in_stock=in_stock, out_of_stock=out_of_stock, user_orders=user_orders, new_request=new_request, size=order_size, title='Make Order')


@app.route('/cancelorder/<int:order_id>', methods=['GET', 'POST'])
def cancelorder(order_id):
    cancel_items = Tempdb.query.get_or_404(order_id)
    db.session.delete(cancel_items)
    db.session.commit()
    return redirect(url_for('order'))


# make a new order / shaky logic/ am I depressed?
@app.route('/make_order')
def make_order():
    # item_types_list = []
    temporay_order = Tempdb.query.filter_by(owner=current_user.id).all()
    for order in temporay_order:
        item_ck = Items.query.filter_by(item_name=order.item).first()
        new_order = Order(
            items_n_quantities=f'{order.item}, {order.quantity}', item_types=f'{item_ck.item_type}', owner=current_user.id)
        db.session.add(new_order)
        item_ck.item_quantity = int(
            item_ck.item_quantity) - int(order.quantity)
        db.session.delete(order)
    db.session.commit()
    flash('order successful', 'succes')
    return redirect(url_for('order'))


@app.route('/pending_orders', methods=['POST', 'GET'])
def pending_orders():
    all_orders = Order.query.order_by(Order.id).all()
    return render_template('view_orders.html', all_orders=all_orders, title='Pending Orders')


@app.route('/history')
def history():
    receipts = Counter(Order.query.filter_by(
        owner=current_user.id).order_by(Order.order_date.desc()).all())
    return render_template('history.html', receipts=receipts, title=current_user.username)


@app.route('/catalogue')
def catalogue():
    in_stock = Items.query.order_by(Items.id.desc()).all()
    return render_template('catalogue.html', title='Catalogue', in_stock=in_stock)


# add a new user/ only available to admin
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
        return redirect(url_for('newuser'))
    return render_template('adduser.html', title='Add New User', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/users', methods=['GET', 'POST'])
def users():
    all_users = User.query.all()
    return render_template('manage_users.html', all_users=all_users, title='Manage Users')


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
        return redirect(url_for('additem'))

    elif form_2.validate_on_submit():
        try:
            item2 = cap(form_2.item.data)
            item_type = cap(form_2.item_type.data)
            item_desc = cap(form_2.item_description.data)
            new_item = Items(item_name=item2, item_quantity=form.quantity.data,
                             item_type=item_type, item_description=item_desc)
            # new_item = Items(item_name=form_2.item.data, item_quantity=form.quantity.data,
            #                  item_type=form_2.item_type.data, item_description=form_2.item_description.data)
            db.session.add(new_item)
            db.session.commit()
            flash('new item added to inventory', 'info')
        except:
            flash('failed to add new item to inventory', 'danger')
        return redirect(url_for('additem'))

    added_stock = Items.query.order_by(Items.id.desc()).all()
    out_of_stock = Items.query.filter_by(
        item_quantity=0).order_by(Items.id.desc()).all()
    return render_template('additem.html', title='Update Iventory', form=form, form_2=form_2, out_of_stock=out_of_stock, added_stock=added_stock)


@app.route('/loop')
def loop():
    return redirect('order')
