#!/usr/bin/env python3

import csv
import os
from datetime import datetime


script_path = os.path.dirname(os.path.realpath(__file__))

def write_csv(input):
    try:
        with open(f'{script_path}/learning_data.txt', 'a', encoding='utf-8') as f:
            f.write(input)
    except:
        return


def open_companies_house_data():
    with open('companies_house_data.csv') as csv_file:
        csv_return = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_return.append(row)
        return csv_return


def insert_company_name_into_CSV(companies_data):
    for row in companies_data:
        company_name = row[0]
        print(f"Inserting {company_name} into CSV")
        company_name = f"{company_name}\t2\n"
        write_csv(company_name)


def main():
    companies_data = open_companies_house_data()
    insert_company_name_into_CSV(companies_data)

if __name__ == '__main__':
    main()
