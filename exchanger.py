from order_repo import Order, Product, Customer, Customer1c, session
from datetime import datetime, date, timedelta

import mysql.connector

# db_connection = mysql.connector.connect(
#   host="192.168.1.180",
#   user="root",
#   passwd="mypassword",
#   database="sitemanager"
# )

db_connection = mysql.connector.connect(
  host="77.222.60.182",
  user="SD",
  passwd="EvH(psZ#V+y~w5",
  database="shpilkspb_bitrix"
)

db_cursor = db_connection.cursor()


def day_basket_list(day: date):
    day_start = datetime.combine(day, datetime.min.time())
    day_end = datetime.combine(day, datetime.max.time())
    q_string = f"SELECT FUSER_ID, ORDER_ID, COUNT(*) " \
               f"FROM(" \
               f"SELECT * FROM b_sale_basket " \
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
               f"FROM b_sale_order where ID = {order_id}"
    db_cursor.execute(q_string)
    # print('Good', order_id, f_user)
    bso_res = db_cursor.fetchall()[0]

    correct_status = 1
    if bso_res[4] == 'Y' or bso_res[5] == 'CF':
        correct_status = 2

    correct_date = bso_res[0] #  + timedelta(hours=4)

    q_string = f"SELECT NAME, LAST_NAME, EMAIL, PERSONAL_PHONE FROM b_user WHERE ID = {bso_res[1]}"
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

    q_string = f"SELECT NAME, QUANTITY, PRICE FROM b_sale_basket WHERE ORDER_ID = {order_id}"
    db_cursor.execute(q_string)

    total_quantity = 0
    for prd in db_cursor.fetchall():
        c_order.products.append(Product(name=prd[0], quantity=prd[1], price=prd[2]))
        total_quantity += prd[1]
    c_order.total_quantity = total_quantity

    session.add(c_order)
    session.commit()


total_find = 0
doubles = []
bad_phone_list = ['11111', '11111111111']


def compare_customers_by_phone(phone_number):
    global total_find
    global doubles
    global find_list
    if phone_number is not None and phone_number not in bad_phone_list:
        clear_phone_num = ''.join(x for x in phone_number if x.isdigit())
        search = "%{}%".format(clear_phone_num[1:])
        customer1c = session.query(Customer1c).filter(Customer1c.phone_for_search.like(search)).all()
        if len(customer1c) > 1:
            doubles.append([phone_number, clear_phone_num])
        if customer1c is not None:
            cur_customer1c: Customer1c = None
            for cust in customer1c:
                # Проверка и возврат того, кто свежее :)
                if cur_customer1c is None or cur_customer1c.dateCreate < cust.dateCreate:
                    cur_customer1c = cust
                    total_find = total_find + 1
            return cur_customer1c
    return None


def recheck_all_customers():
    customers = session.query(Customer).all()
    for customer in customers:
        new1c_customer = compare_customers_by_phone(customer.phone)
        if new1c_customer is not None:
            customer.customer1c = new1c_customer
            customer.is_1C_resident = True
            session.add(customer)
            session.commit()


def recheck_last_10_customers():
    # query = users.select().order_by(users.c.id.desc()).limit(5)
    customers = session.query(Customer).order_by(Customer.id.desc()).limit(10)
    for customer in customers:
        new1c_customer = compare_customers_by_phone(customer.phone)
        if new1c_customer is not None:
            customer.customer1c = new1c_customer
            customer.is_1C_resident = True
            session.add(customer)
            session.commit()


# d = date(year=2020, month=6, day=18) - timedelta(0)
# day_basket_list(d)

for i in range(5):
    d = date(year=2020, month=7, day=13) - timedelta(i)
    day_basket_list(d)

recheck_last_10_customers()
print(total_find)
for a in doubles:
    print(a)
