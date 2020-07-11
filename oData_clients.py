from getCostPriceOfSalary import request_jason_data
from datetime import datetime, date, timedelta

from order_repo import Order, Product, Customer, session

#  Catalog_Контрагенты

# Запрос одного элемента:
# http://192.168.1.108/mayco/odata/standard.odata/InformationRegister_КонтактнаяИнформация&$top=1&$format=json

# ID Подразделения -> Чеки за период (лист Дисконтная карта) -> Контрагент (лист) -> Если нет, записываем в БД
#
# При загрузке с сайте контакты -> фильтр телефонов -> сравнение
#
total_list = []

def main():

    for i in range(90):
        d = date(year=2018, month=1, day=1) + timedelta(days=i)

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
                client_info = get_client_by_code(client_number)
                get_contact_reg_info(client_number)

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
        pass  # print(req['Представление'], req['ПолеПоискаПоТелефону'])
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


if __name__ == '__main__':
    main()
