import operator

"""
UNIVERSAL CRUD ERROR EXCEPTION
"""
class CRUDError(Exception):
	def __init__(self, error):
		self._error = error

	@property
	def messages(self):
		err_msg = None
		if isinstance(self.error, list):
			err_msg = {}
			for error in self.error:
				err_msg.update(error.messages)
		else:
			err_msg = self._error.messages
		# if not isinstance(err_msg, list):
		# 	err_msg = [err_msg]
		return {'errors':err_msg}

	@property
	def error(self):
		return self._error
	

	def add_error(self, error):
		if isinstance(error, list):
			self._errors.extend(error)
		else:
			self._errors.append(error)

"""
BASE ERROR
"""
class BaseCRUDError(Exception):
	_default_col = "Unspecified Column"
	_default_msg = "Something went wrong..."

	def __init__(self, key="", msg="", **kwargs):

		self._key = key or self._default_col
		self._msg = msg or self._default_msg

		for k,v in kwargs.items():
			if not k in ['key', 'msg']:
				self.k = v

	@property
	def messages(self):
		key = self._key
		return {key:[self._msg]}

	def __repr__(self):
		return "{} - {} : {}".format(self._errorname, self._key, self._msg)

"""
SPECIFIC ERRORS
"""
class MissingError(BaseCRUDError):
	_errorname = 'MissingError'
	_default_msg = "No row with specified filter or primary key was found."
	def __init__(self, tablename="",msg="", **kwargs):
		if not msg:
			if tablename:
				msg = "{} has no row with specified filter or primary key.".format(tablename)
			else:
				msg = self._default_msg

		super().__init__(msg=msg, key="missing", **kwargs)

class ImmutableError(BaseCRUDError):
	_errorname = 'ImmutableError'
	_default_msg = "You are trying to change and immutable column."
	_default_colname = "unknown_column"

	def __init__(self, colname, print_columns={}, msg=""):
		colname = colname or self._default_colname

		print_colname = print_columns.get(colname) or colname.capitalize()
		msg = msg or "Field {} cannot be changed.".format(print_colname)

		super().__init__(key=colname, msg=msg)

	
class OverwriteError(BaseCRUDError):
	_errorname = 'OverwriteError'

	operator = {
		'gt': 'greater than',
		'eq': 'equal to'
	}

	# indata are the values that were put in, out_data are the rows that conflicted
	def __init__(self, conflict_check={}, out_data=None, in_data=None, print_columns={}, **kwargs):

		assert(in_data and out_data), 'in_data and out_data must both be specified for OverwriteErrors'
		self._in_data = in_data
		self._out_data = out_data
		self._conflict_check = conflict_check
		self._print_columns = print_columns
		self._violators = self.find_violators(conflict_check, in_data, out_data)



	@property
	def messages(self):
		messages = {}
		for violator in self._violators:

			raw_colname = violator['colname']
			colname = self._print_columns.get(raw_colname) or raw_colname.capitalize()
			op = self.operator[ violator['operator'] ]
			value = violator['out_value']

			if not colname in messages:
				messages[raw_colname] = []

			if violator['operator'] == 'eq':
				messages[raw_colname].append("{} {} already exists.".format(colname, value))
			else:
				messages[raw_colname].append("{} must be {} {}".format(colname, op, value))

		return messages


	def find_violators(self, sqlfilter, in_data, out_data, grouping=None):
		violators=[]

		if isinstance(sqlfilter, list):
			for r in sqlfilter:
				violators.extend(self.find_violators(r, in_data, out_data))
		elif isinstance(sqlfilter, dict):
			for k,v in sqlfilter.items():
				if k in ['or', 'and']:
					violators.extend(self.find_violators(sqlfilter[k], in_data, out_data, grouping=k))
				else:
					violator = []
					for k,v in sqlfilter.items():
						if isinstance(v,list):
							if in_data and v[0] in in_data and getattr(operator, k)(v[1], getattr(out_data, v[0])):
								violator.append({
										'colname': v[0],
										'in_value': in_data[v[0]],
										'out_value': v[1],
										'operator': k,
									})
						else:
							if v in in_data and v in out_data and getattr(operator, k)(out_data[v], in_data[v]):
								violator.append({
										'colname': v,
										'in_value': in_data[v],
										'out_value': out_data[v],
										'operator': k
									})
						# if grouping == 'and':
						# 	violators.append(violator)
						# else:
						violators.extend(violator)


		return violators


	@property
	def in_data(self):
		return self._in_data

	@property
	def out_data(self):
		return self._out_data

valid_crud_errors = (
	CRUDError,
	BaseCRUDError,
	MissingError,
	ImmutableError,
	OverwriteError)