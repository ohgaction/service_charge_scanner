#!/usr/bin/env python3

import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

script_path = os.path.dirname(os.path.realpath(__file__))

engine = create_engine(
            f'sqlite:///{script_path}/companies_house.sqlite', echo=True
)
Base = declarative_base()

class Company_Details(Base):

    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    CompanyName = Column(String)
    CompanyNumber = Column(String)
    RegAddress_CareOf = Column(String)
    RegAddress_POBox = Column(String)
    RegAddress_AddressLine1 = Column(String)
    RegAddress_AddressLine2 = Column(String)
    RegAddress_PostTown = Column(String)
    RegAddress_County = Column(String)
    RegAddress_Country = Column(String)
    RegAddress_PostCode = Column(String)
    SICCode_SicText_1 = Column(String)

    def __init__(
                    CompanyName,
                    CompanyNumber,
                    RegAddress_CareOf,
                    RegAddress_POBox,
                    RegAddress_AddressLine1,
                    RegAddress_AddressLine2,
                    RegAddress_PostTown,
                    RegAddress_County,
                    RegAddress_Country,
                    RegAddress_PostCode,
                    SICCode_SicText_1,
    ):

        self.CompanyName = CompanyName
        seld.CompanyNumber = CompanyNumber
        self.RegAddress_CareOf = RegAddress_CareOf
        self.RegAddress_POBox = RegAddress_POBox
        self.RegAddress_AddressLine1 = RegAddress_AddressLine1
        self.RegAddress_AddressLine2 = RegAddress_AddressLine2
        self.RegAddress_PostTown = RegAddress_PostTown
        self.RegAddress_County = RegAddress_County
        self.RegAddress_County = RegAddress_County
        self.RegAddress_PostCode = RegAddress_PostCode
        self.SICCode_SicText_1 = CompanyCategory

Base.metadata.create_all(engine)
