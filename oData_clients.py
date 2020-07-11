from getCostPriceOfSalary import request_jason_data

#  Catalog_Контрагенты

# Запрос одного элемента:
# http://192.168.1.108/mayco/odata/standard.odata/InformationRegister_КонтактнаяИнформация&$top=1&$format=json

# Чеки за период - Дисконтная карта - Контрагент - контакты - фильтр телефонов - сравнение


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
    print(req)
    # for a in req['value']:
    #     if a['IsFolder']:
    #         list_to_work.append(a['Ref_Key'])
    #         print(a['Description'])


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
    print(req['Представление'], req['ПолеПоискаПоТелефону'])


def search_recipe_by_period():
    START_DATE = '2020-05-01T00:00:00'
    END_DATE = '2020-05-01T23:59:59'
    catalog = 'Document_ЧекККМ'
    select = ''
    filt = f"Date ge datetime'{START_DATE}' and Date le datetime'{END_DATE}' "
    req = request_jason_data(catalog, select, filt)
    for a in req['value']:
        if a['ДисконтнаяКарта_Key'] != '00000000-0000-0000-0000-000000000000':
            search_inf_card(a['ДисконтнаяКарта_Key'])
            print(a['ДисконтнаяКарта_Key'])

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


# get_contr_by_code('АА0094687')
# search_recipe_by_period()
# get_client_by_code('e7e66f48-cf94-11e7-a937-005056950094')
get_contact_reg_info('e7e66f48-cf94-11e7-a937-005056950094')
