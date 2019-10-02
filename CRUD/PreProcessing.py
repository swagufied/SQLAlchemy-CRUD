import sqlalchemy
import itertools

def get_column_names(table):

	if isinstance(table, sqlalchemy.ext.declarative.api.DeclarativeMeta):
		return [col.name for col in table.__table__.columns]

	elif hasattr(table, 'columns'):
		return [col.name for col in table.columns]

	return []
	

def get_relationship_names(table):

	print(type(table), dir(table))

	return [str(r).split('.')[1] for r in sqlalchemy.inspect(table).relationships]

def get_relationship_target_table(table, relationship_name):
	print('table type', type(getattr(table, relationship_name).parent))
	print('dir', dir(getattr(table, relationship_name).parent))
	return getattr(table, relationship_name).parent

def get_relationship_data(table):


	# table info
	# relationship type
	# table of target
	# primary key of target

	
	relationship_data = []
	for r in sqlalchemy.inspect(table).relationships:

		# make sure relationship we look at is from the current table


		rstring = str(r).split('.')[1]
		relationship = getattr(table, rstring)
		
		# print('col.parent', type(col.parent), dir(col.parent))
		# print(col.parent.relationships)

		# check the backreference of the relationship and use it to determine relationship type
		backref_in_current = False
		backref_in_target = False
		if r.backref:
			backref_in_current = True
			print('relationships', relationship.parent)
			for q in relationship.parent.relationships:
				if str(q).split('.')[1] == r.backref:

					backref_in_target = True
					# if q.uselist and r.uselist:
					# 	relationship_type = 'm2m'
					# elif q.uselist and not r.uselist:
					# 	relationship_type = 'o2m'
					# elif not q.uselist and r.userlist:
					# 	relationship_type = 'm2o'
					# elif not q.uselist and not r.userlist:
					# 	relationship_type = 'o2o'

					break
					# if r.uselist == False and r.parent

		# check to see which foreign key
		

		# check backref and uselist first
		# check foreign keys


		# relationship_data.append({
		# 	'type':
		# 	'table': relationship.parent
		# 	'pk': relationship.primary_key
		# })


		# print(r, dir(r))
		# print(r.parent, dir(r.parent))
		# print(r.target.corresponding_column, dir(r.target.corresponding_column))
		# print(r.corresponding_column)
		# print(r.target.columns, type(r.target),dir(r.target))
		# print(r.target.metadata.tables, type(r.target.metadata), dir(r.target.metadata))

		# for t in r.target.metadata.tables:
		# 	print('table', t, type(t))
		# print(r.table, type(r.table), dir(r.table))
		# one to many


	return

def get_primary_key(table):
	pk = [pk.name for pk in table.__table__.primary_key] or None
	if pk:
		pk = pk[0]
	return pk

def get_table_constraints(table):
	return [pk for pk in table.__table__.constraints]

def get_table(self, table, db=None):
		if hasattr(self, '_db'):
			if isinstance(table, str):
				table = [cls for cls in self._db.Model._decl_class_registry.values()
				if isinstance(cls, type) and issubclass(cls, self._db.Model) and cls.__tablename__ == table][0]
		else:
			if isinstance(table, str):
				table = [cls for cls in db.Model._decl_class_registry.values()
				if isinstance(cls, type) and issubclass(cls, db.Model) and cls.__tablename__ == table][0]

		return table


class PreProcessing:

	def preprocess( table, values, table_schema=None, constraints=None, default_constraints=True, load='load', relationship_schema=None):
		"""
		This function is called as a quality check for the values that will be put into the database.
		- schema can reformat/clearn values according to the user's choosing
		- ensure values are present within the table
		- ensure values do not conflict with any db constraints
		"""

		# use schema or sa table to verify values are valid columns or relationships
		columns, relationships = {}, {}
		if table_schema:
			values = getattr(table_schema, load)(values)
		columns, relationships = PreProcessing.filter_values(table,values, relationship_schema=relationship_schema)


		# run checks on constraints
		if constraints:
			if default_constraints:
				PreProcessing.create_constraint_filter(table)
			else:
				PreProcessing.process_constraints(constraints)


		# statement = constraints
		# if default_constraints:
		# 	statement = get_default_constraints_statement(table, validated_values)
		# elif constraints:
		# 	if isinstance(constraints, dict):
		# 		statement = PreProcessing.sqlize_filter(table, constraints, values)
		# 	elif  isinstance(constraints, self.list_filters + self.single_filters) or\
		# 	(isinstance(constraints, tuple) and isinstance(*constraints, self.list_filters + self.single_filters)):
		# 		pass
		# 	else:
		# 		raise Exception('invalid input for kwarg constraints')
		

		# return_data = table.query.filter(*statement).limit(query_limit).all()



		return columns, relationships

	def filter_values(table, values, relationship_schema=None):

		columns = {}
		for column_name in get_column_names(table):
			if column_name in values:
				columns[column_name] = values[column_name]


		relationships = {}
		# if not relationship_schema:
		# 	relationship_schema = get_relationship_data(table)

		for relationship in relationship_schema:
			if relationship in values:
				relationships[relationship] = {
						"value": values[relationship],
						"table": get_relationship_target_table(table, relationship),
						"type": relationship_schema[relationship],
						"pk": get_primary_key(table)
					}

		return columns, relationships

	# run a check on constraints
	def process_constraints(constraints):
		pass


	def get_default_constraints_statement(table, values):

		table_constraints = get_table_constraints(table)
		statement = {'or':[]}

		for constraint,info in table_constraints.items():
			if constraint == 'unique':
				statement['or'].append({
						'eq': [info[0], values[info[0]]]
					})
			elif constraint == 'check':
				pass


		return

	# def get_table_constraints(table):

	# 	"""
	# 	returns the construants (e.g. unique, check, primary_key)
		
	# 	{
	# 		'unique': ['username'],
	# 		'check': ''
	# 	}

	# 	"""

	# 	# primary key
	# 	primary_keys = get_primary_keys(table)

	# 	# unique constraint
	# 	# print(table.__table__.constraints)
	# 	# print(dir(table.__table__.constraints))
	# 	# print(dir(table.__table__.constraints.__class__))
	# 	constraints = get_table_constraints(table)


	# 	print(sqlalchemy.inspect(table))
	# 	print(dir(sqlalchemy.inspect(table)))

	# 	print(constraints)
	# 	for c in constraints:
	# 		print(c, c.dialect_kwargs, c.kwargs)
	# 		print(dir(c))
	# 		print('kwargs', type(c.kwargs), c.kwargs._key(), dir(c.kwargs))
	# 		print(c.dialect_kwargs.values)
	# 		for k in c.dialect_kwargs.values:
	# 			print('ss',k)
	# 	# print(dir(table.__table__))


		# return {}
