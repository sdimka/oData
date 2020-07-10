from order_repo import Order, Product, Customer, session
from datetime import datetime, date, timedelta

import mysql.connector

db_connection = mysql.connector.connect(
  host="192.168.1.180",
  user="root",
  passwd="mypassword",
  database="sitemanager"
)
db_cursor = db_connection.cursor()


def last_baskets():  # DESC LIMIT 500
    q_string = 'SELECT FUSER_ID, COUNT(*) ' \
               'FROM(' \
               'SELECT * FROM sitemanager.b_sale_basket ORDER BY id DESC' \
               ')sub ' \
               'GROUP BY FUSER_ID ' \
               'ORDER BY FUSER_ID ASC'
    db_cursor.execute(q_string)
    return [column[0] for column in db_cursor.fetchall()]


def order_inf_from_bit(fuser_id):
    q_string = f"SELECT ORDER_ID, PRICE, NAME, QUANTITY FROM sitemanager.b_sale_basket WHERE FUSER_ID ='{fuser_id}'"
    db_cursor.execute(q_string)
    basket_data = []
    for column in db_cursor.fetchall():
        basket_data.append(column)
    #  если ORDER_ID не Null
    print(basket_data[0][0])
    q_string = f"SELECT DATE_INSERT, PRICE, USER_ID, CANCELED, STATUS_ID FROM b_sale_order WHERE ID ="


double_list = []


def search_double(fuser_id):
    q_string = f"SELECT ORDER_ID, PRICE, NAME, QUANTITY FROM sitemanager.b_sale_basket WHERE FUSER_ID ='{fuser_id}'"
    db_cursor.execute(q_string)
    basket_data = []
    for column in db_cursor.fetchall():
        basket_data.append(column)
    asa = [val[0] for val in basket_data]
    if len(set(asa)) > 1:
        double_list.append(fuser_id)


def search_double_null(fuser_id):
    q_string = f"SELECT ORDER_ID, PRICE, NAME, QUANTITY, SORT FROM sitemanager.b_sale_basket WHERE FUSER_ID ='{fuser_id}'"
    db_cursor.execute(q_string)
    basket_data = []
    for column in db_cursor.fetchall():
        if column[0] is None:
            basket_data.append(column[4])
    if len(basket_data) != len(set(basket_data)):
        double_list.append(fuser_id)


def basket_by_day(day: date):
    day_start = datetime.combine(day, datetime.min.time())
    day_end = datetime.combine(day, datetime.max.time())
    q_string = f"SELECT FUSER_ID, DATE_INSERT, ORDER_ID, PRICE, NAME, QUANTITY, SORT FROM sitemanager.b_sale_basket WHERE DATE_INSERT >='{day_start}' AND DATE_INSERT <='{day_end}'"
    db_cursor.execute(q_string)

    for column in db_cursor.fetchall():
        print(column)

# bask_list = last_baskets()

# order_inf_from_bit(734422)
# order_inf_from_bit(642064)

d = date(year=2020, month=6, day=18) - timedelta(0)
basket_by_day(d)

# for b in bask_list:
#     search_double_null(b)

print(double_list)
