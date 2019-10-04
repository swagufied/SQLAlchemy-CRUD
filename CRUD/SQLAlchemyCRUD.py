# from sqlalchemy import MetaData, create_engine, Table
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# from .constants import SKELETON_URL
#
#
from .Table import Table
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from .utils import get_decl_meta_tables_from_base, get_tablename_from_decl_meta

class SQLAlchemyCRUD(object):

    def __init__(self, base, session):
        self.base = base
        self.session = session


        self.decl_meta_tables = get_decl_meta_tables_from_base(base)
        print(self.decl_meta_tables)

        for table in base._decl_class_registry.values():
            if isinstance(table, DeclarativeMeta):

                tablename = get_tablename_from_decl_meta(table)

                print()
                print('INITIALIZING TABLE: %s' % table.__tablename__)
                print()

                sacrud_table = Table(session, table, decl_meta_tables=self.decl_meta_tables)
                setattr(self, tablename, sacrud_table)
