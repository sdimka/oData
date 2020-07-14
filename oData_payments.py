from getCostPriceOfSalary import request_jason_data
from datetime import datetime, date, timedelta
from order_repo import Order, Product, Customer, Customer1c, session

# Номер заказа из БД + статус оплаты -> ID заказа 1С -> Чек по ID заказа, если нет Оплата от покупателя ПК
#  Закрытие заказов покупателей

#  ААЭС0011272 - на сайте оплачен, оплаты ПК нет
#  ААЭС0011283 - есть ОПК, на сайте оплаты нет???

#  http://192.168.1.108/mayco/odata/standard.odata/Document_ЧекККМ&$top=1&$format=json


def main():
    #  0:00:00.063795 - without select
    #  0:00:00.034555 - with select

    start_d = datetime.combine(date(year=2020, month=5, day=1), datetime.min.time())
    end_d = start_d + timedelta(days=7)


    # список заказов с сайта
    order_list = session.query(Order).filter(Order.date >= start_d).filter(Order.date <= end_d)

    # список чеков +- неделя
    ord_start_d = start_d - timedelta(days=7)
    ord_end_d = end_d + timedelta(days=7)
    recipe_list = recipe_by_period(ord_start_d, ord_end_d)

    # список ОПК +- неделя
    opk_start_d = start_d - timedelta(days=7)
    opk_end_d = end_d + timedelta(days=7)
    opk_list = opk_by_period(opk_start_d, opk_end_d)

    # список заказов 1С день в день
    order_1c_list = orders_by_period(start_d, end_d)


    # для каждого заказа с сайта проверяем и записываем
    for order in order_list:
        if order.order_status == 2:
            pass




def orders_by_period(start_date: datetime, end_date: datetime):
    s_date = f"{start_date.year}-{('%02d' % start_date.month)}-{('%02d' % start_date.day)}T00:00:00"
    e_date = f"{end_date.year}-{('%02d' % end_date.month)}-{('%02d' % end_date.day)}T23:59:59"

    catalog = f"Document_ЗаказПокупателя"
    select = 'Ref_Key, Number, Date, Б_Идентификатор'
    filt = "Number eq 'ААЭС0009820'"
    # filt = "Number eq 'ААЭС0009820'" Б_Идентификатор
    filt = f"Date ge datetime'{s_date}' and Date le datetime'{e_date}' and Б_Идентификатор ne ''"
    req = request_jason_data(catalog, select, filt)
    return req['value']


def recipe_by_period(start_date: datetime, end_date: datetime):
    s_date = f"{start_date.year}-{('%02d' % start_date.month)}-{('%02d' % start_date.day)}T00:00:00"
    e_date = f"{end_date.year}-{('%02d' % end_date.month)}-{('%02d' % end_date.day)}T23:59:59"

    catalog = f"Document_ЧекККМ"
    select = 'Ref_Key, Number, Date, ЗаказОснование_Key'
    # filt = f"ЗаказОснование_Key eq guid'{req['value'][0]['Ref_Key']}'"
    filt = f"Date ge datetime'{s_date}' and Date le datetime'{e_date}' and ЗаказОснование_Key ne guid'00000000-0000-0000-0000-000000000000'"
    req = request_jason_data(catalog, select, filt)
    return req['value']


def opk_by_period(start_date: datetime, end_date: datetime):
    s_date = f"{start_date.year}-{('%02d' % start_date.month)}-{('%02d' % start_date.day)}T00:00:00"
    e_date = f"{end_date.year}-{('%02d' % end_date.month)}-{('%02d' % end_date.day)}T23:59:59"

    catalog = 'Document_ОплатаОтПокупателяПлатежнойКартой'
    select = 'Date, ДокументОснование, РасшифровкаПлатежа'
    filt = f"Date ge datetime'{s_date}' and Date le datetime'{e_date}' and ИТС_ОрганизацияДляПечати_Key eq guid'1aae1c91-3e2d-11df-9651-005056c00008'"
    req2 = request_jason_data(catalog, select, filt)
    return req2['value']


if __name__ == '__main__':
    main()
