#!/usr/bin/env python3

import csv
#import rsa
import os
#from forms import RenewalsSearchForm, RenewalForm
from flask import flash, render_template, request, redirect
from flask_basicauth import BasicAuth
from datetime import datetime

from db_setup import init_db, db_session
from models import Company
#from tables import Results

init_db()

def open_companies_house_data():
    with open('companies_house_data.csv') as csv_file:
        csv_return = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_return.append(row)
        return csv_return


def insert_csv_into_db():

    companies_data = open_companies_house_data()

    for row in companies_data:

        company = Company()

        company.CompanyName = row[0]
        print(f"Adding {company.CompanyName} to database...")
        company.CompanyNumber = row[1]
        company.RegAddress_CareOf = row[2]
        company.RegAddress_POBox = row[3]
        company.RegAddress_AddressLine1 = row[4]
        company.RegAddress_AddressLine2 = row[5]
        company.RegAddress_PostTown = row[6]
        company.RegAddress_County = row[7]
        company.RegAddress_Country = row[8]
        company.RegAddress_PostCode = row[9]
        company.SICCode_SicText_1 = row[26]

        db_session.add(company)

    db_session.commit()


def main():
    insert_csv_into_db()


if __name__ == '__main__':
    main()
