import csv
import datetime
import pandas
import copy

file_lines = []

file_headers = [
    'fecha',
    'material',
    'precio_local',
    'cantidad',
    'precio_total_local',
    'total_dolar',
    'conversion_dolar',
]

FILE_PATH = 'datos_de_ventas.csv'

def read_ventas():

    csv.register_dialect('semi_col', delimiter=';', quoting=csv.QUOTE_NONE)
    reader = csv.reader(open(FILE_PATH, 'r'), 'semi_col')
    for row in reader:
        # row[1] = "hola"
        # for val in row:
        #     row_values.append(val)
        file_lines.append(copy.copy(row))
        print(row)
    # data = pandas.read_csv(
    #     'datos_de_ventas.csv',
    #     index_col='fecha',
    #     parse_dates=['fecha'],
    #     header=0,
    #     names=file_headers
    # )
    # print(data)


if __name__ == "__main__":
    read_ventas()
