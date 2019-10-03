# from sqlalchemy import MetaData, create_engine, Table
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# from .constants import SKELETON_URL
#
#
from .Table import Table
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from .utils import get_decl_class_tables_from_base

class SQLAlchemyCRUD(object):
    '''Wrapper to easily start interacting with database using SQLAlchemy'''

    def __init__(self, base, session):
        self.base = base
        self.session = session


        self.decl_class_tables = get_decl_class_tables_from_base(base)
        print(self.decl_class_tables)

        for table in base._decl_class_registry.values():
            if isinstance(table, DeclarativeMeta):

                print()
                print('INITIALIZING TABLE: %s' % table.__tablename__)
                print()
                self.table_name = Table(session, table, decl_class_tables=self.decl_class_tables)
