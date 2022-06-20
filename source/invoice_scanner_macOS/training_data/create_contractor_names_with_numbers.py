#!/usr/bin/env python3

import csv
import os
from datetime import datetime


script_path = os.path.dirname(os.path.realpath(__file__))

def write_csv(input):
    try:
        with open(f'{script_path}/contractor_details_with_numbers.csv', 'a', encoding='utf-8') as f:
            f.write(input)
    except:
        return


def open_companies_house_data():
    with open(f'{script_path}/companies_house_data.csv') as csv_file:
        csv_return = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_return.append(row)
        return csv_return


def insert_data_into_csv(companies_data):
    for row in companies_data:
        company_name = row[0]
        company_name = company_name.replace(',',' ')
        company_number = row[1]
        csv_data = f"{company_name},{company_number}\n"
        print(f"Inserting {csv_data} into CSV")
        write_csv(csv_data)


def main():
    companies_data = open_companies_house_data()
    insert_data_into_csv(companies_data)


if __name__ == '__main__':
    main()
