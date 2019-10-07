import unittest
from ddt import ddt, data, unpack
from .tables import *
from CRUD.pre_processing import *
from deepdiff import DeepDiff
from CRUD.utils import get_decl_meta_tables_from_base
from tests import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

@ddt
class DetectRelationshipTest(unittest.TestCase):


	def setUp(self):
		self.base = Base
		self.engine = create_engine("sqlite://", echo=False)
		self.connection = self.engine.connect()
		self.base.metadata.create_all(self.engine)
		self.session = Session(self.engine)

	def tearDown(self):
		self.base.metadata.drop_all(bind=self.engine)

	# o2m -
	@data(
	(User, {
		'comments':{
			'table': Comment,
			'pk': ['id'],
			'type': 'o2m'
		},
		'nicknames':{
			'table': NickName,
			'pk': ['id'],
			'type': 'o2m'
		},
		'roles':{
			'table': Role,
			'pk': ['id'],
			'type': 'm2m'
		},
		'details':{
			'table': UserDetails,
			'pk': ['id'],
			'type': 'o2o'
		},
		'sensitive_info':{
			'table': UserSensitiveInfo,
			'pk': ['id'],
			'type': 'o2o'
		}
	}),
	(NickName, {
		'user': {
			'table': User,
			'pk': ['id'],
			'type': 'm2o'
		}
	}),
	(UserDetails, {
		'user': {
			'table': User,
			'pk': ['id'],
			'type': 'o2o'
		}
	}),
	(UserSensitiveInfo, {
		'user': {
			'table': User,
			'pk': ['id'],
			'type': 'o2o'
		}
	}),
	(Role, {
		'users': {
			'table': User,
			'pk': ['id'],
			'type': 'm2m'
		}
	}),
	(Comment, {
		'user': {
			'table': User,
			'pk': ['id'],
			'type': 'm2o'
		}
	})
	)
	def test_get_relationship_schema(self, values):
		tables = get_decl_meta_tables_from_base(self.base)
		output = get_relationship_schema(values[0], tables)

		ddiff = DeepDiff(output, values[1], ignore_order=True, report_repetition=True)

		assert not ddiff

	@data(
	(User, {}),
	(NickName, {
		'User': [{'column_name': 'user_id'}]
	}),
	# (, { # in self referencing table
	#
	# })
	)
	def test_get_foreign_key_table_map(self, values):
		output = get_foreign_key_table_map(values[0])
		print(output)
		ddiff = DeepDiff(output, values[1], ignore_order=True, report_repetition=True)
		assert not ddiff


	@data(
	((User, "Comment", "user"), "User.comments"), #o2m
	((UserDetails, "User", "details"), "UserDetails.user"), #o2o
	((Role, "User", "roles"), "Role.users"), #m2m
	((User, "NickName", "user"), "User.nicknames") #m2o
	)
	def test_get_target_table_relationship_with_backref(self, values):
		output = get_target_table_relationship_with_backref(*values[0])
		assert str(output) == values[1]
