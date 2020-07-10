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


def day_basket_list(day: date):
    day_start = datetime.combine(day, datetime.min.time())
    day_end = datetime.combine(day, datetime.max.time())
    q_string = f"SELECT FUSER_ID, ORDER_ID, COUNT(*) " \
               f"FROM(" \
               f"SELECT * FROM sitemanager.b_sale_basket " \
               f"WHERE DATE_INSERT >='{day_start}' AND DATE_INSERT <='{day_end}' " \
               f"ORDER BY id DESC)sub " \
               f"GROUP BY FUSER_ID, ORDER_ID ORDER BY FUSER_ID ASC"
    db_cursor.execute(q_string)

    for column in db_cursor.fetchall():
        # print(column)
        if (column[1] is None):
            collect_write_aband_order(column[0], column[2], day)
        else:
            collect_write_norm_order(column[0], column[1], column[2])


def collect_write_aband_order(f_user, count, basket_date):
    pass
    # print('Bad ', f_user)


def collect_write_norm_order(f_user, order_id, count):
    """
    from b_sale_order: DATE_INSERT
    from b_user: (if not exist)
    from b_sale_basket: products
    :param f_user:
    :param order_id:
    :param count:
    :return:
    """
    # toDo update order if already in DB

    order = session.query(Order).filter(Order.number == order_id).scalar()
    if order is not None:
        print('Here it is! Order: ', order_id)
        return

    q_string = f"SELECT DATE_INSERT, USER_ID, PRICE, PRICE_DELIVERY, CANCELED, STATUS_ID  " \
               f"FROM sitemanager.b_sale_order where ID = {order_id}"
    db_cursor.execute(q_string)
    # print('Good', order_id, f_user)
    bso_res = db_cursor.fetchall()[0]

    correct_status = 1
    if bso_res[4] == 'Y' or bso_res[5] == 'CF':
        correct_status = 2

    correct_date = bso_res[0] + timedelta(hours=4)

    q_string = f"SELECT NAME, LAST_NAME, EMAIL, PERSONAL_PHONE FROM sitemanager.b_user WHERE ID = {bso_res[1]}"
    db_cursor.execute(q_string)
    bu_res = db_cursor.fetchall()[0]

    c_order = Order(date=correct_date, b_fuser_id=f_user, number=order_id,
                    delivery_price=bso_res[3], order_status=correct_status, b_status_id=bso_res[5], total_sum=bso_res[2],
                    total_quantity=3)
    customer = session.query(Customer).filter(Customer.bit_id == bso_res[1]).scalar()
    if customer is not None:
        c_order.customer = customer
    else:
        c_order.customer = Customer(bit_id=bso_res[1], name=bu_res[0], last_name=bu_res[1], e_mail=bu_res[2],
                                    phone=bu_res[3], is_1C_resident=False)

    q_string = f"SELECT NAME, QUANTITY, PRICE FROM sitemanager.b_sale_basket WHERE ORDER_ID = {order_id}"
    db_cursor.execute(q_string)

    total_quantity = 0
    for prd in db_cursor.fetchall():
        c_order.products.append(Product(name=prd[0], quantity=prd[1], price=prd[2]))
        total_quantity += prd[1]
    c_order.total_quantity = total_quantity


    session.add(c_order)
    session.commit()


# d = date(year=2020, month=6, day=18) - timedelta(0)
# day_basket_list(d)

for i in range(10):
    d = date(year=2020, month=6, day=23) - timedelta(i)
    day_basket_list(d)
