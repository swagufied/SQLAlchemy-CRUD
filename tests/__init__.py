from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .utils import block_msg
import sqlalchemy
Base = declarative_base()
#
#
engine = create_engine("sqlite://", echo=False)
block_msg("Creating Tables:")

from .tables import *
# print((User.__table__.columns))
# print(dir(User.__table__))
# print(dir(User.__mapper__.relationships))
# for r in User.__mapper__.relationships:
# 	print(r)

# print()
Base.metadata.create_all(engine)

session = Session(engine)

# from CRUD import SQLAlchemyCRUD
#
# db = SQLAlchemyCRUD("sqlite://")
# db.connect()

"""

schema
check conflicts



goal to make user friendly check constraints



for many to many - how to indicate delete
"""
