import re
import operator
import sqlalchemy
import sys




"""
operator.lt(a, b)
operator.le(a, b)
operator.eq(a, b)
operator.ne(a, b)
operator.ge(a, b)
operator.gt(a, b)

like
in
and
or

"""

def generate_statement(operator_value, col_name, col_values):
			statement = ()
			if isinstance(col_values, list):
				for col_value in col_values:
					print(col_value)
					statement += (getattr(operator, operator_value)(col_name, col_value),)
			else:
				statement = (getattr(operator, operator_value)(col_name, col_values),)
			print(statement)
			return statement

def sqlize_filter(table, filter_dict, **values):
		"""
		returns sql filter expression
		table - table on which expression is to be generated. must be sqlalchemy Base object
		filter_dict: and,or must be list of single key dicts. key is operator and value is column name
		values: kwargs of values where key is column name and value is the value to be used in the operator. alternative is to provide values in list for as the value in filter_dict. The first index will be the column name and the second index will be the value
		EX:
		input: {'and': [
					{'eq':'mal_id'},
					{'or':[
						{'gt': 'mal_id'},
						{'eq': 'add_date'}
					]},
					{'eq': ['modify_date', False]}
					]
				}
		output:
		print(*input)
		"MalEntry".mal_id = :mal_id_1 AND ("MalEntry".mal_id > :mal_id_2 OR "MalEntry".add_date = :add_date_1) AND "MalEntry".modify_date = false		

		supports all inequality operators (ie. gt, ge, lt, ne, etc.), and, or, and like.
		
		for statements such as "in" you can use the eq key. ex. {"eq": ['name', ['Joe', 'Bob']]}

		"""





		statement = ()
		for k in filter_dict:
			if k in ['and', 'or']:
				ops = () # initialize list of operators
				for v in filter_dict[k]: # list of single dicts [{operator:col_name}, {operator:col_name}]
					if isinstance(v, dict) and len(v.keys()) == 1:
						ops += (sqlize_filter(table, v, **values),)
					else:
						print('invalid list value in sqlize_filter: {}'.format(v))
						sys.exit()
				statement += (getattr(sqlalchemy, '{}_'.format(k))(*ops), )
			else:

				a,b = None, None

				# filters for relationships
				# if '.' in filter_dict[k][0]:
				# 	col_name_split = filter_dict[k][0].split('.')

				# 	getattr(table, '.'.join(col_name_split[:-1])).getattr(sqlalchemy, 'has')(getattr(operator, k)(col_name_split[-1],[filter_dict[k][0]]))

				if k == 'like':

					terms = filter_dict[k][1] if isinstance(filter_dict[k][1], list) else [filter_dict[k][1]]

					if not isinstance(filter_dict[k], list):
						raise Exception("the \"like\" statement value must be a list. list[0] = column name, list[1] = value(s)")

					

					for term in terms:
						statement += (table.filter_dict[k][0].ilike('%{}%'.format(term)), )
					continue

				elif isinstance(filter_dict[k], list): # {operator: [col_name, value]}


					if filter_dict[k][0] in table.__table__.columns: # should be value
						a = getattr(table, filter_dict[k][0])
						b = filter_dict[k][1]


					else:
						raise Exception('Column "{}" doesnt exist in table "{}"'.format(filter_dict[k][0], table.__tablename__))

				# elif isinstance(filter_dict[k], str): # {operator: col_name}
				# 	if filter_dict[k] in table.__table__.columns: # should be value
				# 		a = getattr(table, filter_dict[k])
				# 		b = values[filter_dict[k]]
				# 	else:
				# 		raise Exception('Column "{}" doesnt exist in table "{}"'.format(filter_dict[k], table.__tablename__))
				else:
					print('Invalid value for operator: {}'.format(filter_dict[k]))
					sys.exit()

				print(a, b)
				statement += generate_statement(k, a, b)
		return statement