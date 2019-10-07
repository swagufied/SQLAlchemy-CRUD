from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
utilsBase = declarative_base()

"""
when just doing scripting testing
"""
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# from .utils import block_msg
# import sqlalchemy
# engine = create_engine("sqlite://", echo=False)
# block_msg("Creating Tables:")
#
# from .tables import *
#
# Base.metadata.create_all(engine)
# session = Session(engine)
