#!/usr/bin/env python3

import cv2
import re
import os
import json
import pathlib
import pandas as pd
import subprocess
import applescript
from getkey import getkey
from tkinter import filedialog
from PIL import Image
from pdf2image import convert_from_path

from models import Config, generate_text_line
from auto_labeller import build_auto_classifier, auto_classifier
from invoice_extractor import extract_details_from_receipts, sort_invoice_files
from invoice_extractor import convert_to_temp_jpeg, get_file_extension

Config.index = 0
Config.script_path = os.path.dirname(os.path.realpath(__file__))
Config.thin_line = generate_text_line("thin")
Config.thick_line = generate_text_line("thick")
Config.path = Config.script_path


# Saves the current state of "database" and the folder path to disk
def save_and_quit(receipt_details):
    json_database = receipt_details.to_json(orient="index")
    with open(os.path.join(Config.script_path, 'data_save.dat'), 'w') as f:
        f.write(json.dumps(json_database))
    with open(os.path.join(Config.script_path, 'path.dat'), 'w') as f:
        f.write(json.dumps(Config.path))


# Restores the last saved "database" from disk, along with the working
# reeipt folder path
def restore():
    with open(os.path.join(Config.script_path, 'data_save.dat'), 'r') as f:
        json_database = json.loads(f.read())
        receipt_details = pd.read_json(json_database,orient="index")
    with open(os.path.join(Config.script_path, 'path.dat'), 'r') as f:
        Config.path = json.loads(f.read())
    return receipt_details


# Displays a given jpeg file to screen
def display_image(img, file):
    test = Image.open(img)
    test.show()


# Clears the termiaal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# displays a dialogue window to select an input folder
def select_folder_diag():
    selected = filedialog.askdirectory()
    if selected == '':
        selected = Config.script_path
    return selected


# Processes the main menu selection options, I.e when 'f' is pressed it openes
# a folder dialogue menu to select the input folder
def main_menu_selection(receipt_details):
    invoices = []
    while True:
        key = getkey()
        if key == "f":
            Config.path = select_folder_diag()
            # invoices = os.listdir(os.path.expanduser(Config.path))
            invoices = sort_invoice_files(Config.path)
            if invoices != []:
                main_menu()
            else:
                print("This folder has no PDF files")
        if key == 'q':
            save_and_quit(receipt_details)
            clear_screen()
            quit()
        if key == 'p':
            # invoices = os.listdir(os.path.expanduser(Config.path))
            invoices = sort_invoice_files(Config.path)
            if invoices != []:
                clear_screen()
                receipt_details = extract_details_from_receipts(Config.path)
                print("Finished Extraction")
                return receipt_details
            else:
                print("This folder has no PDF files")
        if key == 'r':
            receipt_details = restore()
            no_of_invoices = len(receipt_details.index)
            Config.index = 0
            invoice_menu(receipt_details, no_of_invoices)
            invoice_browser(receipt_details, no_of_invoices)


# Processes the invoice screen menu options
def invoice_browser(receipt_details, no_of_invoices):
    last_invoice = no_of_invoices - 1
    while True:
        key = getkey()
        if key == "s":
            file = receipt_details.loc[Config.index,'Filename']
            filename = os.path.join(Config.path, file)
            convert_to_temp_jpeg(filename)
            display_image(os.path.join(Config.script_path, 'temp.jpg'), file)
        if key == '.':
            Config.index = Config.index + 1
            if Config.index > last_invoice:
                Config.index  = last_invoice
            invoice_menu(receipt_details, no_of_invoices)
        if key == ',':
            Config.index = Config.index - 1
            if Config.index  < 0:
                Config.index = 0
            invoice_menu(receipt_details, no_of_invoices)
        if key == 'q':
            save_and_quit(receipt_details)
            clear_screen()
            quit()
        if key == 'x':
            clear_screen()
            while True:
                filename = input("Please enter file name: ")
                if filename != "":
                    output_folder = select_folder_diag()
                    receipt_details.to_excel(os.path.join(
                                                            output_folder,
                                                            f"{filename}.xlsx"
                    ))
                    invoice_menu(receipt_details, no_of_invoices)
                    print(
                            f"Exported to "\
                            f"{os.path.join(output_folder,f'{filename}.xlsx')}"
                    )
                    break


# Displays the main menu
def main_menu():
    clear_screen()
    print(Config.thick_line)
    print("\nInvoice Scanner - 2022 - E.Spencer")
    print("Version 2.0 Beta")
    print("\nThis invoice extraction tool is free for personal use.")
    print("It comes with no warranty and is used entirely")
    print("at your own discretion. By proceeding you accept these terms.\n")
    print(Config.thick_line)
    print('\n[R] Restore from disk\t\t\t[P] Process')
    print('[F] Select input folder\t\t\t[Q] Quit')
    print(f'\nInput folder:\t{Config.path[0:49]}')
    print(f'\t\t{Config.path[49:102]}')
    print(f'\t\t{Config.path[102:147]}')
    print(Config.thick_line)


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
def invoice_menu(receipt_details, no_of_invoices):
    invoice_num = Config.index + 1
    clear_screen()

    top_menu = \
                f'{Config.thick_line}\n'\
                f'Invoice {invoice_num}/{no_of_invoices}\n'\
                f'{Config.thin_line}\n'\
                'Press < or > to move between invoices\n'\
                f'{Config.thin_line}\n'\
                'Extracted Text:\n'\
                f'{Config.thick_line}'

    print(top_menu)

    display_invoice(
            receipt_details.loc[Config.index,'Extracted Text']
    )

    filename = receipt_details.loc[Config.index,'Filename']
    total = receipt_details.loc[Config.index,'Total']
    date = receipt_details.loc[Config.index,'Invoice Date']
    company_name = receipt_details.loc[Config.index,'Company Name']
    company_number = receipt_details.loc[Config.index,'Company Number']
    company_post_code = receipt_details.loc[Config.index,'Company Post Code']
    category = receipt_details.loc[Config.index,'Category']
    description = receipt_details.loc[Config.index,'Description']

    print(Config.thick_line)

    invoice_details = \
                f'{"File Name:":<20}{filename[0:45]:<30}\n'\
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
    print(Config.thin_line)
    print('[S] Show orginal invoice file')
    print(Config.thin_line)
    print('[X] Eport\t\t\t\t[Q] Save and Quit')
    print(Config.thick_line)
    return


# Resizes the Terminal (OSX) window using Apple Script
def resize_window():
    command = applescript.tell.app("Terminal",'''
    set bounds of window 1 to {50, 90, 530, 950}
    ''')
    assert command.code == 0, command.err


# Main function, launches main menu
def main():
    receipt_details = restore()
    resize_window()
    main_menu()
    receipt_details = main_menu_selection(receipt_details)
    no_of_invoices = len(receipt_details.index)
    invoice_menu(receipt_details, no_of_invoices)
    invoice_browser(receipt_details, no_of_invoices)


if __name__ == '__main__':
    main()
