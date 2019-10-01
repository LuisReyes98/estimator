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

FILE_PATH = 'datos_de_ventas.csv'


def read_ventas():
    file_lines = []

    csv.register_dialect('semi_col', delimiter=';', quoting=csv.QUOTE_NONE)
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


if __name__ == "__main__":
    rows = read_ventas()
    write_csv(rows, 'datos_formateados.csv')
