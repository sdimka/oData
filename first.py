import requests
from requests.auth import HTTPBasicAuth


def main():
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

    # catalog = 'Document_ЧекККМ'
    # select = ''
    # filt = "Date ge datetime'2020-05-23T00:00:00' and Date le datetime'2020-05-23T23:59:59' and " \
    #        "ЗаказОснование_Key ne '00000000-0000-0000-0000-000000000000'"
    # res = request_jason_data(catalog, select, filt)
    # # newDict = {key: value for (key, value) in res.items()
    # #            if key['ЗаказОснование_Key'] != '00000000-0000-0000-0000-000000000000'}
    # filtered_res = []
    # for a in res['value']:
    #     if a['ЗаказОснование_Key'] != '00000000-0000-0000-0000-000000000000':
    #         filtered_res.append(a)
    #         for b in a['Товары']:
    #             pass
    #             # print(b)
    #
    # for a in filtered_res:
    #     print(a['Number'])
    #     print(a['ЗаказОснование_Key'])
    #     for b in a['Товары']:
    #         catalog = f"Catalog_Номенклатура(Ref_Key=guid'{b['Номенклатура_Key']}'"
    #         select = 'Description'
    #         filt = ''
    #         res = request_jason_data(catalog, select, filt)
    #         b['Name'] = (res['Description'])
    #         print(b)

    catalog = 'AccumulationRegister_ПродажиСебестоимость_RecordType'
    select = ''
    filt = "Period ge datetime'2020-05-23T00:00:00' and Period le datetime'2020-05-23T23:59:59'"
    res = request_jason_data(catalog, select, filt)
    print(res)
    for a in res['value']:
        print(a)


def request_jason_data(catalog, select, r_filter):
    request_string = f'http://192.168.1.108/mayco/odata/standard.odata/{catalog}?' \
                     f'$format=json&' \
                     f'$select={select}&' \
                     f'$filter=({r_filter})'
    print(request_string)
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

