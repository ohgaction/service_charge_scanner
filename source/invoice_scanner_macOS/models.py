#!/usr/bin/env python3

from app import db

class Company(db.Model):
    """"""
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String)
    CompanyNumber = db.Column(db.String)
    RegAddress_CareOf = db.Column(db.String)
    RegAddress_POBox = db.Column(db.String)
    RegAddress_AddressLine1 = db.Column(db.String)
    RegAddress_AddressLine2 = db.Column(db.String)
    RegAddress_PostTown = db.Column(db.String)
    RegAddress_County = db.Column(db.String)
    RegAddress_Country = db.Column(db.String)
    RegAddress_PostCode = db.Column(db.String)
    SICCode_SicText_1 = db.Column(db.String)


class Config:
    def __init__(
                    index,
                    script_path,
                    path,
                    line_thin,
                    line_thick,
                    receipt_details
    ):
        self.index
        self.script_path
        self.path
        self.line_thin
        self.line_thick
        self.receipt_details


# Displays a line on screen, either 'thick' or 'thin'
def generate_text_line(size):
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
