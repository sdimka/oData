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


def last_baskets():
    q_string = 'SELECT FUSER_ID, COUNT(*) ' \
               'FROM(' \
               'SELECT * FROM sitemanager.b_sale_basket ORDER BY id DESC LIMIT 10' \
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



# bask_list = last_baskets()
order_inf_from_bit(734422)
order_inf_from_bit(642064)

