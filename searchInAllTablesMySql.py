import mysql.connector
import time

search_value = "9431814"

db_connection = mysql.connector.connect(
  host="192.168.1.180",
  user="root",
  passwd="mypassword",
  database="sitemanager"
)
db_cursor = db_connection.cursor()


def get_tables():
    db_cursor.execute("SHOW TABLES")
    return [column[0] for column in db_cursor.fetchall()]
    # return db_cursor.fetchall()


def get_columns(table_name):
    db_cursor.execute(f'SHOW columns FROM {table_name}')
    return [column[0] for column in db_cursor.fetchall()]


def get_value(table, column, value):
    result = []
    s_string = "%" + value + "%"
    try:
        db_cursor.execute(f'SELECT * FROM {table} WHERE {column} like "%943 18 14%"')
        result = [column[0] for column in db_cursor.fetchall()]
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        print(f'Table: {table}, Column: {column}')
    # return [column[0] for column in db_cursor.fetchall()]
    return result

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
    tables = get_tables()

    l = len(tables)
    count = 0

    # Initial call to print 0% progress
    # printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
    # for i, item in enumerate(items):
    #     # Do stuff...
    #     time.sleep(0.1)
    #     # Update Progress Bar
    #     printProgressBar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)
    total = []
    printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
    for a in tables:
        columns = get_columns(a)
        count += 1
        for b in columns:
            res = get_value(a, b, search_value)
            if len(res) > 0:
                total.append(f'Table: {a}, Column: {b}, Row: {res}')
        printProgressBar(count , l, prefix='Progress:', suffix='Complete', length=50)

    print(total)
