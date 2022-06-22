#!/usr/bin/env python3

import re
import os
import pathlib
import cv2
import pandas as pd

import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path
from datetime import datetime
from fuzzysearch import find_near_matches
from thefuzz import fuzz
from thefuzz import process

from models import Company
from db_setup import init_db, db_session
from invoice_extractor import sort_invoice_files


init_db()
script_path = os.path.dirname(os.path.realpath(__file__))


def convert_to_temp_jpeg(filepath):
    try:
        if os.path.isfile(filepath) is True:
            pages = convert_from_path(
                                    filepath,
                                    dpi=300,
                                    grayscale=True,
                                    fmt='jpeg',
                                    jpegopt={"quality": 100, "optomise": True}
            )

            for page in pages:
                page.save(os.path.join(script_path, "temp.jpg"), 'JPEG')
    except:
        print("Not a supported file")


def extract_text_from_image(img):
    if os.path.isfile(img) is True:
        image = cv2.imread(img)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(image)
        return text


def search_company_number(input):
    qry = db_session.query(Company).filter(
                                Company.CompanyNumber.contains(input)
    )
    results = qry.all()
    return results


def search_company_name(input):
    qry = db_session.query(Company).filter(
                                Company.CompanyName.contains(input)
    )
    results = qry.all()
    return results


def find_contractor_name(path):

    invoices_sorted = sort_invoice_files(path)
    invoices_sorted.sort()

    for invoice in invoices_sorted:
        new_path = os.path.join(path, invoice)
        image = os.path.join(script_path, "temp.jpg")

        convert_to_temp_jpeg(new_path)

        text = extract_text_from_image(image)

        print(text)

        search_entry = input("Please enter company name or number: ")

        companies = search_company_number(search_entry)
        if companies == []:
            companies = search_company_name(search_entry)

        number_of_found_companies = len(companies)

        print(f"Number of matches {number_of_found_companies}")

        if number_of_found_companies > 5:
            print("Too many matches, please check company name")


        if number_of_found_companies < 5:
            for company in companies:
                print(f"{company.CompanyNumber}, {company.CompanyName}, {company.RegAddress_AddressLine1}, {company.RegAddress_PostCode}, {company.SICCode_SicText_1}")
                # company_post_code = company.RegAddress_PostCode
                # company_category = company.SICCode_SicText_1

path = "/Users/edspece/Desktop/Test_files"
find_contractor_name(path)
