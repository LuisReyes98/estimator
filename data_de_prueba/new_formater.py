import csv
from datetime import datetime, date
import copy

csv.register_dialect(
    'semi_col',
    delimiter=';',
    quoting=csv.QUOTE_NONE
)
FILE_PATH = './finales/ventas_agrupadas.csv'

FILE_PATH_2 = './finales/ventas_agrupadas_2.csv'


def group_by_name():
    year_month_dict = {}
    fo = open(FILE_PATH, 'r')
    reader = csv.reader(fo, 'semi_col')

    for index, row in enumerate(reader):
        if index == 0:
            header = row
        elif index > 0:
            date = datetime.strptime(row[0], '%Y-%m-%d').date()
            string_date = "%d-%d" % (date.year, date.month)
            name = row[4]

            dollar_price = float(row[1])

            prod = {
                'name': name,
                'amount': row[5],
                'cost_dollar': row[6],
            }
            if not year_month_dict.get(string_date):
                year_month_dict[string_date] = {}
                year_month_dict[string_date]['items'] = {}
                year_month_dict[string_date]['dollar_price'] = dollar_price

            if year_month_dict[string_date]['dollar_price'] < dollar_price:
                year_month_dict[string_date]['dollar_price'] = dollar_price

            # year_month_dict[string_date].append(row)
            if not year_month_dict[string_date].get(name):
                year_month_dict[string_date]['items'][name] = prod
            else:
                year_month_dict[string_date]['items'][name]['amount'] = int(year_month_dict[string_date]['items'][name]['amount'] ) +  int(prod['amount'])
                if float(year_month_dict[string_date]['items'][name]['cost_dollar']) < float(prod['cost_dollar']):
                    year_month_dict[string_date]['items'][name]['cost_dollar'] = float(prod['cost_dollar'])
    fo.close()

    # print(year_month_dict)

    file = open(FILE_PATH_2, mode='w')
    file_writer = csv.writer(
        file,
        delimiter=';',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
    )

    for key, value in year_month_dict.items():
        row = []
        row.append(key + '-1')
        row.append(value['dollar_price'])

        for k, val in value['items'].items():

            row.append(val['name'])
            row.append(val['amount'])
            row.append(val['cost_dollar'])
            row.append(0)
            row.append('SI')

        file_writer.writerow(row)


if __name__ == "__main__":
    pass
    group_by_name()
