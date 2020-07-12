from getCostPriceOfSalary import request_jason_data
from datetime import datetime, date, timedelta

import sys, getopt

from order_repo import Customer1c, session

from sqlalchemy.orm.exc import MultipleResultsFound

#  Catalog_Контрагенты

# Запрос одного элемента:
# http://192.168.1.108/mayco/odata/standard.odata/InformationRegister_КонтактнаяИнформация&$top=1&$format=json

# ID Подразделения -> Чеки за период (лист Дисконтная карта) -> Контрагент (лист) -> Если нет, записываем в БД
#
# При загрузке с сайте контакты -> фильтр телефонов -> сравнение
#
total_list = []


def main(year, month, day, steps):

    for i in range(steps):
        d = date(year=year, month=month, day=day) + timedelta(days=i)

        start_date = f"{d.year}-{('%02d' % d.month)}-{('%02d' % d.day)}T00:00:00"
        end_date = f"{d.year}-{('%02d' % d.month)}-{('%02d' % d.day)}T23:59:59"

        print(start_date)

        for depart in dep_name_list.values():
            print(depart)
            # номера карт по чекам
            inf_card_nums = get_recipe_by_period(start_date, end_date,
                                                 get_department_id_by_code(depart))
            # номера клиентов из карт
            client_number_list = []
            for card_num in inf_card_nums:
                client_number_list.append(get_client_by_inf_card(card_num))

            #  Получаем клиента, если нет в базе, получаем контактную инфу, записываем
            for client_number in client_number_list:

                #  toDo !!! Ошибочные карты !!!!
                if client_number == '00000000-0000-0000-0000-000000000000':
                    break

                client_info = get_client_by_code(client_number)

                try:
                    customer1c = session.query(Customer1c).filter(Customer1c.code_1c == client_info['Code']).scalar()
                except MultipleResultsFound:
                    print('Error client code: ', client_info['Code'])
                    sys.exit('Error message')
                if customer1c is None:
                    reg_info = get_contact_reg_info(client_number)
                    new_customer = Customer1c(code_1c=client_info['Code'], id_1c=client_number,
                                              name=client_info['НаименованиеПолное'],
                                              dateCreate=client_info['ДатаСоздания'])

                    try:
                        new_customer.phone = reg_info[0][:25]
                        new_customer.phone_for_search = reg_info[1]
                    except TypeError:
                        new_customer.phone = ''
                        new_customer.phone_for_search = ''
                    session.add(new_customer)
                    session.commit()
    for error in total_list:
        print(error)

    # print(get_client_by_code('dbd853bf-a8e5-11e3-82a7-005056950007'))



def get_client_by_code(code):
    """
    Полезные поля: 'Description'/'НаименованиеПолное' , 'Code'
    'ДатаСоздания', 'СогласенНаРассылкуSMS', 'ДатаРождения', 'Пол', 'СогласенНаРассылкуEMAIL'
    :param code:
    :return:
    """
    catalog = f"Catalog_Контрагенты(Ref_Key=guid'{code}')"
    select = 'Code, НаименованиеПолное, ДатаСоздания'
    filt = ''
    req = request_jason_data(catalog, select, filt)

    # get_contact_reg_info(req['Ref_Key'])
    return req


def get_contact_reg_info(client_code):
    #  Использовать "ПолеПоискаПоТелефону"
    #  http://192.168.1.108/mayco/odata/standard.odata/InformationRegister_КонтактнаяИнформация
    #  (Объект='e7e66f48-cf94-11e7-a937-005056950094',
    #  Объект_Type='StandardODATA.Catalog_Контрагенты',
    #  Тип = 'Телефон',
    #  Вид=guid'968558ff-8fe0-40d0-84e3-ca694acbc839',
    #  Вид_Type='StandardODATA.Catalog_ВидыКонтактнойИнформации')
    catalog = f"InformationRegister_КонтактнаяИнформация(Объект='{client_code}', " \
              f"Объект_Type='StandardODATA.Catalog_Контрагенты', " \
              f"Тип = 'Телефон', " \
              f"Вид=guid'968558ff-8fe0-40d0-84e3-ca694acbc839', " \
              f"Вид_Type='StandardODATA.Catalog_ВидыКонтактнойИнформации')"
    select = ''
    filt = ''
    req = request_jason_data(catalog, select, filt)
    if 'Представление' in req:
        return [req['Представление'], req['ПолеПоискаПоТелефону']]
    else:
        total_list.append(client_code)


def get_recipe_by_period(start_date, end_date, dep_code):  # возвращаем дисконтные карты из чеков
    catalog = 'Document_ЧекККМ'
    select = ''
    filt = f"Date ge datetime'{start_date}' and Date le datetime'{end_date}' and Подразделение_Key eq guid'{dep_code}'"
    req = request_jason_data(catalog, select, filt)
    result = []
    for a in req['value']:
        if a['ДисконтнаяКарта_Key'] != '00000000-0000-0000-0000-000000000000':
            result.append(a['ДисконтнаяКарта_Key'])
    return result


def get_client_by_inf_card(card_num):  # код клиента из инф карты
    # Catalog_ИнформационныеКарты
    catalog = f"Catalog_ИнформационныеКарты(Ref_Key=guid'{card_num}')"
    select = ''
    filt = ''
    req = request_jason_data(catalog, select, filt)
    return req['ВладелецКарты']


def get_department_id_by_code(code):
    catalog = f"Catalog_Подразделения"
    select = ''
    filt = f"Code eq '{code}'"
    req = request_jason_data(catalog, select, filt)
    return req['value'][0]['Ref_Key']

# get_contr_by_code('АА0094687')
# get_client_by_code('e7e66f48-cf94-11e7-a937-005056950094')
# get_contact_reg_info('e7e66f48-cf94-11e7-a937-005056950094')


dep_name_list = {'Магазин Богатырский': 'ОП0000002'
    , 'Магазин Гулливер': 'ИТС000024',
                 'Магазин Заневский': 'ИТС000022', 'Магазин Лондон Молл': 'АА0000025',
                 'Магазин Порт Находка': 'АА0000026', 'Магазин РодеоДрайв': 'ИТС000027', 'Магазин Рубикон': 'ОП0000003',
                 'Магазин Французский бульвар': 'АА0000024', 'Магазин Звездный': 'АА0000018', 'Магазин Международный' : 'АА0000012',
                 'Магазин Нахимова': 'АА0000020', 'Магазин ОКей Пулково': 'ИТС000026', 'Магазин Оккервиль': 'ОП0000004',
                 'Магазин Стачек': 'АА0000022', 'Магазин Типанова': 'ЛС0000001', 'Магазин Электросила': 'ОП0000006',
                 }


def incom_args(args):
    opts, argm = getopt.getopt(args, 'y:m:d:s:', ['foperand', 'soperand'])
    ls = {}
    for opt, arg in opts:
        ls[opt] = int(arg)
    main(ls['-y'], ls['-m'], ls['-d'], ls['-s'])


if __name__ == '__main__':
    # print(get_client_by_code('0004e0e6-5824-11e7-ace4-005056950094'))
    # print(get_contact_reg_info('0004e0e6-5824-11e7-ace4-005056950094'))
    # main()
    if len(sys.argv[1:]) < 8:  # Just for testing
        print('Wrong args!')
        incom_args(['-y', '2018', '-m', '2', '-d', '17', '-s', '1'])
    else:
        incom_args(sys.argv[1:])
