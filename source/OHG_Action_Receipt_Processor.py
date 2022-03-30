import pytesseract
from pytesseract import Output
from datetime import datetime
import cv2
import re
import os
import shutil
import pathlib
from pdf2image import convert_from_path
from getkey import getkey
from tkinter import *
from tkinter import filedialog
from PIL import Image
import textwrap
import json

# "database" is the working list of list that contains all extracted invoices

# Saves the current state of "database" and the folder path to disk
def save_and_quit(database,path,script_path):

    with open(f'{script_path}/data_save.dat', 'w') as f:
        f.write(json.dumps(database))

    with open(f'{script_path}/path.dat', 'w') as f:
        f.write(json.dumps(path))


# Restores the last saved "database" from disk, along with the working
# reeipt folder path
def restore(script_path):

    with open(f'{script_path}/data_save.dat', 'r') as f:
        database = json.loads(f.read())

    with open(f'{script_path}/path.dat', 'r') as f:
        path = json.loads(f.read())

    return database,path


# Pulls a list of addresses and contractors from disk
def config(script_path):

    file = open(f"{script_path}/addresses.txt", "r")
    addresses = file.read()
    addresses_list = addresses.split('\n')
    file.close()

    file = open(f"{script_path}/contractors.txt", "r")
    contractors = file.read()
    contractors_list = contractors.split('\n')
    file.close()

    file = open(f"{script_path}/jobcode.txt", "r")
    jobcode = file.read()
    job_codes_list = jobcode.split('\n')
    file.close()

    return addresses_list, contractors_list, job_codes_list


# Wipes the output.csv file from the scipt directory
def wipe_csv():

    open(f'output.csv', 'w').close()


# appends a line to the output.csv file, and outputs the extracted data
def write_csv(input):

    try:
        with open(f'output.csv', 'a', encoding='utf-8') as f:
            f.write(input)

    except:
        messagebox.showinfo("showwarning", "Could not modify CSV File")
        gui.mainloop()
        return


# Appeneds a contractor to the contractors.txt file
def add_contractor(contractor):

    file = open("contractors.txt", "a")
    file.write(f'{contractor}\n')
    file.close()


# Appends an address to the addesses.txt file
def add_address(address):

    file = open("addresses.txt", "a")
    file.write(f'{address}\n')
    file.close()


# Convers the current PDF file to a JPEG file so it's text can be scanned
def convert_to_temp_jpeg(filepath,script_path):

    try:

        if os.path.isfile(filepath) == True:
            pages = convert_from_path(
                                        filepath,
                                        dpi=150,
                                        grayscale=True,
                                        fmt='jpeg',
                                        jpegopt={"quality":100,"optomise":True}
            )

            for page in pages:
                page.save(f'{script_path}/temp.jpg', 'JPEG')

    except:

        print("Not a supported file")


# Extracts the file extension of a given file
def get_file_extension(file):

    file_extension = pathlib.Path(file).suffix
    return file_extension


# Searches input text for a given list of job numbers
def search_for_invoice_no(input_list, input):

    result = ""
    for item in input_list:
        search = re.findall(fr'{item}', input, re.MULTILINE)
        if search != []:
            result = search[0]
            return result


# Searches given input text for a list of items
def search_item(input_list, input):

    result = ""
    for item in input_list:
        search = re.findall(fr'{item}', input)
        if search != []:
            result = search[0]
            return result


# Searches given input text for a total, which is integer  with
# decimal point, I.e 99.99
def search_total(input):

    total = ""
    sorted_ammounts = []
    totals = re.findall(r'\d+\.\d+', input, re.MULTILINE)
    if totals != []:
        for item in totals:
            sorted_ammounts.append(float(item))
        sorted_ammounts.sort()
        total = sorted_ammounts[-1]
    return total


# Searches given input text for a list of dates
def serarch_date(text):

    date_regex = "[0-9]{1,2}[\/\.-][0-9]{1,2}[\/\.-][0-9]{2,4}"
    date = ""
    date_list = re.findall(fr'{date_regex}', text, re.MULTILINE)
    if date_list != []:
        date_list.sort()
        date_list = date_list[0]
        date_list = date_sort(date_list)
    if date == "":
        date = date_list
    return date


# Sorts a date into the correct YYYY-MM-DD format so it is easy to sort
# in an excel spreadsheet
def date_sort(date):

    try:
        datetimeobject = datetime.strptime(date,'%d/%m/%Y')
        date = datetimeobject.strftime('%Y-%m-%d')
    except:
        try:
            datetimeobject = datetime.strptime(date,'%d %B %Y')
            date = datetimeobject.strftime('%Y-%m-%d')
        except:
            try:
                datetimeobject = datetime.strptime(date,'%d.%m.%y')
                date = datetimeobject.strftime('%Y-%m-%d')
            except:
                try:
                    datetimeobject = datetime.strptime(date,'%d.%m.%Y')
                    date = datetimeobject.strftime('%Y-%m-%d')
                except:
                    date = ""
    return date


# Uses pytesseract to extract text information from a given jpeg image
def extract_text_from_image(img):

    image = cv2.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(image)
    return text


# Displays a given jpeg file to screen
def display_image(img, file):

    test = Image.open(img)
    test.show()


# Clears the termiaal
def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')


# displays a dialogue window to select an input folder
def select_input_folder(script_path):

    selected = filedialog.askdirectory()
    if selected == '':
        selected = script_path
    return selected


# This is the text that is displayed at the top of the "trim" selection screen
def trim_screen_text():

    print('[T] Accept Trim')
    print('Use [ and ] to trim the description')
    print('Use < and > to reduce the trim')
    print("=================================================================")


# This is the menu that allows you to navigate the "trim" selection screen
def trim_menu(input):

    clear_screen()
    trim_screen_text()

    description_list = input.split('\n')
    end_of_description_list = len(description_list)

    start = 0
    end = end_of_description_list

    show_list = description_list[start:end]
    for line in show_list:
        print(line)

    while True:
        description = ""
        key = getkey()

        if key == "[":

            clear_screen()
            start = start + 1
            if start > end:
                start = end
            show_list = description_list[start:end]
            trim_screen_text()
            for line in show_list:
                print(line)

        if key == ']':

            clear_screen()
            end = end - 1
            if end < 0:
                end = 0
            show_list = description_list[start:end]
            trim_screen_text()
            for line in show_list:
                print(line)

        if key == ",":

            clear_screen()
            start = start - 1
            if start < 0:
                start = 0
            show_list = description_list[start:end]
            trim_screen_text()
            for line in show_list:
                print(line)

        if key == '.':

            clear_screen()
            end = end + 1
            if end > end_of_description_list:
                end = end_of_description_list
            show_list = description_list[start:end]
            trim_screen_text()
            for line in show_list:
                print(line)

        if key == 't':

            description = ' '.join(show_list)
            return description


def extract_data(
                    file, path, addresses,
                    contractors, job_codes, script_path
):

    filename = f'{path}/{file}'
    convert_to_temp_jpeg(filename,script_path)
    return_text = extract_text_from_image(f'{script_path}/temp.jpg')
    return_text_no_commas = return_text.replace(',','')
    date_text = serarch_date(return_text)
    supplier = search_item(contractors, return_text)
    address = search_item(addresses, return_text)
    total_text = search_total(return_text_no_commas)
    if date_text == [] or None:
        date_text = ""
    job_code = search_for_invoice_no(job_codes, return_text)

    return return_text, return_text_no_commas, date_text, supplier, address, total_text, job_code


def extract_data_rescan(
                                return_text, addresses,
                                contractors, job_codes
):

    return_text_no_commas = return_text.replace(',','')
    date_text = serarch_date(return_text)
    supplier = search_item(contractors, return_text)
    address = search_item(addresses, return_text)
    total_text = search_total(return_text_no_commas)
    if date_text == [] or None:
        date_text = ""
    job_code = search_for_invoice_no(job_codes, return_text)

    return return_text, return_text_no_commas, date_text, supplier, address, total_text, job_code


def get_multiple_invoices_from_path(
                                        path,addresses,contractors,
                                        script_path,job_codes
):

    database = []
    invoices_sorted = []
    no_files = False

    invoices = os.listdir(os.path.expanduser(path))

    for file in invoices:
        extension = get_file_extension(file)
        if extension == ".PDF":
            invoices_sorted.append(file)
        if extension == ".pdf":
            invoices_sorted.append(file)

    if invoices_sorted == []:
        print("No PDF files found in supplied folder")
        no_files = True
        return database, no_files

    for sorted_file in invoices_sorted:
        date_text = ""
        total_text = ""
        clear_screen()
        print(f"Scanning: {sorted_file}...")

        return_text, return_text_no_commas, date_text, supplier,\
        address, total_text, job_code = extract_data(
                                        sorted_file, path,
                                        addresses, contractors,
                                        job_codes, script_path
        )

        item = []
        item.append(return_text)
        item.append(sorted_file)
        item.append(date_text)
        item.append(total_text)
        item.append(supplier)
        item.append(address)
        item.append("")
        item.append(job_code)
        database.append(item)

    return database, no_files


def get_multiple_invoices_rescan(
                                    database,path,addresses,
                                    contractors,
                                    script_path, job_codes
):

    i = 0
    for line in database:
        text_to_rescan = line[0]

        return_text, return_text_no_commas, date_text,\
        supplier, address, total_text, job_code = extract_data_rescan(
                                                    text_to_rescan, addresses,
                                                    contractors,
                                                    job_codes
        )

        database[i][0] = return_text
        database[i][2] = date_text
        database[i][3] = database[i][3]
        if database[i][4] == "":
            database[i][4] = supplier
        else:
            database[i][4] = database[i][4]
        database[i][5] = address
        database[i][6] = database[i][6]
        database[i][7] = job_code
        i = i + 1

    return database


def main_menu_selection(script_path):

    path = script_path
    addresses, contractors, job_codes = config(script_path)

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

            invoices = os.listdir(os.path.expanduser(path))
            if invoices != []:
                database, no_files = get_multiple_invoices_from_path(
                                                    path,addresses,contractors,
                                                    script_path,job_codes
                )
                return database, no_files, path
            else:
                print("This folder is empty")

        if key == 'r':

            no_files = False
            database,path = restore(script_path)
            return database, no_files, path


def invoice_menu_selection(
                            index,path,addresses,contractors,
                            database,last_invoice,no_of_invoices,script_path
):

    long_text = database[index][0]
    invoice_list = long_text.split('\n')
    end_of_invoice_list = len(invoice_list)
    end_of_display = end_of_invoice_list - 20

    start = 0
    end = 20

    while True:
        key = getkey()

        if key == "[":

            clear_screen()
            start = start + 1
            end = end + 1
            if start > end_of_display:
                start = end_of_display
            if end > end_of_invoice_list:
                end = end_of_invoice_list
            if end - start < 20:
                start = end - 20

            invoice_menu(database,index,no_of_invoices,start,end)

        if key == ']':

            clear_screen()
            start = start - 1
            end = end - 1
            if start < 0:
                start = 0
            if end < 20:
                end = 20
            invoice_menu(database,index,no_of_invoices,start,end)

        if key == "a":

            line = database[index]
            file = line[1]
            filename = f'{path}/{file}'
            contractor_to_add = input("Please Enter Contractor: ")
            if contractor_to_add != "":
                database[index][4] = contractor_to_add
                add_contractor(contractor_to_add)
                addresses, contractors, job_codes = config(script_path)
                new_database = get_multiple_invoices_rescan(
                                                database,
                                                path,addresses,
                                                contractors,
                                                script_path,
                                                job_codes
                )

                invoice_menu(new_database,index,no_of_invoices,start,end)
            else:
                invoice_menu(database,index,no_of_invoices,start,end)

        if key == "d":

            line = database[index]
            file = line[1]
            filename = f'{path}/{file}'
            address_to_add = input("Please Enter Address: ")
            if address_to_add != "":
                database[index][5] = address_to_add
                add_address(address_to_add)
                addresses, contractors, job_codes = config(script_path)
                new_database = get_multiple_invoices_rescan(
                                                database,
                                                path,addresses,
                                                contractors,
                                                script_path,
                                                job_codes
                )

                invoice_menu(new_database,index,no_of_invoices,start,end)
            else:
                invoice_menu(database,index,no_of_invoices,start,end)

        if key == "c":

            line = database[index]
            file = line[1]
            new_total = input("Please Enter new total: ")
            new_total = new_total.replace('£','')
            new_total = new_total.replace('$','')
            if new_total != "":
                addresses, contractors, job_codes = config(script_path)
                database[index][3] = new_total
                new_database = get_multiple_invoices_rescan(
                                                database,
                                                path,addresses,
                                                contractors,
                                                script_path,
                                                job_codes
                )

                invoice_menu(new_database,index,no_of_invoices,start,end)
            else:
                invoice_menu(database,index,no_of_invoices,start,end)


        if key == "t":

            line = database[index]
            long_text = line[0]
            addresses, contractors, job_codes = config(script_path)
            database[index][6] = trim_menu(long_text)
            new_database = get_multiple_invoices_rescan(
                                            database,
                                            path,addresses,
                                            contractors,
                                            script_path,
                                            job_codes
            )

            invoice_menu(new_database,index,no_of_invoices,start,end)

        if key == "s":

            line = database[index]
            file = line[1]
            filename = f'{path}/{file}'
            convert_to_temp_jpeg(filename,script_path)
            display_image(f'{script_path}/temp.jpg', file)

        if key == '.':

            index = index + 1
            start = 0
            end = 20
            if index > last_invoice:
                index = last_invoice
            invoice_menu(database,index,no_of_invoices,start,end)

        if key == ',':

            index = index - 1
            start = 0
            end = 20
            if index < 0:
                index = 0
            invoice_menu(database,index,no_of_invoices,start,end)

        if key == 'q':

            save_and_quit(database,path,script_path)
            clear_screen()
            quit()

        if key == 'x':

            wipe_csv()

            for line in database:

                # Remove ',' from items sent to CSV, this avoids
                # accidentally creating columns you do not want to create
                filename = str(line[1]).replace(',','')
                date = str(line[2]).replace(',','')
                total = str(line[3]).replace(',','')
                contractor = str(line[4]).replace(',','')
                address = str(line[5]).replace(',','')
                description = str(line[6]).replace(',','')

                write_csv(f"{filename},{date},{total},{contractor},{address},{description}\n")

            print(f"Exported to {script_path}/output.csv")


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
    print(line)


def main_menu(path):

    clear_screen()

    print_line("thick")
    print("\nInvoice Scanner - 2022 - E.Spencer")
    print("Version 1.0 Beta")
    print("\nThis invoice extraction tool is free for personal use.")
    print("It comes with no warranty and is used entirely")
    print("at your own discretion. By proceeding you accept these terms.\n")
    print_line("thick")
    print('\n[R] Restore from disk\t\t\t[P] Process')
    print('[F] Select input folder\t\t\t[Q] Quit')
    print(f'\nInput folder: {path}\n')
    print_line("thick")


# Displays the invoice within the invoice menu, and permits the user to scroll
# up and down across the invoice
def show_invoice(input,start,end):

    invoice_list = input.split('\n')
    end_of_invoice_list = len(invoice_list)

    if start < 0:
        start = 0
    if end > end_of_invoice_list:
        end = end_of_invoice_list

    show_list = invoice_list[start:end]

    while len(show_list) < 20:
        show_list.append("")

    for line in show_list:
        print(line)

    return start,end


# This displays the standard menu within terminal for browsing invoices
def invoice_menu(database,index,no_of_invoices,start,end):

    clear_screen()

    line = database[index]

    return_text = line[0]
    invoice_num = index + 1

    print_line("thick")
    print(f"Invoice {invoice_num}/{no_of_invoices}")
    print_line("thin")
    print('Press [ or ] to scroll up and down')
    print('Press < or > to move between invoices')
    print_line("thin")
    print('Extracted Text:')
    print_line("thick")

    show_invoice(return_text,start,end)

    filename = f'{line[1]}'
    date = f'{line[2]}'
    total = f'{line[3]}'
    contractor = f'{line[4]}'
    address = f'{line[5]}'
    description = f'{line[6]}'

    print_line("thick")
    print(f'{"File Name:":<15}{filename:<30}')
    print(f'{"Date:":<15}{date:<30}')
    print(f'{"Total":<15}{total:<30}')
    print(f'{"Contractor:":<15}{contractor:<30}')
    print(f'{"Address:":<15}{address:<30}')
    print(f'{"Description:":<15}{description:<30}')
    print_line("thin")
    print('[S] Show orginal invoice file\t\t[A] Add contractor')
    print('[D] Add address\t\t\t\t[C] Change total')
    print('[T] Trim description')
    print_line("thin")
    print('[X] Eport to CSV\t\t\t\t[Q] Save and Quit')
    print_line("thick")


# Main function, launches the main menu
def main():

    # Determins the location the script is being run from
    script_path = os.path.dirname(os.path.realpath(__file__))

    addresses, contractors, job_codes = config(script_path)

    main_menu(script_path)

    database, no_files, path = main_menu_selection(script_path)

    index = 0
    start = 0
    end = 20

    if no_files == False:

        no_of_invoices = len(database)
        last_invoice = no_of_invoices - 1

        invoice_menu(database,index,no_of_invoices,start,end)

        invoice_menu_selection(
                                index,path,addresses,contractors,
                                database,last_invoice,
                                no_of_invoices,script_path
        )

    if no_files == True:
        main()


if __name__ == '__main__':
    main()
