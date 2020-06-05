"""
pip3 install mysql-connector-python
"""

import mysql.connector
from credentials import credentials
from getCostPriceOfSalary import request_jason_data

db_connection = mysql.connector.connect(
    host=credentials['SQLHost'],
    user=credentials['SQLUser'],
    passwd=credentials['SQLPass'],
    database=credentials['SQLDB']
)

database = db_connection.cursor()

sql_statement = 'SELECT * FROM products'
database.execute(sql_statement)
output = database.fetchall()

for x in output:
    print(x)

list_to_work = ['7bb97928-2be5-11dd-94e3-0019992accca']


def get_child(parent_ref_id):
    catalog = 'Catalog_Номенклатура'
    select = ''
    filt = f"Parent_Key eq guid'{parent_ref_id}'"
    req = request_jason_data(catalog, select, filt)
    print(req)
    for a in req['value']:
        if a['IsFolder']:
            list_to_work.append(a['Ref_Key'])
            print(a['Description'])


def main():
    while len(list_to_work):
        get_child(list_to_work.pop())


if __name__ == '__main__':
    main()