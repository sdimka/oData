from getCostPriceOfSalary import request_jason_data

#  Catalog_Контрагенты

# Запрос одного элемента:
# http://192.168.1.108/mayco/odata/standard.odata/InformationRegister_КонтактнаяИнформация&$top=1&$format=json

# Чеки за период -> Дисконтная карта -> Контрагент -> контакты -> фильтр телефонов - сравнение


def get_client_by_code(code):
    """
    Полезные поля: 'Description'/'НаименованиеПолное' , 'Code'
    'ДатаСоздания', 'СогласенНаРассылкуSMS', 'ДатаРождения', 'Пол', 'СогласенНаРассылкуEMAIL'
    :param code:
    :return:
    """
    catalog = f"Catalog_Контрагенты(Ref_Key=guid'{code}')"
    select = ''
    filt = ''
    req = request_jason_data(catalog, select, filt)
    print('Клиент:', req['Ref_Key'], req['Code'])
    get_contact_reg_info(req['Ref_Key'])


def get_contact_reg_info(code):
    #  Использовать "ПолеПоискаПоТелефону"
    #  http://192.168.1.108/mayco/odata/standard.odata/InformationRegister_КонтактнаяИнформация
    #  (Объект='e7e66f48-cf94-11e7-a937-005056950094',
    #  Объект_Type='StandardODATA.Catalog_Контрагенты',
    #  Тип = 'Телефон',
    #  Вид=guid'968558ff-8fe0-40d0-84e3-ca694acbc839',
    #  Вид_Type='StandardODATA.Catalog_ВидыКонтактнойИнформации')
    catalog = f"InformationRegister_КонтактнаяИнформация(Объект='{code}', " \
              f"Объект_Type='StandardODATA.Catalog_Контрагенты', " \
              f"Тип = 'Телефон', " \
              f"Вид=guid'968558ff-8fe0-40d0-84e3-ca694acbc839', " \
              f"Вид_Type='StandardODATA.Catalog_ВидыКонтактнойИнформации')"
    select = ''
    filt = ''
    req = request_jason_data(catalog, select, filt)
    print(req)
    # print(req['Представление'], req['ПолеПоискаПоТелефону'])


def search_recipe_by_period(dep_code):  # и не нулевой картой
    START_DATE = '2020-03-01T00:00:00'
    END_DATE = '2020-03-01T23:59:59'
    catalog = 'Document_ЧекККМ'
    select = ''
    filt = f"Date ge datetime'{START_DATE}' and Date le datetime'{END_DATE}' and Подразделение_Key eq guid'{dep_code}'"
    req = request_jason_data(catalog, select, filt)
    print(req)
    for a in req['value']:
        if a['ДисконтнаяКарта_Key'] != '00000000-0000-0000-0000-000000000000':
            # print(a['ДисконтнаяКарта_Key'])
            # print(a)
            print('Номерчека: ', a['Number'])
            # search_inf_card(a['ДисконтнаяКарта_Key'])


def search_inf_card(card_num):
    # Catalog_ИнформационныеКарты
    catalog = f"Catalog_ИнформационныеКарты(Ref_Key=guid'{card_num}')"
    select = ''
    filt = ''
    req = request_jason_data(catalog, select, filt)
    get_client_by_code(req['ВладелецКарты'])
    # print(req['ВладелецКарты'])
    # for a in req:
    #     print(a)


def get_department_id_by_code(code):
    catalog = f"Catalog_Подразделения"
    select = ''
    filt = f"Code eq '{code}'"
    req = request_jason_data(catalog, select, filt)
    return req['value'][0]['Ref_Key']

# get_contr_by_code('АА0094687')
# get_client_by_code('e7e66f48-cf94-11e7-a937-005056950094')
# get_contact_reg_info('e7e66f48-cf94-11e7-a937-005056950094')


dep_name_list = {'Магазин Богатырский' : 'ОП0000002', 'Магазин Гулливер': 'ИТС000024', 'Магазин Девяткино': 'АА0000017',
                 'Магазин Заневский': 'ИТС000022', 'Магазин Лондон Молл': 'АА0000025', 'Магазин Меркурий': 'АА0000015',
                 'Магазин Порт Находка': 'АА0000026', 'Магазин РодеоДрайв': 'ИТС000027', 'Магазин Рубикон': 'ОП0000003',
                 'Магазин Французский бульвар': 'АА0000024', 'Магазин Звездный': 'АА0000018', 'Магазин Международный' : 'АА0000012',
                 'Магазин Нахимова': 'АА0000020', 'Магазин ОКей Пулково': 'ИТС000026', 'Магазин Оккервиль': 'ОП0000004',
                 'Магазин Стачек': 'АА0000022', 'Магазин Типанова': 'ЛС0000001', 'Магазин Электросила': 'ОП0000006',
                 }

search_recipe_by_period(
    get_department_id_by_code(dep_name_list['Магазин Заневский']))

# for a in dep_name_list.values():
#     print(get_department_id_by_code(a))
