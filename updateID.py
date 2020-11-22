import csv
from getCostPriceOfSalary import request_jason_data, request_patch
import time

file_name = './data_files/goods_test_sml.csv'
# file_name = './data_files/goods_test.csv'
input_file = csv.DictReader(open(file_name, encoding='utf-8-sig'), delimiter=';')
row_count = sum(1 for row in input_file)

bad_val = {}


def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == "__main__":

    count = 0
    print(row_count)
    printProgressBar(0, row_count, prefix='Progress:', suffix='Complete', length=50)

    input_file = csv.DictReader(open("./data_files/goods_test_sml.csv", encoding='utf-8-sig'), delimiter=';')
    for row in input_file:
        if row['art'] is not None:
            # print(row)
            catalog = 'Catalog_Номенклатура'
            select = f""
            filt = f"Артикул eq '{row['art']}'"
            res = request_jason_data(catalog, select, filt)
            if len(res['value']) != 0:
                for a in res['value']:
                    pass
                    # print(a['Ref_Key'])
            else:
                bad_val.update({row['art']: res})
                # print('Bad val!')
        count += 1
        printProgressBar(count, row_count, prefix='Progress:', suffix='Complete', length=50)

    for a in bad_val:
        print(a)




