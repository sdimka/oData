import requests
from requests.auth import HTTPBasicAuth


def main():

    START_DATE = '2020-05-23T00:00:00'
    END_DATE = '2020-05-23T23:59:59'
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

    catalog = "Catalog_Номенклатура(Ref_Key=guid'b00f7fca-08ac-11e3-a448-005056950007')"
    select = ''
    filt = ''
    res = request_jason_data(catalog, select, filt)
    print(res)

    catalog = 'Document_ЧекККМ'
    select = ''
    filt = f"Date ge datetime'{START_DATE}' and Date le datetime'{END_DATE}' and " \
           f"ЗаказОснование_Key ne '00000000-0000-0000-0000-000000000000'"
    res = request_jason_data(catalog, select, filt)
    filtered_res = [value for value in res['value']
               if value['ЗаказОснование_Key'] != '00000000-0000-0000-0000-000000000000']

    catalog = 'AccumulationRegister_ПродажиСебестоимость_RecordType'
    select = 'Recorder_Type, Подразделение_Key, Номенклатура_Key, Стоимость'
    filt = f"Period ge datetime'{START_DATE}' and Period le datetime'{END_DATE}'"
    res = request_jason_data(catalog, select, filt)

    sorted_cost_price = dict()
    for a in res['value']:
        if a['Recorder_Type'] == 'StandardODATA.Document_ОтчетОРозничныхПродажах' \
                and a['Подразделение_Key'] == '1e2039a3-da0a-11dc-b992-001bfcc2ffde':
            sorted_cost_price[a['Номенклатура_Key']] = a['Стоимость']

    total_cost_price = 0
    total_price = 0

    for a in filtered_res:
        doc_price = 0
        print(a['Number'])
        print(a['Ref_Key'])
        # print(a['ЗаказОснование_Key'])
        for b in a['Товары']:
            catalog = f"Catalog_Номенклатура(Ref_Key=guid'{b['Номенклатура_Key']}'"
            select = 'Description'
            filt = ''
            res = request_jason_data(catalog, select, filt)
            b['Name'] = (res['Description'])
            b['cost_price'] = sorted_cost_price[b['Номенклатура_Key']]
            print(f"{b['Name']} \t {b['cost_price']} ")
            total_cost_price += b['cost_price']
            total_price += b['Сумма']
            doc_price += b['Сумма']
        print(doc_price)

    print(total_cost_price)
    print(total_price)


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

