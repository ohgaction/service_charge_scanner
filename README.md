# Service Charge Scanner

## OHG action invoice scanner

This tool currently works by searching text extracted from PDF files, looking for patterns and matching them to a list of known contractors and addresses.

The next iteration will use machine learning to do this more automatically with less input. However, for now, I think it's still very useful for people to scan large numbers of receipts in an hour or two rather than the days it would otherwise take

## How to use the scanner

### Scanning a folder

When you run the scanner, you press the **F** key to select a folder of receipts to scan. A dialogue window will appear. Select where you've saved your PDF files.

Press the **P** key and it will start processing. Once it has finished it will display a text display of each receipt. You can navigate between the receipts using the < or > keys, and you can scroll up and down using [ and ] keys (you may need to stretch the terminal window open a bit, as it sometimes crops the top of the display)

### How to see what data is extracted

Below the scrolling part of the display, which shows the text it has extracted from the invoice, you will see the fields it has collated. If the contractor is not displayed, I recommend copying the name of the contractor from the extracted text.

### How to add a contractor

You can then press the **A** key to add the contractor to the database. You can paste (CMD+V or CONTROL+V) the contractor here.

Once you hit enter, you should see that all receipts with this contractor have been updated when you navigate **<** and **>** through the receipts. If you find another receipt with a missing contractor, repeat until all the contractors have been filled in. You only need to add the names of contractors once, after this they are stored in the database for each subsequent time you use the tool.

### How to add an address

You essentially do the same to detect the address (if you want this in your data). But instead of using the **A** key, you use the **D** key to add an address to the database.

The total is automatically calculated by creating a list of totals from the receipt and then taking the highest value. This normally works fine, but you may find a few receipts where this is inaccurate. If you want to change a total press the C key.

### How to see the original invoice

You can use the **S** key at any time to show you the original PDF file

### How to extract a description

The Trim description can be used if you press the **T** key. You can now use the [ and the ] keys to trim down the receipt data to only show the description. Press T again to save this. In the next version, I'm going to look at doing this automatically using machine learning to detect descriptions.

### How to export results into a spreadsheet

When you are finished checking the invoices, press the X key and it will export a CSV file to the script folder. If you have installed as per the installation instructions this folder will be on your desktop called with Invoice_scanner_Windows or Invoice_scanner_macOS

if you load this you should see your results as a spreadsheet. This file can be easily imported into Excel or Google Sheets:

https://support.microsoft.com/en-us/office/import-or-export-text-txt-or-csv-files-5250ac4c-663c-47ce-937b-339e391393ba

### Future versions

In the final version, it will automatically export Excel files and will allow you to change the output directory and filename.

## Installation (Windows)

1. The first thing you’ll need to install is an update to Windows called **Visual C++ Redistributable for Visual Studio 2015**. You can download this using the following link:

https://www.microsoft.com/en-gb/download/details.aspx?id=48145

When asked, select the **vc_dedist.x64.exe.**

Open the **.exe** file that downloads and follow the onscreen instructions to install

**Note:** It is possible you already have this, or a newer update installed. If this is the case Windows will warn you and you can skip this step.

2. Next you need to install **Python**. Python is the programming language the script has been made with. This can be downloaded from here.

https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe

Run the python installer.

**Make sure to tick the box at the bottom of the menu that says Add Python 3.10 to Path and then click on Install Now**

3. Click on the **Start** button in Windows and type **PowerShell**. Right-click on Windows **PowerShell** and select **Run as Administrator**

Type the following command (copy & paste) into **PowerShell** and hit enter:

`pip install –upgrade pip`

Once pip has finished updating, please enter the following command (copy & paste).

`pip3 install tk opencv-python keyboard pytesseract pdf2image`

This will install the python dependencies.

4. Now you need to download the script from github. Please download from this link, and click download in the right hand corner:

https://github.com/ohgaction/service_charge_scanner/blob/main/downloads/Invoice_scanner_Windows.zip

Once the **.zip** file is downloaded, please move or copy it to the desktop

Right click on the **.zip** file and select **Extract All**

Please delete the end of the path which says **Invoice_scanner_Windows**. The address will be extracted to will look like the below example:

`C:\Users\{Your_User_Name_Here}\Desktop\`

5. You need to install **Tesseract**. This is the actual OCR software that is used by the script to read text from images. You can download tesseract from the following link:

https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.1.20220118.exe

Please open the **.exe** file that is downloaded and follow the instructions

Please make sure to install Tesseract into the default location `C:\Program Files\Tesseract-OCR`

6. Now you need to install **poppler**. This is software which converts PDF files to image files. We use poppler to convert PDFs into JPEG files temporarily so that the OCR software can read them. Please use this link to download poppler:

https://github.com/oschwartz10612/poppler-windows/releases/download/v22.01.0-0/Release-22.01.0-0.zip

Once the .zip file is downloaded, please open it. Right click on the folder called **poppler-22.01.0** and click **cut**

Now navigate to your Desktop, where we put the script folder. Please open the folder called **Invoice_scanner_Windows**. Now right-click and select **Paste**.

7. The final step is to set an **environmental variable**. This is so that poppler will work from the command line, and permit the script to run.

Click on the start menu and type **View Advanced System Settings**. Open this

In the bottom right of the menu, select **Enviroment Variables**

In the bottom half of the next window, highlight **Path** and select **Edit**

Click New and then **Browse** to the following directory **Desktop\Invoice_scanner_Windows\poppler-20.01.0\Library\bin**

Click Ok. Make sure to close **PowerShell** if it’s open

8. Relaunch **PowerShell** from the start menu, right clicking again to launch it as an Administrator. Type ‘python’ making sure to leave a space. Next drag the file called OHG_Action_Receipt_Processor.py from the Invoice_scanner_Windows folder on your desktop into the **PowerShell** window. This should look something like this:

`python C:\Users\{Your_User_Name_Here}\Desktop\Invoice_scanner_Windows\OHG_Action_Receipt_Processor.py`

Press Enter and the script should run

## Installation (macOS)

1. Open Terminal

You can do this by clicking on the magnifying glass in the top right hand corner of the screen.

Type:

`su`

Press Enter. This command elevates Terminal so you can run as a super user. You will be prompted for your password. Note that when you type it, it will not display on the screen. Press enter.

2. Next, you need to install **Brew**. This is a package manager for macOS. To install Brew simply copy and paste the entire text below into terminal and hit enter.

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

3. Next we can install **Python**. Python is the programming language that is used to write this script. To install python simply type the following

`brew install pytho`

4. Next we need to install **Tesseract**. This is the plugin that reads an image and converts it to text using OCR character recognition. We do this by typing

`brew install tesseract`

5. Next we need to install the **python dependencies** for the script to actually run. Please copy and paste the line below into Terminal

`pip3 install tk pdf2image opencv-python json getkey pytesseract`

6. Now download the script from this location:
https://github.com/ohgaction/service_charge_scanner/blob/main/downloads/invoice_scanner_macOS.zip

Click on the **Download** link to the right of the screen.

Please move this **.zip** file to your Desktop. You can do this in Chrome by clicking **Show in Finder** on the file you’ve just downloaded.

Now drag the **.zip** file to your desktop:

Double click the **.zip** file on the desktop, and it will expand into a folder:

You can drag the **.zip** file to the Recycling bin now as you’re done with it.

7. Now we’re ready to run the script. To do this, please go back to Terminal and type (or copy and paste)

`python ~/Desktop/Invoice_scanner_macOS/OHG_Action_Receipt_Processor.py`

The script will now launch
