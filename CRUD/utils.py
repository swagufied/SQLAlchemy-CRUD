from sqlalchemy.ext.declarative.api import DeclarativeMeta


# table must be of type  <class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'>
def get_decl_meta_tables_from_base(base):

	decl_class_tables = {}

	for table in base._decl_class_registry.values():
		if isinstance(table, DeclarativeMeta):
			decl_class_tables[table.__tablename__] = table

	return decl_class_tables

def get_primary_keys_from_decl_meta(table):
	primary_keys = []

	for column in table.__table__.columns:
		if column.primary_key:
			primary_keys.append(column.name)

	return primary_keys

def get_columns_from_decl_meta(table):
	return [col for col in table.__table__.columns]

def get_column_schema(table):
	column_schema = {}
	pk = []
	for col in table.__table__.columns:

		if col.primary_key:
			pk.append(col.name)

		column_schema[col.name] = col

	column_schema["__primary_key"] = pk

	return column_schema

def get_column_names_from_decl_meta(table):
	return [col.name for col in table.__table__.columns]

def get_tablename_from_decl_meta(table):
	return table.__tablename__

def get_tablename_from_relationship(relationship):
	pass

# def get_table(self, table, db=None):
# 		if hasattr(self, '_db'):
# 			if isinstance(table, str):
# 				table = [cls for cls in self._db.Model._decl_class_registry.values()
# 				if isinstance(cls, type) and issubclass(cls, self._db.Model) and cls.__tablename__ == table][0]
# 		else:
# 			if isinstance(table, str):
# 				table = [cls for cls in db.Model._decl_class_registry.values()
# 				if isinstance(cls, type) and issubclass(cls, db.Model) and cls.__tablename__ == table][0]
#
# 		return table
