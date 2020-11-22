# import sys
# from invent.models import User, Order, Items, Tempdb


# def table(tbl, instance):
#     instance = tbl.query.all()
#     length = len(instance)
#     print(length)
#     [element := print(table_element) for table_element in instance]


# # table(User, 'users')
# args_1 = sys.argv[1]
# args_2 = sys.argv[2]

# print(table(args_1, args_2))

pw_hsh = guard.generate_password_hash('codecommander').decode('utf8')
new_user = User(name='Code Commander', email='huntbokx@protonmail.ch',
                username='codecmnd', password=pw_hsh)
db.session.add(new_user)
db.session.commit()
