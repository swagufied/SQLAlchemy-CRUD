import sqlalchemy
import itertools
from .utils import get_columns_from_decl_meta



def get_target_table_relationship_with_backref(decl_meta_table, relationship_name):

	for relationship in sqlalchemy.inspect(decl_meta_table).relationships:
		if relationship.backref == relationship_name or relationship.back_populates == relationship_name:
			return relationship

	return None

def get_foreign_key_table_map(decl_meta_table):
	columns = get_columns_from_decl_meta(decl_meta_table)
	foreign_key_tables = {}
	for column in columns:
		# get all columns that are foreign keys
		if column.foreign_keys:
			for fk in column.foreign_keys:

				target_table_name = fk.target_fullname.split('.')[0]

				# print(dir(fk), fk.target_fullname)
				# print('name', fk.name)
				# print('fk.column', fk.column)
				# print('link_to_name', fk.link_to_name)
				# print('references', fk.references)
				# print('info', fk.info)
				# print('kwargs', fk.kwargs)
				if target_table_name in foreign_key_tables:
					foreign_key_tables[target_table_name].append({
						'column_name': column.name
					})
				else:
					foreign_key_tables[target_table_name] = [{
						'column_name': column.name
					}]
	return foreign_key_tables


# table must be of type  <class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'>
"""
first, the foreign keys in the table are compiled.

The relationship are iterated through to then find information about them.
"""

def get_relationship_data(table, decl_class_tables):

	print('DETECTING RELATIONSHIP DATA')
	print('table: %s' % table)
	# print('table type: %s' % type(table))
	# print(dir(table))
	# print()
	relationship_data = []

	# for s in dir(table.__table__):
	# 	print(s, type(s))

	foreign_key_tables = get_foreign_key_table_map(table)


	print(foreign_key_tables)

	# relationship is of type <class 'sqlalchemy.orm.relationships.RelationshipProperty'>
	for relationship in sqlalchemy.inspect(table).relationships:

		# if the relationship isnt used to update data, skip it
		if relationship.viewonly:
			continue

		print('INSPECTING RELATIONSHIP: %s' % relationship)
		# print('r type: %s' % type(r))
		# print('r table: %s' % r.table)
		# print('r table type: %s' % type(r.table))
		# print(dir(r.table))
		# print(dir(relationship))
		# print(dir(relationship.target))
		# print(relationship.target.fullname)
		# print('parent', relationship.parent, dir(relationship.parent))
		relationship_name = str(relationship).split('.')[1]
		# print(relationship_name)
		# type <class 'sqlalchemy.orm.attributes.InstrumentedAttribute'>
		# relationship_ia = getattr(table, relationship_name)
		# print('relationship_ia dir', dir(relationship_ia))

		relationship_target_name = relationship.target.name

		table_uselist = False
		target_uselist = False
		fk_in_table = False
		fk_in_target = False

		# check if the relationship has a foreign key restraint and if it has uselist=True for the relationship
		if relationship_target_name in foreign_key_tables:
			fk_in_table = True
			print(relationship_target_name)



			# check if the target has uselist=True
			if relationship_target_name in decl_class_tables:

				target_relationship = get_target_table_relationship_with_backref(decl_class_tables[relationship_target_name], relationship_name)

				if target_relationship:
					if target_relationship.uselist:
						target_uselist = True

		else: # current table doesnt have foreign key to relationship table.
			target_table = decl_class_tables[relationship_target_name]
			target_fk_table_map = get_foreign_key_table_map(target_table)

			if table.__tablename__ in target_fk_table_map:
				fk_in_target=True



		# if relationship is using list
		if relationship.uselist:
			table_uselist = True
		# check if the target table of the relationship has a foreign key restraint



		relationship_type = ""

		# determine type of relationship
		if fk_in_table and not fk_in_target:

			if target_uselist:
				relationship_type = "m2o"
			else:
				relationship_type = "o2o"

		elif fk_in_target and not fk_in_table:
			relationship_type = "o2m"

		elif fk_in_table and fk_in_target: # self-referencing relationship

			if target_uselist:
				relationship_type = "m2o"
			else:
				relationship_type = "o2o"

		elif not fk_in_table and not fk_in_target: # m2m or association table relationship
			relationship_type = "m2m"


		relationship_data.append({
			'name': relationship_name,
			'type': relationship_type,
			'table': decl_class_tables[relationship_target_name]
			})


		print()

	return relationship_data
