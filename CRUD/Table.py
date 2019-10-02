from .BaseCRUD import BaseCRUD
from sqlalchemy.sql import schema
from flask_sqlalchemy.model import DefaultMeta
from .ComplexCRUD import ComplexCRUD

"""
session is the session of the db
table must be a db.Model object or string of the objects classname.


tables - must be my defined tables. and relationships must be recorded


relationships = {
	rel_name: rel_type
}

"""


class Table(ComplexCRUD):
	def __init__(self, session, table, table_schema=None, relationship_schema=None):
		self._session = session
		self._table = table

		self.local_params = {}
		self.local_params['table_schema'] = table_schema
		self.local_params['relationship_schema'] = relationship_schema

	"""
	CRUD
	"""
	def create(self, values, **kwargs):
		return self._cupdate(self._session, self._table, None, values, **self.local_params, **kwargs)

	def read(self, row_id, **kwargs):
		return self._cread(self._session, self._table, row_id, **self.local_params, **kwargs)

	def update(self, row_id, values, **kwargs):
		return self._cupdate(self._session, self._table, row_id, values, **self.local_params, **kwargs)

	def delete(self, row_id, **kwargs):
		return self._bdelete(self._session, self._table, row_id, **kwargs)

	"""
	QUERY
	"""

"""
OUTMODED TABLE OBJECT
"""

class tTable(BaseCRUD):

	def __init__(self, session, table, db=None, schema=None):
		self._session = session
		self._db = db
		self._table = self.get_table(table, db=db)
		self._table_columns = self.get_table_columns(self._table)
		
		self._primary_key = self.get_primary_key(self._table)
		self._unique_columns = self.get_unique_columns()
		self._schema = schema
		self._relationships = self.get_relationships(self._table, db=db)

		print('table init. super starting')
		super().__init__()

	# determines type of relationship
	def get_relationships(self, table, db=None):
		out_data = {}
		# print('table dir', dir(table))
		if not isinstance(table, DefaultMeta):
			raise Exception('table of type db.Model must be given as table argument.')
		for r in self._table.__mapper__.relationships:
			rel_type = ''
	
			if r.viewonly:
				continue

			# find out if theres a foreign key in current table or target table
			# if foreign key in either and uselist = false, o2o
			# if foreign key in target, o2m
			# if fk in current table and current table is target table, o2m
			# if fk in current table, m2o
			# if no fk in either table - must be m2m

			# association ????? TODO
			
			# print('r', r)
			# print('target', r.target)
			# print('parent', r.parent)
			# print('backref', r.backref)
			# print('back_populates', r.back_populates)
			# print(dir(r))
			# print(dir(r.table))

			
			# for distinguishing parent in self referencing relationships
			backref_in_current = False
			if r.backref:
				backref_in_current = True


			# determine if the foreign key of the relationship is defined in the current table
			fk_in_current = False
			for col in self.get_table_columns(table):
				if col.foreign_keys:
					for fk in col.foreign_keys:
						split_target_col = fk.target_fullname.split('.')
						table_str = split_target_col[0]
						col_str = split_target_col[1]
						if table_str == str(r.table.fullname) and col_str == self.get_primary_key(table):
							fk_in_current=True
							break
				if fk_in_current:
					break

			# determine if the foreign key of the relationship is defined in the target table	
			fk_in_target = False
			for col in self.get_table_columns(r.table):
				if col.foreign_keys:
					for fk in col.foreign_keys:
						split_target_col = fk.target_fullname.split('.')
						table_str = split_target_col[0]
						col_str = split_target_col[1]
						if table_str == str(r.table.fullname) and col_str == self.get_primary_key(r.table):
							fk_in_target=True
							break
				if fk_in_target:
					break

			# determine if the target tables relationship specifies uselist=false - determines if o2o or o2m
			target_uselist = False
			target_table = self.get_table(str(r.table.fullname),db=db)
			for rel in target_table.__mapper__.relationships:
				if str(rel).split('.')[1] == r.back_populates and rel.uselist:
					target_uselist = True


			# print(r, fk_in_current,fk_in_target)
			# print(target_uselist)
			if (fk_in_current and not fk_in_target or fk_in_target and not fk_in_current) and not r.uselist and not target_uselist:
				rel_type = 'o2o'

			# self-referencing table
			elif fk_in_current and fk_in_target:
				if backref_in_current:
					rel_type = 'm2o'
				else:
					rel_type = 'o2m'
			elif not fk_in_current and fk_in_target:
				rel_type = 'o2m'
			elif fk_in_current and not fk_in_target:
				rel_type = 'm2o'
			elif not fk_in_target and not fk_in_target:
				rel_type = 'm2m'

		
				# # association - no foreign key in either
				# if r.table not in [r.back_populates]
			relationship_name = (str(r)).split('.')[1]
			out_data[relationship_name] = {
				'table': str(r.table.fullname),
				'rel_type': rel_type
			}
		
		# print(out_data)
		return out_data



	# returns a list of the table's column names
	def get_table_columns(self, table):

		if isinstance(table, schema.Table):
			return table.columns
		elif isinstance(table, DefaultMeta):
			return table.__table__.columns
		else:
			raise Exception('Invalid table input into get_table_columns')


	# takes a string rep or sqlalchemy table and returns a sqlalchemy table
	def get_table(self, table, db=None):
		out_table = None

		if isinstance(table, str):

			if not db:
				raise Exception('If a string is given as the "table" argument, you must provide an input for db')

			for cls in db.Model._decl_class_registry.values():
				if isinstance(cls, type) and issubclass(cls, db.Model) and cls.__tablename__ == table:
					out_table = cls
					break

			return out_table
		elif isinstance(table, DefaultMeta):
			return table
		# elif isinstance(table, schema.Table):
		# 	return table
		else:
			raise Exception('Invalid table given to Table class')

	def get_primary_key(self, table):

		for column in self.get_table_columns(table):
			if column.primary_key:
				return column.name

	def get_unique_columns(self):
		unique_columns = []
		for column in self._table_columns:
			if column.unique:
				unique_columns.append(column.name)
		return unique_columns

	# takes in dict and returns dict keys that match the table's column names 
	def filter_column_values(self, edit_primary=False, include_relationships=True, **kwargs):
		#pulls all valid values after ensuring - cannot edit primary key
		values={}
		for col in self._table_columns:
			if col.name in kwargs and (not col.primary_key or edit_primary):
				values[col.name] = kwargs[col.name]
		return values