import unittest
from ddt import ddt, data, unpack
from CRUD.pre_processing import get_relationship_schema
from deepdiff import DeepDiff
from CRUD.utils import *
from tests import utilsBase
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


from .test_utils_tables import *


@ddt
class UtilsTest(unittest.TestCase):


	def setUp(self):
		self.base = utilsBase
		self.engine = create_engine("sqlite://", echo=False)
		self.connection = self.engine.connect()
		self.base.metadata.create_all(self.engine)
		self.session = Session(self.engine)

	def tearDown(self):
		self.base.metadata.drop_all(self.engine)

	@data(
	(Base, {
		'DifferentName': Table1,
		'Table2': Table2
	})
	)
	def test_get_decl_meta_tables_from_base(self, values):
		output = get_decl_meta_tables_from_base(values[0])
		ddiff = DeepDiff(output, values[1], ignore_order=True, report_repetition=True)
		assert not ddiff

	@data(
	(Table1, ['pk1', 'pk2']),
	(Table2, ['id'])
	)
	def test_get_primary_keys_from_decl_meta(self, values):
		output = get_primary_keys_from_decl_meta(values[0])
		ddiff = DeepDiff(output, values[1], ignore_order=True, report_repetition=True)
		assert not ddiff

	@data(
	(Table1, {
		'__primary_key': ['pk1', 'pk2'],
		'pk1': Table1.pk1,
		'pk2': Table1.pk2,
		'string': Table1.string

	}),
	(Table2, {
		'__primary_key': ['id'],
		'id': Table2.id,
		't1_pk1': Table2.t1_pk1,
		't1_pk2': Table2.t1_pk2
	})
	)
	def test_get_column_schema(self, values):
		output = get_column_schema(values[0])
		assert len(output.keys()) == len(values[1].keys())

		for key in output:
			assert key in values[1]

			if key == '__primary_key':
				assert not DeepDiff(output[key], values[1][key], ignore_order=True, report_repetition=True)


		# ddiff = DeepDiff(output, values[1], ignore_order=True, report_repetition=True)
		# assert not ddiff
	@data(
	(Table1, "DifferentName"),
	(Table2, "Table2")
	)
	def test_get_tablename_from_decl_meta(self, values):
		output = get_tablename_from_decl_meta(values[0])
		assert output == values[1]

	# Should be tested with get_foreign_key_table_map() in test_relationship_detect.py
	# def test_get_columns_from_decl_meta(self, values):
	# 	pass
