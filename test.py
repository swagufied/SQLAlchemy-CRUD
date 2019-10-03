from sqlalchemy import Column

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import joinedload_all
from sqlalchemy.orm import relationship

from sqlalchemy.orm.collections import attribute_mapped_collection


from tests import session, Base
from CRUD.Table import Table
from tests.tables import User, Comment
from tests.utils import block_msg
# from tests.crud_tests import CreateTest
# https://docs.sqlalchemy.org/en/13/_modules/examples/adjacency_list/adjacency_list.html


# print(dir(Base._decl_class_registry.values()))
# print(Base._decl_class_registry.values())
# for f in Base._decl_class_registry.values():
# 	print(f, type(f))

# print(Base.metadata.tables, type(Base.metadata.tables['user_role']))
"""
SQLAlchemyCRUD init scrabbook
"""
from CRUD import SQLAlchemyCRUD


sacrud = SQLAlchemyCRUD(Base, session)


# print(dir(session))


# block_msg("Base:")
# print(Base)
# print(Base._decl_class_registry)
# print(dir(Base))
# print(Base.metadata)
# print(dir(Base.metadata))
# print(Base.metadata.tables)
#
# tables = Base.metadata.tables
#
# for s in tables:
# 	print(tables[s])
# 	print(dir(tables[s]))
# 	print(type(tables[s]))
	# print(dir(s))


from sqlize.sqlize_filter import sqlize_filter




# block_msg("test code")
#
#
# data = [
# 	{
# 		'username':'swagu'
# 	},{
# 		'username':'shiina'
# 	}]
#
# for d in data:
# 	Table(session, User, relationship_schema={'comments':'o2m'}).create(d)

# block_msg("data input")
#
# query = {
# 	'or': [
# 		{'eq': ['username', ['swagu', 'shiina']]}
# 	]
# }
#
# query = sqlize_filter(User, query)
# results = Table(session, User)._query_bread(session, User, query)
# print('results', results)
#
#
# comment={'text':'hello'}
# # Table(session, Comment).create(comment)
#
# print(session.query(User).all())
# print(session.query(Comment).all())
