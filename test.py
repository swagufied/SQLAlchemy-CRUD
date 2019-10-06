
# from tests import session, Base
from CRUD.Table import Table
from tests.tables import User, Comment
from tests.utils import block_msg
# from tests.crud_tests import CreateTest
# https://docs.sqlalchemy.org/en/13/_modules/examples/adjacency_list/adjacency_list.html
from tests.test_relationship_detect import *

from sqlize.sqlize_filter import sqlize_filter
if __name__ == '__main__':
	unittest.main()


# print(Base.metadata.tables, type(Base.metadata.tables['user_role']))
"""
SQLAlchemyCRUD init scrabbook
"""
# from CRUD import SQLAlchemyCRUD
#
#
# sacrud = SQLAlchemyCRUD(Base, session)
#
#
#
#
#
# block_msg("test code")
#
#
# data = [
# 	{
# 		'username':'swagu',
# 		'comments':[
# 			{'text':'hello'}
# 		]
# 	},{
# 		'username':'shiina',
# 		'comments':[{
# 			'text': 'shiina text'
# 		}]
# 	}]

# user = None
# for d in data:
# 	user = sacrud.User.create(d)
# 	print(user)
#
# sacrud.User.update(user.id, {'username':'shiina2'})

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
# print(session.query(Comment).all())
