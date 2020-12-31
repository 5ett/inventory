import string
from invent.models import Items
from datetime import datetime


today = str(datetime.utcnow().date())
today = today.replace('-', '/')

print(today)


def cap(item):
    item = string.capwords(item)
    return item


def return_item_status():
    items_in_inventory = Items.query.all()
    for item in items_in_inventory:
        if item.item_quantity == 0:
            item.item_status = 'Out of Stock'
        else:
            item.item_status = 'In Stock'


return_item_status()


def check_item(item):
    check = Items.query.filter_by(item_name=item).first()
    return check
