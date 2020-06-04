from first import request_jason_data

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
        second_list.append(req2)
    for a in second_list:
        print(a['Date'])
find_from_to()