import re
import os
import pathlib
import cv2
import pytesseract
import pandas as pd

from pytesseract import Output
from pdf2image import convert_from_path
#from tkinter import *
#from tkinter import filedialog

from datetime import datetime
from models import Company
from db_setup import init_db, db_session
from auto_labeller import build_auto_classifier, auto_classifier

from fuzzysearch import find_near_matches
from thefuzz import fuzz
from thefuzz import process


init_db()
vectorizer, classifier = build_auto_classifier()
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


def get_file_extension(file):
    file_extension = pathlib.Path(file).suffix
    return file_extension


def get_invoice_files(path):
    invoices = os.listdir(os.path.expanduser(path))
    invoices_sorted = []
    for file in invoices:
        extension = get_file_extension(file)
        if extension == ".PDF":
            invoices_sorted.append(file)
        if extension == ".pdf":
            invoices_sorted.append(file)
    return invoices_sorted


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


def search_total(input):
    input = input.replace(',','')
    total = ""
    sorted_ammounts = []
    totals = re.findall(r'\d+\.\d+', input, re.MULTILINE)
    if totals != []:
        for item in totals:
            sorted_ammounts.append(float(item))
        sorted_ammounts.sort()
        total = sorted_ammounts[-1]
    return total


def search_description(input):
    description = ""
    space = " "
    input_list = input.split('\n')
    for item in input_list:
        classification = auto_classifier(vectorizer, classifier, item)
        if classification == 3:
            description = description + item + space
    description = description[:200]
    return description


def search_contractor(contractor_details, input, filename):
    contractor = ""
    contractor_number = ""
    contractor_details.reset_index()
    for index, row in contractor_details.iterrows():
        contractor = row["ContractorName"]
        contractor_number = row["ContractorCompanyNumber"]
        text = input.upper()
        matches = find_near_matches(contractor, text, max_l_dist=1)
        if matches != []:
            for m in matches:
               score = fuzz.ratio(contractor,m.matched)
               if score > 90:
                   return row["ContractorName"], row["ContractorCompanyNumber"]
    contractor = ""
    contractor_number = ""
    return contractor, contractor_number


def search_date(text):
    date_regex = '([0-9]{1,2}[\/\.-][0-9]{1,2}'\
                 '[\/\.-][0-9]{2,4}|[0-9]{2,4}'\
                 '[\/\.-][0-9]{1,2}[\/\.-][0-9]{1,2})'
    date__words_regex = '([0-9]{1,2}[\s]'\
                        '(January|February'\
                        '|March|April|May|June'\
                        '|July|August|September|October|'\
                        'November|December|'\
                        'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|'\
                        'Oct|Nov|Dec)'\
                        '[\s][0-9]{2,4})'

    date_list = re.findall(fr'{date_regex}', text, re.MULTILINE)
    date_list_words = re.findall(
                                    fr'{date__words_regex}',
                                    text,
                                    re.MULTILINE|re.IGNORECASE
    )

    sorted_date_list = []

    if date_list != []:
        for item in date_list:
            new_item = date_sort(item)
            if new_item != "":
                sorted_date_list.append(new_item)

    if date_list_words != []:
        for item in date_list_words:
            new_item = date_sort(item[0])
            if new_item != "":
                sorted_date_list.append(new_item)

    sorted_date_list.sort()

    try:
        date = sorted_date_list[0]
    except:
        date = ""
    return date


def date_sort(date):
    try:
        datetimeobject = datetime.strptime(date, '%d/%m/%Y')
        date = datetimeobject.strftime('%Y-%m-%d')
    except:
        try:
            datetimeobject = datetime.strptime(date, '%d/%m/%y')
            date = datetimeobject.strftime('%Y-%m-%d')
        except:
            try:
                datetimeobject = datetime.strptime(date, '%d %B %Y')
                date = datetimeobject.strftime('%Y-%m-%d')
            except:
                try:
                    datetimeobject = datetime.strptime(date, '%d.%m.%y')
                    date = datetimeobject.strftime('%Y-%m-%d')
                except:
                    try:
                        datetimeobject = datetime.strptime(date, '%d.%m.%Y')
                        date = datetimeobject.strftime('%Y-%m-%d')
                    except:
                        try:
                            datetimeobject = datetime.strptime(date, '%d %B %Y')
                            date = datetimeobject.strftime('%Y-%m-%d')
                        except:
                            try:
                                datetimeobject = datetime.strptime(
                                                                date,
                                                                '%d %b %Y'
                                )
                                date = datetimeobject.strftime('%Y-%m-%d')
                            except:
                                date = ""
    return date


def extract_details_using_csv_values(
                                        company_name, contractor_number,
                                        company_num, company_post_code,
                                        company_category, method
):
    if contractor_number != "":
        companies = search_company_number(contractor_number)
        for company in companies:
            company_name = company.CompanyName
            company_num = company.CompanyNumber
            company_post_code = company.RegAddress_PostCode
            company_category = company.SICCode_SicText_1
            method = "CSV Match"

    return (
            company_name, company_num,
            company_post_code, company_category, method
    )


def extract_details_from_receipts(path):

    return_data = pd.DataFrame()

    invoices_sorted = get_invoice_files(path)
    invoices_sorted.sort()

    contractor_details = pd.read_csv(
                                        os.path.join(script_path,
                                        "training_data/contractor_details.csv"
    ))

    number_of_invoices = len(invoices_sorted) - 1
    invoice_no = 1

    for invoice in invoices_sorted:

        company_name = ""
        company_num = ""
        company_post_code = ""
        company_category = ""
        method = ""
        contractor = ""
        contractor_number = ""

        new_path = os.path.join(path, invoice)
        image = os.path.join(script_path, "temp.jpg")

        convert_to_temp_jpeg(new_path)

        text = extract_text_from_image(image)

        contractor, contractor_number = search_contractor(
                                                            contractor_details,
                                                            text, invoice
        )

        if contractor_number != "":
            company_name, company_num,\
            company_post_code,\
            company_category, method = extract_details_using_csv_values(
                                                company_name, contractor_number,
                                                company_num, company_post_code,
                                                company_category, method
            )

        date = search_date(text)
        total = search_total(text)
        description = search_description(text)
        text_display = text.replace('\n',' ')

        display_text =  f'Invoice no:\t\t{invoice_no}/{number_of_invoices}\n'\
                        f'Filename:\t\t{invoice}\n'\
                        f'Total:\t\t\t£{total}\n'\
                        f'Date:\t\t\t{date}\n'\
                        f'Company Name:\t\t{company_name}\n'\
                        f'Company Number:\t\t{company_num}\n'\
                        f'Company Post Code:\t{company_post_code}\n'\
                        f'Category:\t\t{company_category}\n'\
                        f'Description:\t\t{description}\n\n'\

        if company_name == "":
            additional =f'--------------------------------------\n'\
                        f'{text_display}\n'\
                        f'--------------------------------------\n\n'
            display_text = display_text + additional

        print(display_text)

        df2add = pd.DataFrame({
                    'Filename': [invoice],
                    'Total': [total],
                    'Invoice Date': [date],
                    'Company Name': [company_name],
                    'Company Number': [company_num],
                    'Company Post Code': [company_post_code],
                    'Category': [company_category],
                    'Description': [description],
                    'Extracted Text': [text]
        })

        return_data = pd.concat(
                        [return_data, df2add],
                        ignore_index = True,
                        axis = 0
        )

        invoice_no = invoice_no + 1

    return return_data
