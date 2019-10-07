from tests import utilsBase as Base
from datetime import datetime
from sqlalchemy import Table, ForeignKey
from sqlalchemy import Integer, Column, DateTime, Boolean
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import joinedload_all
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKeyConstraint

# composite key

class Table1(Base):
    __tablename__ = "DifferentName"

    pk1 = Column(Integer, primary_key=True)
    pk2 = Column(String(20), primary_key=True)
    string = Column(String(20))



class Table2(Base):
    __tablename__ = "Table2"

    id = Column(Integer, primary_key=True)
    t1_pk1 = Column(Integer)
    t1_pk2 = Column(String(20))

    table1 = relationship("Table1", backref="")

    __table_args__ = (ForeignKeyConstraint([t1_pk1, t1_pk2],
                                           [Table1.pk1, Table1.pk2]),
                      {})
