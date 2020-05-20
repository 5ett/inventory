from flask import url_for, request, redirect, render_template, flash
import string
from datetime import datetime
from invent import app, guard, db
from invent.models import Tempdb, Order, Items, User
from flask_login import login_user, logout_user, current_user, login_required
from invent.forms import Login, New_Order, MakeOrder, NewUser, Updateitems, AddnewItem


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Login()
    if form.validate_on_submit():
        user_auth = User.query.filter_by(email=form.email.data).first()
        if user_auth and guard.check_password_hash(user_auth.password, form.password.data):
            login_user(user_auth)
        else:
            flash('invalid credentials, try logging in again', 'danger')

    return render_template('index.html', form=form)


@app.route('/order', methods=['GET', 'POST'])
def order():
    date = datetime.utcnow().date()
    key = []
    form_1 = New_Order()
    form_2 = MakeOrder()
    form_2.order_made_by.data = f'made by: {current_user.name}'
    if form_1.validate_on_submit():
        cap_item = string.capwords(form_1.item.data)
        key.append(cap_item)
        typpe = Items.query.filter_by(item_name=cap_item).first()
        key.append(typpe)
        temp_items = f'{cap_item}, {form_1.quantity.data}'
        item_order = Tempdb(tem_items=temp_items, made_by=current_user.name)
        db.session.add(item_order)
        db.session.commit()

        if form_2.validate_on_submit():
            new_quantity = int(typpe.item_quantity) - int(form_1.quantity.data)
            typpe.item_quantity = new_quantity
            # for element in order_progress:
            #     db.session.delete(element.id)
            main_order = Order(items=cap_item, quantity=form_1.quantity.data,
                               item_types=typpe.item_type, made_by=current_user.name)
            db.session.add(main_order)
            db.session.commit()
            flash('your order has been made. pendind approval', 'info')
            # return redirect(url_for('deletetemp'))

    order_progress = Tempdb.query.filter_by(made_by=current_user.name).all()
    pending_orders = Order.query.filter_by(made_by=current_user.name).all()
    recents = Items.query.order_by(Items.id.desc()).all()
    out_of_stock = Items.query.filter_by(item_quantity=0).all()
    return render_template('order.html', title='Make Order', form_1=form_1, form_2=form_2, date=date, recents=recents, out_of_stock=out_of_stock, order_progress=order_progress, pending_orders=pending_orders)


@app.route('/cancelorder/<int:order_id>', methods=['GET', 'POST'])
def cancelorder(order_id):
    cancel_items = Tempdb.query.get_or_404(order_id)
    db.session.delete(cancel_items)
    db.session.commit()
    return redirect(url_for('order'))


@app.route('/deletetemp')
def deletetemp():
    temp = Tempdb.query.filter_by(made_by=current_user.name).all()
    for temporary_order in temp:
        db.session.delete(temporary_order)
        db.session.commit()
    return redirect(url_for('order'))


@app.route('/history')
def history():
    return render_template('history.html', title='Order History')


@app.route('/catalogue')
def catalogue():
    return render_template('catalogue.html', title='Catalogue')


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


@app.route('/additem', methods=['GET', 'POST'])
def additem():
    form = Updateitems()
    form_2 = AddnewItem()
    if form.validate_on_submit():
        item = string.capwords(form.item.data)
        item_update = Items.query.filter_by(item_name=item).first()
        if item_update:
            item_update.item_quantity = item_update.item_quantity + form.quantity.data
            db.session.commit()
            flash('item updated', 'success')
        else:
            flash('failed to update item', 'danger')
    if form_2.validate_on_submit():
        item2 = string.capwords(form_2.item.data)
        item_type = string.capwords(form_2.item_type.data)
        item_desc = string.capwords(form_2.item_description.data)
        new_item = Items(item_name=item2,
                         item_quantity=form.quantity.data, item_type=item_type, item_description=item_desc)
        # new_item = Items(item_name=form_2.item.data, item_quantity=form.quantity.data,
        #                  item_type=form_2.item_type.data, item_description=form_2.item_description.data)
        db.session.add(new_item)
        db.session.commit()
        flash('new item added to inventory', 'info')
    else:
        flash('failed to add new item to inventory', 'danger')
    recents = Items.query.order_by(Items.id.desc()).all()
    return render_template('additem.html', title='Update Iventory', form=form, form_2=form_2, recents=recents)
