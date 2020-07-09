from order_repo import Order, Product, Customer, session
from datetime import datetime, date, timedelta
from random import randint


# o1 = Order(date=datetime.now(), number=154)
# o1.customer = Customer(name='Ivanov Ivan', e_mail='sss@mmm.com')
# o1.products = [Product(name='Супер крем', quantity=2, price=25), Product(name='Супер ifvgeym', quantity=3, price=15)]
# session.add(o1)
# session.commit()


def fake_bd_gen():
    for a in range(10):
        dt = date.today() - timedelta(a)
        for i in range(25):
            o1 = Order(date=dt, number=154 + (i * a), isPayed=True, payType=1, total_sum=randint(50, 1500))
            o1.customer = Customer(name=f'Ivan {i}', last_name='Ivanov', e_mail='sss@mmm.com')
            o1.products = [Product(name='Супер крем', quantity=randint(1, 5), price=randint(50, 1500)),
                           Product(name='Супер ifvgeym', quantity=randint(1, 5), price=randint(50, 1500))]

            session.add(o1)
    session.commit()


def get_list():
    return session.query(Order)
