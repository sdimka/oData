from getCostPriceOfSalary import request_jason_data




# Номер заказа из БД + статус оплаты -> ID заказа 1С -> Чек по ID заказа, если нет Оплата от покупателя ПК
#  Закрытие заказов покупателей

#  ААЭС0011272 - на сайте оплачен, оплаты ПК нет
#  ААЭС0011283 - есть ОПК, на сайте оплаты нет???


#  http://192.168.1.108/mayco/odata/standard.odata/Document_ЧекККМ&$top=1&$format=json

catalog = f"Document_ЗаказПокупателя"
select = 'Ref_Key, Number, Date, Б_Идентификатор'
filt = "Number eq 'ААЭС0009820'"
req = request_jason_data(catalog, select, filt)

print(req['value'][0]['Ref_Key'])

catalog = f"Document_ЧекККМ"
select = 'Ref_Key, Number, Date'
filt = f"ЗаказОснование_Key eq guid'{req['value'][0]['Ref_Key']}'"
req1 = request_jason_data(catalog, select, filt)

print(req1)

# catalog = f"Document_ОплатаОтПокупателяПлатежнойКартой(ВидОперации = 'ОплатаПокупателя'" \
#           f"ДокументОснование_Type = 'StandardODATA.Document_ЗаказПокупателя', " \
#           f"ДокументОснование = guid'{req['value'][0]['Ref_Key']}')"
catalog = 'Document_ОплатаОтПокупателяПлатежнойКартой'
select = ''
filt = f"ДокументОснование_Type eq 'StandardODATA.Document_ЗаказПокупателя' and ДокументОснование eq guid'{req['value'][0]['Ref_Key']}'"
req2 = request_jason_data(catalog, select, filt)
print(req2)
