from sqlalchemy.sql.elements import BooleanClauseList, BinaryExpression

class BaseCRUD:

	"""
	The most basic functions of CRUD.

	values argument shold always be dict.
	session is the sqlalchemy session
	table should be the model
	"""

	list_filters = (BooleanClauseList, tuple) # if filters is beyond simple single operator.eq(...)
	single_filters = (BinaryExpression, )

	def _bcreate(self, session, table, values,  commit=False):

		row = table(**values)
		session.add(row)
		
		if commit:
			self._flush(session)
		else:
			self._commit(session)

		return row

	def _bread(self, session, table, row_id):
		return session.query(table).get(row_id)

	def _query_bread(self, session, table, arg, query_limit = 1):
		"""
		This is only meant for internal query use.
		arg can be ID or sqlalchemy filter
		"""
		return_data = []

		if not arg:
			pass
		elif isinstance(arg, self.list_filters):

			# print('READ: {}'.format(*arg))
			if not query_limit:
				return_data = session.query(table).filter(*arg).all()
			else:
				return_data = session.query(table).filter(*arg).limit(query_limit).all()

		elif isinstance(arg, self.single_filters):

			# print('READ: {}'.format(arg))
			if not query_limit:
				return_data = session.query(table).filter(arg).all()
			else:
				return_data = session.query(table).filter(arg).limit(query_limit).all()

		else:
			return_data = [self._bread(session, table, arg)]

		return [row for row in return_data if row]

	def _bupdate(self, session, table, row_id, values, commit=False):

		self._bread(session, table, row_id)
		for key in values:
			setattr(row, key, values[key])

		if commit:
			self._flush(session)
		else:
			self._commit(session)
		return row

	def _bdelete(self, session, table, row_id, commit=True):
		self._bread(session, table, row_id)
		session.delete(row)

		if commit:
			self._flush(session)
		else:
			self._commit(session)
		return row


	def _commit(self, session):
		try:
			session.commit()
		except Exception as e:
			self._rollback(session)
			raise e

	def _flush(self, session):
		try:
			session.flush()
		except Exception as e:
			self._rollback(session)
			raise e

	def _rollback(self, session):
		session.rollback()


