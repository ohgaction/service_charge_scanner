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
