#!/usr/bin/env python3

import cv2
import re
import os
import json
import shutil
import pathlib
import pytesseract
from pytesseract import Output
from datetime import datetime
from getkey import getkey
from tkinter import *
from tkinter import filedialog
from PIL import Image
from pdf2image import convert_from_path
from auto_labeller import build_auto_classifier, auto_classifier
import ssl
import certifi
from invoice_extractor import extract_details_from_receipts, convert_to_temp_jpeg
import pandas as pd
import numpy

script_path = os.path.dirname(os.path.realpath(__file__))

# Saves the current state of "database" and the folder path to disk
def save_and_quit(database, path, script_path):
    json_database = database.to_json(orient="index")

    with open(os.path.join(script_path, 'data_save.dat'), 'w') as f:
        f.write(json.dumps(json_database))
    with open(os.path.join(script_path, 'path.dat'), 'w') as f:
        f.write(json.dumps(path))


# Restores the last saved "database" from disk, along with the working
# reeipt folder path
def restore():
    with open(os.path.join(script_path, 'data_save.dat'), 'r') as f:
        database = json.loads(f.read())
        restored_df = pd.read_json(database,orient="index")
    with open(os.path.join(script_path, 'path.dat'), 'r') as f:
        path = json.loads(f.read())
    return restored_df, path


# Displays a given jpeg file to screen
def display_image(img, file):
    test = Image.open(img)
    test.show()


# Clears the termiaal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# displays a dialogue window to select an input folder
def select_input_folder(path):
    selected = filedialog.askdirectory()
    if selected == '':
        selected = script_path
    return selected


# Processes the main menu selection options, I.e when 'f' is pressed it openes
# a folder dialogue menu to select the input folder
def main_menu_selection(path):
    invoices = []
    while True:
        key = getkey()
        if key == "f":
            path = select_input_folder(script_path)
            invoices = os.listdir(os.path.expanduser(path))
            if invoices != []:
                main_menu(path)
            else:
                print("This folder is empty")
        if key == 'q':
            clear_screen()
            quit()
        if key == 'p':
            if invoices != []:
                clear_screen()
                receipt_details = extract_details_from_receipts(path)
                print("Finished Extraction")
                return receipt_details, path
            else:
                print("This folder is empty")
        if key == 'r':
            receipt_details, path = restore()
            no_of_invoices = len(receipt_details.index)
            index = 0
            invoice_menu(receipt_details, index, no_of_invoices)
            invoice_browser(receipt_details, index, no_of_invoices, path)


# Processes the invoice screen menu options, I.e when '[' or ']' are pressed it
# scrolls the displayed invoice up or down
def invoice_browser(receipt_details, index, no_of_invoices, path):
    last_invoice = no_of_invoices - 1
    start = 0
    end = 0
    while True:
        key = getkey()
        if key == "s":
            file = receipt_details.loc[index,'Filename']
            filename = os.path.join(path, file)
            convert_to_temp_jpeg(filename)
            display_image(os.path.join(script_path, 'temp.jpg'), file)
        if key == '.':
            index = index + 1
            if index > last_invoice:
                index = last_invoice
            invoice_menu(receipt_details, index, no_of_invoices)
        if key == ',':
            index = index - 1
            if index < 0:
                index = 0
            invoice_menu(receipt_details, index, no_of_invoices)
        if key == 'q':
            save_and_quit(receipt_details, path, script_path)
            clear_screen()
            quit()
        if key == 'x':
            receipt_details.to_excel(os.path.join(script_path, "output.xlsx"))
            print(f"Exported to {os.path.join(script_path, 'output.xlsx')}")


# Displays a line on screen, either 'thick' or 'thin'
def print_line(size):
    end = 65
    length = 0
    if size == "thick":
        symbol = "="
    if size == "thin":
        symbol = '-'
    line = ''
    while length < end:
        line = (line + symbol)
        length = length + 1
    return line


# Displays the main menu
def main_menu(path):
    clear_screen()
    line = print_line("thick")
    print(line)
    print("\nInvoice Scanner - 2022 - E.Spencer")
    print("Version 1.0 Beta")
    print("\nThis invoice extraction tool is free for personal use.")
    print("It comes with no warranty and is used entirely")
    print("at your own discretion. By proceeding you accept these terms.\n")
    print(line)
    print('\n[R] Restore from disk\t\t\t[P] Process')
    print('[F] Select input folder\t\t\t[Q] Quit')
    print(f'\nInput folder:\t{path[0:49]}')
    print(f'\t\t{path[49:102]}')
    print(f'\t\t{path[102:147]}')
    print(line)


# Displays the invoice within the invoice menu, and permits the user to scroll
# up and down across the invoice
def display_invoice(input):
    invoice_list = input.split('\n')
    show_list = []
    start = 0
    end = 30
    for line in invoice_list:
        if line != "":
            show_list.append(line)
    while len(show_list) < 30:
        show_list.append("")
    show_list = show_list[start:end]
    for line in show_list:
        crop = line[0:65]
        print(crop)
    return


# This displays the standard menu within terminal for browsing invoices
def invoice_menu(receipt_details,index,no_of_invoices):
    invoice_num = index + 1
    clear_screen()

    line1 = print_line("thick")
    line2 = print_line("thin")

    print(line1)
    print(f"Invoice {invoice_num}/{no_of_invoices}")
    print(line2)
    print('Press < or > to move between invoices')
    print(line2)
    print('Extracted Text:')
    print(line1)

    display_invoice(
            receipt_details.loc[index,'Extracted Text']
    )

    filename = receipt_details.loc[index,'Filename']
    total = receipt_details.loc[index,'Total']
    date = receipt_details.loc[index,'Invoice Date']
    company_name = receipt_details.loc[index,'Company Name']
    company_number = receipt_details.loc[index,'Company Number']
    company_post_code = receipt_details.loc[index,'Company Post Code']
    category = receipt_details.loc[index,'Category']
    description = receipt_details.loc[index,'Description']

    print(line1)

    invoice_details = f'{"File Name:":<20}{filename[0:45]:<30}\n'\
                f'{"Total:":<20}{total:<30}\n'\
                f'{"Date":<20}{date:<30}\n'\
                f'{"Company Name:":<20}{company_name[0:45]:<30}\n'\
                f'{"Company Number:":<20}{company_number[0:45]:<30}\n'\
                f'{"Company Post Code:":<20}{company_post_code[0:45]:<30}\n'\
                f'{"Category:":<20}{category[0:45]:<30}\n'\
                f'{"Description:":<20}{description[0:45]:<30}\n'\
                f'{"":<20}{description[45:90]:<30}\n'\
                f'{"":<20}{description[90:135]:<30}\n'\
                f'{"":<20}{description[135:180]:<30}\n'\

    print(invoice_details)
    print(line2)
    print('[S] Show orginal invoice file')
    print(line2)
    print('[X] Eport\t\t\t\t[Q] Save and Quit')
    print(line1)
    return


# Main function, launches main menu
def main():
    main_menu(script_path)
    receipt_details, path = main_menu_selection(script_path)
    no_of_invoices = len(receipt_details.index)
    index = 0
    invoice_menu(receipt_details, index, no_of_invoices)
    invoice_browser(receipt_details, index, no_of_invoices, path)

if __name__ == '__main__':
    main()
