#!/usr/bin/env python3

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

script_path = os.path.dirname(os.path.realpath(__file__))

engine = create_engine(
                        f'sqlite:///{script_path}/database/companies_house.sqlite',
                        convert_unicode=True
)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
