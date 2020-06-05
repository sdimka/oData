from first import request_jason_data
from datetime import datetime


def find_from_to():
    START_DATE = '2020-05-01T00:00:00'
    END_DATE = '2020-05-30T23:59:59'
    catalog = 'Document_ЧекККМ'
    select = ''
    filt = f"Date ge datetime'{START_DATE}' and Date le datetime'{END_DATE}' " \
        f"and ЧекККМПродажа_Key ne guid'00000000-0000-0000-0000-000000000000'"
    req = request_jason_data(catalog, select, filt)

    second_list = []
    for a in req['value']:
        catalog = f"Document_ЧекККМ(Ref_Key=guid'{a['ЧекККМПродажа_Key']}')"
        select = ''
        filt = ''
        req2 = request_jason_data(catalog, select, filt)
        str1 = a['Date']
        date1 = datetime.strptime(str1[:10], '%Y-%m-%d')
        str2 = req2['Date']
        date2 = datetime.strptime(str2[:10], '%Y-%m-%d')
        if date1 != date2:
            print(a['Number'])
        second_list.append(req2)

    # for a in second_list:
    #     str = a['Date']
    #     date_time = datetime.strptime(str[:10], '%Y-%m-%d')
    #     print(date_time.date())

def get_product_by_id(id):
    catalog = f"Catalog_Номенклатура(Ref_Key=guid'{id}')"
    select = ''
    filt = ''
    res = request_jason_data(catalog, select, filt)
    print(res['Code'], res['Description'], res['DeletionMark'])


# find_from_to()
get_product_by_id('5e24bf7d-7a1a-11e4-87b0-005056950007')

