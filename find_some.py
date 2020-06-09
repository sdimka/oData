from getCostPriceOfSalary import request_jason_data
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth


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

def get_return_receipts(start_date, end_date):
    catalog = 'Document_ЧекККМ'
    select = ''
    filt = f"Date ge datetime'{start_date}' and Date le datetime'{end_date}' and " \
           f"ЧекККМПродажа_Key ne guid'00000000-0000-0000-0000-000000000000'"
    receipts_on_return = request_jason_data(catalog, select, filt)
    for a in receipts_on_return['value']:
        print(a['Number'])


def cost_price_by_day(start_date, end_date):
    catalog = 'AccumulationRegister_ПродажиСебестоимость_RecordType'
    select = 'Recorder_Type, Подразделение_Key, Period, Номенклатура_Key, Стоимость, Количество'
    filt = f"Period ge datetime'{start_date}' and Period le datetime'{end_date}'"
    res = request_jason_data(catalog, select, filt)
    sorted_cost_price = {}

    for a in res['value']:
        if a['Recorder_Type'] == 'StandardODATA.Document_ОтчетОРозничныхПродажах' \
                and a['Подразделение_Key'] == '1e2039a3-da0a-11dc-b992-001bfcc2ffde':
            str = a['Period']
            date = datetime.strptime(str[:10], '%Y-%m-%d')
            if date in sorted_cost_price:
                sorted_cost_price[date].update({a['Номенклатура_Key']: a['Стоимость']/a['Количество']})
            else:
                sorted_cost_price[date] = {a['Номенклатура_Key']: a['Стоимость']/a['Количество']}
    print(sorted_cost_price)


def test():
    my_dict = {}
    a_date = '2020-05-01T00:00:00'
    b_date = '2020-05-10T23:59:59'
    val1 = datetime.strptime(a_date[:10], '%Y-%m-%d')
    val2 = datetime.strptime(b_date[:10], '%Y-%m-%d')
    if val1 in my_dict:
        my_dict[val1].update({'res2': 1113})
    else:
        my_dict[val1] = ({'res1': 1112})
    print(my_dict[val1])


def get_last_cost(product_ref, departure_ref):

    start_date = '2020-05-01T00:00:00'
    end_date = '2020-05-11T23:59:59'
    catalog = 'AccumulationRegister_ПродажиСебестоимость_RecordType'
    select = 'Recorder_Type, Подразделение_Key, Period, Номенклатура_Key, Стоимость, Количество'
    r_filter = f"Period ge datetime'{start_date}' and Period le datetime'{end_date}' " \
               f"and Номенклатура_Key eq guid'{product_ref}' " \
               f"and Recorder_Type eq 'StandardODATA.Document_ОтчетОРозничныхПродажах' " \
               f"and Подразделение_Key eq guid'{departure_ref}'"
    # f'$orderby = {order}&' - Параметр $orderby, top не поддерживается, WTF???
    n_res = request_jason_data(catalog, select, r_filter)
    return n_res


# find_from_to()
get_product_by_id('e93b7176-7e3c-11dd-a8e6-0019992accca')
start_date = '2020-05-01T00:00:00'
end_date = '2020-05-10T23:59:59'
# get_return_receipts(start_date, end_date)
# cost_price_by_day(start_date, end_date)
# test()
res = get_last_cost('e93b7176-7e3c-11dd-a8e6-0019992accca', '1e2039a3-da0a-11dc-b992-001bfcc2ffde')
print(res)
for a in res['value']:
    print(round(a['Стоимость']/a['Количество'], 2))


