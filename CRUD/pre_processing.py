import sqlalchemy
import itertools
from .utils import get_columns_from_decl_meta



def get_target_table_relationship_with_backref(decl_meta_table, target_table_name, relationship_name):

	for relationship in sqlalchemy.inspect(decl_meta_table).relationships:
		if str(relationship.target) == target_table_name and (relationship.backref == relationship_name or relationship.back_populates == relationship_name):
			return relationship

	return None

# returns a dict of each table that is represented in the input, decl_meta_table. key is the tablename, value is a list of dicts of relevant information about the foreign keys
def get_foreign_key_table_map(decl_meta_table):
	columns = get_columns_from_decl_meta(decl_meta_table)
	fk_table_map = {}
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
				if target_table_name in fk_table_map:
					fk_table_map[target_table_name].append({
						'column_name': column.name
					})
				else:
					fk_table_map[target_table_name] = [{
						'column_name': column.name
					}]
	return fk_table_map


# table must be of type  <class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'>
"""
first, the foreign keys in the table are compiled.

The relationship are iterated through to then find information about them.
"""

def get_relationship_data(table, decl_class_tables):

	print('DETECTING RELATIONSHIP DATA')
	print('table: %s' % table)


	relationship_data = []
	fk_table_map = get_foreign_key_table_map(table)


	print(fk_table_map)

	# relationship is of type <class 'sqlalchemy.orm.relationships.RelationshipProperty'>
	for relationship in sqlalchemy.inspect(table).relationships:

		# if the relationship isnt used to update data, skip it
		if relationship.viewonly:
			continue

		print('INSPECTING RELATIONSHIP: %s' % relationship)


		relationship_table = str(relationship).split('.')[0]
		relationship_name = str(relationship).split('.')[1]
		target_tablename = relationship.target.name # target table of the relationship

		print('target_tablename', target_tablename)

		# these variables will be used to determine the type of relationship
		table_uselist = False
		target_uselist = False
		fk_in_table = False
		fk_in_target = False

		# check if the relationship has a foreign key restraint and if it has uselist=True for the relationship
		if target_tablename in fk_table_map:
			fk_in_table = True




			# check if the target has uselist=True
			if target_tablename in decl_class_tables:

				target_relationship = get_target_table_relationship_with_backref(decl_class_tables[target_tablename], relationship_table, relationship_name)
				print('target_relationship', target_relationship)
				if target_relationship:
					print('in target_rel')
					if target_relationship.uselist:
						target_uselist = True

		else: # current table doesnt have foreign key to relationship table.
			target_table = decl_class_tables[target_tablename]
			target_fk_table_map = get_foreign_key_table_map(target_table)

			if table.__tablename__ in target_fk_table_map:
				fk_in_target=True



		# if relationship is using list
		if relationship.uselist:
			table_uselist = True
		# check if the target table of the relationship has a foreign key restraint

		print('table_uselist', table_uselist)
		print('target_uselist',target_uselist)
		print('fk_in_table',fk_in_table)
		print('fk_in_target', fk_in_target)

		relationship_type = ""

		# determine type of relationship
		if fk_in_table and not fk_in_target:

			if target_uselist:
				relationship_type = "m2o"
			else:
				relationship_type = "o2o"

		elif fk_in_target and not fk_in_table:

			if table_uselist:
				relationship_type = "o2m"
			else:
				relationship_type = "o2o"


		elif fk_in_table and fk_in_target: # self-referencing relationship

			if target_uselist:
				relationship_type = "m2o"
			elif table_uselist:
				relationship_type = "o2m"
			else:
				relationship_type = "o2o"

		elif not fk_in_table and not fk_in_target: # m2m or association table relationship
			relationship_type = "m2m"

			#TODO: detect association table


		relationship_data.append({
			'name': relationship_name,
			'type': relationship_type,
			'table': decl_class_tables[target_tablename]
			})


		print()

	return relationship_data
