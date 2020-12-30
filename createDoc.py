from getCostPriceOfSalary import request_patch, request_post, request_jason_data, request_post_document, request_delete_document


def create_ORP():
    products = [{'Номенклатура_Key': 'd089a08d-fe9e-11e2-809a-005056950007',
                 'Количество': 2,
                 'LineNumber': '1',
                 'ЕдиницаИзмерения_Key': 'd089a08e-fe9e-11e2-809a-005056950007',
                 'Цена': 39,
                 'Сумма': 39},
                {'Номенклатура_Key': 'b5980fd3-0af6-457b-851c-9e63dc70b615',
                 'Количество': 1,
                 'LineNumber': '2',
                 'ЕдиницаИзмерения_Key': 'e07be3d5-10ee-11dd-a121-000c29f7257a',
                 'Цена': 49,
                 'Сумма': 46.55}]
    cat = 'Document_ОтчетОРозничныхПродажах'
    body = {"Date": "2020-12-29T12:01:07",
            'Склад_Key': '02e2113a-04bd-11e3-809a-005056950007',
            'Организация_Key': 'd2a7e3db-ce58-11dc-b98e-001bfcc2ffde',
            'ИТС_ОрганизацияДляПечати_Key': '88eb2a4c-2f9f-11e1-b212-005056950007',
            'ВидОперации': 'ОтчетККМОПродажах',
            'ОтражатьВУправленческомУчете': True,
            'Подразделение_Key': '02e21134-04bd-11e3-809a-005056950007',
            'КассаККМ_Key': '02e21138-04bd-11e3-809a-005056950007',
            'Товары': products}
    # res = request_post(cat, '', '', body)

    # START_DATE = '2020-12-29T00:00:00'
    # END_DATE = '2020-12-29T23:59:59'
    # filt = f"Date ge datetime'{START_DATE}' and Date le datetime'{END_DATE}' "
    # reg1 = request_jason_data(cat, '', filt)
    # for a in reg1['value']:
    #     print(a)

    rk = '62931678-49ee-11eb-961b-00505639c498'
    req = request_post_document(cat, rk)
    print(req)
    for a in req:
        print(a.decode('utf-8'))

    # res['Ref_Key'])
    # http://host/base/odata/standard.odata/Document_РасходТоваров(guid'value')/Post?PostingModeOperational=false
    # print(res)


def create_PTY():
    cat = 'Document_ПоступлениеТоваровУслуг'
    # START_DATE = '2020-12-29T00:00:00'
    # END_DATE = '2020-12-29T23:59:59'
    # filt = f"Date ge datetime'{START_DATE}' and Date le datetime'{END_DATE}' "
    rk = '01c64969-49eb-11eb-961b-00505639c498'
    # print(request_jason_data(cat, '', filt))

    req = request_post_document(cat, rk)
    for a in req:
        print(a.decode('utf-8'))


def test1():

    catalog = f"Document_ОтчетОРозничныхПродажах"
    # select = 'Ref_Key, Number, Date, Б_Идентификатор'
    filt = "Number eq 'ААЛК0000310'"
    # filt = "Number eq 'ААЭС0009820'" Б_Идентификатор
    # filt = f"Date ge datetime'{s_date}' and Date le datetime'{e_date}' and Б_Идентификатор ne ''"
    req = request_jason_data(catalog, '', filt)
    print(req)


if __name__ == "__main__":
    create_ORP()
