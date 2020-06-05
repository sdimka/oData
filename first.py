import requests
from requests.auth import HTTPBasicAuth


def main():
    start_date = '2020-05-01T00:00:00'
    end_date = '2020-05-20T23:59:59'
    get_salary(start_date, end_date)


def get_salary(start_date, end_date):

    # catalog = 'Catalog_Контрагенты'
    # select = 'Ref_Key, Description, ИНН, КПП'
    # filt = 'ИНН eq \'7814153672\''
    # print(request_jason_data(catalog, select, filt))

    # catalog = 'Document_ЗаказПокупателя'
    # select = ''
    # filt = "Date ge datetime'2020-05-24T00:00:00' and Date le datetime'2020-05-24T23:59:59'"
    # res = request_jason_data(catalog, select, filt)
    # print(res)
    # for a in res['value']:
    #     print('--------------------------')
    #     print(a)
    #     for b in a['Товары']:
    #         print(b)

    # Получаем список чеков
    catalog = 'Document_ЧекККМ'
    select = ''
    filt = f"Date ge datetime'{start_date}' and Date le datetime'{end_date}' and " \
           f"ЗаказОснование_Key ne '00000000-0000-0000-0000-000000000000'"
    res = request_jason_data(catalog, select, filt)
    filtered_res = [value for value in res['value']
                    if value['ЗаказОснование_Key'] != '00000000-0000-0000-0000-000000000000']

    # Получаем себестоимость
    # ToDo если закрытие смены было на след день?
    catalog = 'AccumulationRegister_ПродажиСебестоимость_RecordType'
    select = 'Recorder_Type, Подразделение_Key, Номенклатура_Key, Стоимость, Количество'
    filt = f"Period ge datetime'{start_date}' and Period le datetime'{end_date}'"
    res = request_jason_data(catalog, select, filt)

    # Убираем лишнее из себестоимости
    sorted_cost_price = dict()
    for a in res['value']:
        if a['Recorder_Type'] == 'StandardODATA.Document_ОтчетОРозничныхПродажах' \
                and a['Подразделение_Key'] == '1e2039a3-da0a-11dc-b992-001bfcc2ffde':
            sorted_cost_price[a['Номенклатура_Key']] = a['Стоимость']/a['Количество']

    total_cost_price = 0
    total_price = 0
    total_quantity = 0

    for a in filtered_res:
        doc_price = 0
        doc_quantity = 0
        doc_cost_price = 0
        # print(a['Number'])
        # print(a['Ref_Key'])

        # Получаем чеки на возрат по ссылке
        catalog = 'Document_ЧекККМ'
        select = ''
        filt = f"ЧекККМПродажа_Key eq guid'{a['Ref_Key']}'"
        receipts_on_return = request_jason_data(catalog, select, filt)

        if len(receipts_on_return['value']) == 0:
            for b in a['Товары']:
                # Получаем наименование товара
                catalog = f"Catalog_Номенклатура(Ref_Key=guid'{b['Номенклатура_Key']}'"
                select = 'Description'
                filt = ''
                res = request_jason_data(catalog, select, filt)
                b['Name'] = (res['Description'])

                # Не учитываем с/с доставки
                if b['Номенклатура_Key'] != '785ef93b-8e84-11e9-95f9-00505695411f' \
                        and b['Номенклатура_Key'] in sorted_cost_price:
                    b['cost_price'] = sorted_cost_price[b['Номенклатура_Key']]
                elif b['Номенклатура_Key'] == '785ef93b-8e84-11e9-95f9-00505695411f':
                    b['cost_price'] = 0
                else:
                    raise Exception(f"Could't find Key {b['Номенклатура_Key']} in cost_price on Date:{a['Date']}, Doc {a['Number']}")

                # print(f"{b['Name']} \t {b['Количество']} \t {b['Сумма']} \t {b['cost_price']} ")
                total_cost_price += b['cost_price'] * b['Количество']
                total_price += b['Сумма']
                total_quantity += b['Количество']
                doc_price += b['Сумма']
                doc_quantity += b['Количество']
                doc_cost_price += b['cost_price'] * b['Количество']
        else:
            print("Have receipt on return!")
            ddd = [val for val in receipts_on_return['value']]
            # print(ddd[0]['Товары'])
            if len(ddd[0]['Товары']) == len(a['Товары']):
                print('Full return just skip')
            else:
                print('Better to recalcs')

        # print(f"{a['Number']} По доку: Цена: {doc_price}, Кол-во: {doc_quantity}, С/С: {doc_cost_price}")

    print(f'Всего: Цена: {total_price}, Кол-во: {total_quantity}, С/С: {total_cost_price}')


def request_jason_data(catalog, select, r_filter):
    request_string = f'http://192.168.1.108/mayco/odata/standard.odata/{catalog}?' \
                     f'$format=json&' \
                     f'$select={select}&' \
                     f'$filter=({r_filter})'
    n_res = requests.get(request_string, auth=HTTPBasicAuth('sd', '12345'))
    n_res.encoding = 'utf-8'
    j_data = n_res.json()
    return j_data


def request_a(catalog, select, r_filter):
    request_string = f'http://192.168.1.108/mayco/odata/standard.odata/{catalog}?' \
                     f'$format=json&' \
                     f'$filter=({r_filter})'
    n_res = requests.get(request_string, auth=HTTPBasicAuth('sd', '12345'))
    n_res.encoding = 'utf-8'
    j_data = n_res.json()
    return j_data


if __name__ == '__main__':
    main()

