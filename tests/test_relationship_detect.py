import unittest
from ddt import ddt, data, unpack
from .tables import *
from CRUD.pre_processing import get_relationship_schema
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
		self.base.metadata.drop_all(self.engine)

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
