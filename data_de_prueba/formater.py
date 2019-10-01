import csv
import datetime
import pandas
import copy

file_headers = [
    'fecha',
    'material',
    'precio_local',
    'cantidad',
    'precio_total_local',
    'total_dolar',
    'conversion_dolar',
]
file_headers2 = [
    '#',
    'fecha',
    'material',
    'precio_local',
    'cantidad',
    'precio_total_local',
    'total_dolar',
    'conversion_dolar',
]


FILE_PATH = 'datos_de_ventas.csv'

csv.register_dialect('semi_col', delimiter=';', quoting=csv.QUOTE_NONE)


def read_ventas():
    file_lines = []

    reader = csv.reader(open(FILE_PATH, 'r'), 'semi_col')
    for index, row in enumerate(reader):
        if index > 0:
            pass
            # agrupando franelillas
            if row[1].find('FRANELILLA') != -1:
                row[1] = 'FRANELILLA'

            elif row[1].find('NIÑO') != -1:
                row[1] = 'FRANELA NIÑO'

            elif row[1].find('FRANELA') != -1:
                row[1] = 'FRANELA'

            elif row[1].find('TAZA') != -1:
                row[1] = 'TAZA'

            elif row[1].find('VASO') != -1:
                row[1] = 'VASO'

            elif row[1].find('GORRA') != -1:
                row[1] = 'GORRA'

            elif row[1].find('PULSERA') != -1:
                row[1] = 'PULSERA'

            elif row[1].find('PULSERITA') != -1:
                row[1] = 'PULSERITA'

            elif row[1].find('BODY') != -1:
                row[1] = 'BODY BEBE'

            elif row[1].find('CAB') != -1:
                row[1] = 'FRANELA'

            elif row[1].find('DAMAS') != -1:
                row[1] = 'FRANELA'

            elif row[1].find('CARTUCHERA') != -1:
                row[1] = 'CARTUCHERA'

            elif row[1].find('LLAVERO') != -1:
                row[1] = 'LLAVERO'

            elif row[1].find('VIAJERA') != -1:
                row[1] = 'VIAJERA'

            elif row[1].find('PORTA') != -1:
                row[1] = 'PORTA COSMETICO'

            elif row[1].find('BRAZALETE') != -1:
                row[1] = 'BRAZALETE'

            elif row[1].find('ESTAMPADO') != -1:
                row[1] = 'ESTAMPADO'

            elif row[1].find('BANDOLERA') != -1:
                row[1] = 'BANDOLERA'

            elif row[1].find('TULA') != -1:
                row[1] = 'TULA'

            elif row[1].find('MAPA') != -1:
                row[1] = 'COLLAR MAPA'
            file_lines.append(copy.copy(row))

    return file_lines


def write_csv(rows, file_name):

    with open(file_name, mode='w') as employee_file:
        file_writer = csv.writer(
            employee_file,
            delimiter=';',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL
        )

        file_writer.writerow(file_headers)

        for row in rows:
            file_writer.writerow(row)


def format_dates():

    df = pandas.read_csv(
        'datos_formateados.csv',
        parse_dates=['fecha'],
        header=0,
        names=file_headers,
        sep=';',
    )
    print(df)
    df.to_csv('datos_con_fecha.csv', sep=';')


def format_dolar_dates():
    df = pandas.read_csv(
        'dolar_today.csv',
        parse_dates=['fecha'],
        header=0,
        names=['fecha', 'conversion_dolar'],
        sep=';',
    )
    print(df)
    df.to_csv('dolar_fecha.csv', sep=';')


def add_dolar_price_dates():
    row_list = []

    dolar_df = pandas.read_csv(
        'dolar_fecha.csv',
        header=0,
        index_col='#',
        names=['#', 'fecha', 'conversion_dolar'],
        sep=';',
    )

    datos_df = pandas.read_csv(
        'datos_con_fecha.csv',
        header=0,
        index_col='#',
        names=file_headers2,
        sep=';',
    )

    for index, row in datos_df.iterrows():
        edit_row = dict(row)
        dolar_value = dolar_df.loc[dolar_df['fecha'] == row['fecha']]['conversion_dolar']
        # import pdb; pdb.set_trace()
        # print(dolar_value)
        try:
            edit_row['conversion_dolar'] = float(dolar_value)
            row_list.append(edit_row)
        except Exception as ex:
            print(ex)
            print(edit_row)
            print(dolar_value)

    with open('datos_precio_fecha.csv', mode='w') as csv_file:
        # fieldnames = ['emp_name', 'dept', 'birth_month']
        writer = csv.DictWriter(
            csv_file,
            fieldnames=file_headers,
            delimiter=';'
        )
        writer.writeheader()

        for row in row_list:
            writer.writerow(row)
    # print(row_list)


def get_dolar_price():
    with open('employee_birthday.txt', mode='r') as csv_file:
        pass

if __name__ == "__main__":
    add_dolar_price_dates()
    # rows = read_ventas()
    # write_csv(rows, 'datos_formateados.csv')
    # format_dates()
    # format_dolar_dates()
    # get_dolar_price()
