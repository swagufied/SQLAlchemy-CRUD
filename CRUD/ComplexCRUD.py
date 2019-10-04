from sqlalchemy.sql.elements import BooleanClauseList, BinaryExpression
from .PreProcessing import PreProcessing
from .BaseCRUD import BaseCRUD






class ComplexCRUD(BaseCRUD):

	"""
	Provides more options to basic CRUD.
	"""

	list_filters = (BooleanClauseList, tuple) # if filters is beyond simple single operator.eq(...)
	single_filters = (BinaryExpression, )

	def rollback_handler(wrapped_function):
		# handles automatic rollback of any changes made to db
		# args[0] should be the Table object. args[1] should be the session variable
		def _wrapper(*args, **kwargs):
			try:
				result = wrapped_function(*args, **kwargs)
			except:
				args[0]._rollback(args[1])
				raise
			return result
		return _wrapper

	"""
	for create, just call ComplexCRUD._cupdate with the row_id argument as None
	"""

	def _cread(self, session, table, row_id, format_output=True):

		row = self._bread(session, table, row_id)

		if format_output:
			if schema:
				return schema.dump(row)
			else:
				return PostProcessing.dump(row)
		else:
			return row

	@rollback_handler
	def _cupdate(self, session, table, row_id, values, table_schema=None, commit=True, **kwargs):
		# print('cupdate kwargs', kwargs)
		columns, relationships = PreProcessing.preprocess(table, values, table_schema=table_schema, **kwargs)


		row = None
		if row_id:
			row = self._bupdate(session, table, row_id, columns)
		else:
			row = self._bcreate(session, table, columns)


		# manage relationships
		# print('relationships', relationships)
		for relationship, properties in relationships.items():
			if properties['type'] == 'o2m':
				if isinstance(properties['value'], list):
					for value in properties['value']:
						self._cupdate(session, properties['table'], properties['pk'], value)
				else:
					self._cupdate(session, properties['table'], properties['pk'], properties['value'])

			elif relationship['type'] == 'm2m':
				x=1


		# commit changes
		if commit:
			self._flush(session)
		else:
			self._commit(session)

		return row

	"""
	for delete, just call BaseCRUD._bdelete
	"""


	# takes in dict, returns a filter in format for sqlalchemy to process
	def process_conflict_params(self, constraints, **values):
		tuple_conflict_params = None
		if isinstance(conflict_params, dict):
			if not conflict_params: # if conflict check is empty, use default
				conflict_params = self.build_default_conflict_params(**values)

				if not conflict_params:
					return None, conflict_params
			tuple_conflict_params = SQLHandler.sqlize_filter(self._table, conflict_params, **values)

		else: # if a personalized check is input
			tuple_conflict_params = conflict_params

		return tuple_conflict_params, conflict_params





# phased out
class cComplexCRUD:


	def ccreate(self, format_output=True, **kwargs):
		if self._marshmallow_schema:
			schema = self._marshmallow_schema()
			validated_schema = schema.load(kwargs)
		return self.cupdate(row_id=None, format_output=format_output, **kwargs)

	def cread(self, row_id, format_output=True):

		row = self.read(row_id)[0]

		if format_output and self._marshmallow_schema:
			schema = self._marshmallow_schema()
			return schema.dump(row)
		else:
			return row

	def cupdate(self, row_id=None, format_output=True, check_conflict=True, conflict_params={}, partial_update=True, **kwargs):

		validated_schema = kwargs
		if self._marshmallow_schema:
			schema = self._marshmallow_schema(partial=True)
			validated_schema = schema.load(kwargs)

		row = None
		if row_id:
			row = row_update_helper(row_id, conflict_params=conflict_params, check_conflict=check_conflict, **validated_schema)
		else:
			row = row_create_helper(conflict_params=conflict_params, check_conflict=check_conflict, **validated_schema)


		# for column in validated_schema:
		# 	if column in self._relationships:
		# 		rel_type = self._relationships[column]['rel_type']
		# 		rel_pk =  self.get_table(rel_table, db=self._db)
		# 		rel_table = self._relationships[column]['table']

		# 		# one to many
		# 		if rel_type == 'o2m':
		# 			child_ids = [getattr(child, rel_pk) for child in getattr(row, column)]
		# 			for child in validated_schema[column]:
		# 				child[rel_pk] = getattr(row, self._primary_key)
		# 				try:
		# 					child_row = row_update_helper(rel_table, child.get(rel_pk), **child)
		# 					if child_row.id in child_ids:
		# 						del child_ids[child_ids.index(child_row.id)]
		# 				except MissingError as e:
		# 					child_row = row_create_helper(rel_table, **child)

		# 			if not partial_update:
		# 				for child_id in child_ids:
		# 					row_delete_helper(rel_table, child_id)

		# 		# many to many
		# 		if rel_type = 'm2m':
		# 			child_ids = [getattr(child, rel_pk) for tag in getattr(row, column)]
		# 			for child in validated_schema[column]:
		# 				child_row = m2m_update_helper(rel_table, row, )

		# 				if getattr(child_row, rel_pk) in child_ids:
		# 					del child_ids[child_ids.index(getattr(child_row, rel_pk))]

		# 			if not partial_update:
		# 				for child_id in child_ids:
		# 					m2m_update_helper(rel_table, row, child_id, )




	def row_create_helper(self, conflict_params={}, check_conflict=True, **validated_schema):
		try:
			return self.create(conflict_params=conflict_params, check_conflict=check_conflict, **validated_schema)
		except Exception as e:
			self.rollback()
			raise e

	def row_update_helper(row_id,  conflict_params={},check_conflict=True, **validated_schema):
		try:
			return self.update(row_id, conflict_params=conflict_params,check_conflict=check_conflict, **validated_schema)
		except Exception as e:
			self.rollback()
			raise e

	def row_delete_helper(table, row_id):
		try:
			row = Row(table)
			child_row = row.delete(row_id)
		except Exception as e:
			db.session.rollback()
			raise e

	def m2m_update_helper(table, parent, row_id, fxn):
		try:
			row = Row(table)
			child_row = row.read(row_id)[0]
			getattr(parent, fxn)(child_row)
			return child_row
		except Exception as e:
			db.session.rollback()
			raise e

	def tiered_parent_helper(table, child_list, parent=None, child_attr="children", depth_limit=None):

		child_ids = []
		if parent:
			child_ids = [child.id for child in getattr(parent, child_attr)]
		# print(child_ids)
		child_rows = []
		for child in child_list:

			child_row = None
			if parent:
				child['parent_id'] = parent.id
			if child.get('id'):
				child_row = row_update_helper(table, child['id'], **child)
			else:
				child_row = row_create_helper(table, **child)
			child_rows.append(child_row)
			if child_attr in child:
				tiered_parent_helper(table, child[child_attr], parent=child_row, child_attr=child_attr)


		for child_id in child_ids:
			row_delete_helper(table, child_id)

		return child_rows

	def association_proxy_create_helper(table, parent, fxn, **values):

		table = CRUDHelpers.get_table(None, table, db=db)

		try:
			child_row = table(**values)
			getattr(parent, fxn)(child_row)
			return child_row
		except Exception as e:
			db.session.rollback()
			raise e

	def association_proxy_update_helper(table, parent, row_id, fxn):
		try:
			row = Row(table)
			child_row = row.read(row_id)[0]
			getattr(parent, fxn)(child_row)
			return child_row
		except Exception as e:
			db.session.rollback()
			raise e

	@classmethod
	def update(self, question_id=None, format_output=True, **kwargs):

		db.session.rollback()
		schema = QuestionSchema(partial=True)
		validated_schema = schema.load(kwargs)

		#create question
		question_row = None
		if question_id:
			question_row = row_update_helper('Question', question_id, **validated_schema)
		else:
			question_row = row_create_helper('Question', **validated_schema)

		# manage which shows question is associated with
		if 'shows' in validated_schema:
			show_ids = [show.id for show in question_row.shows]
			for show in validated_schema['shows']:
				show_row = m2m_update_helper('Show', question_row, show['id'], 'add_show')
				if show_row.id in show_ids:
					del show_ids[show_ids.index(show_row.id)]
			for show_id in show_ids:
				m2m_update_helper('Show', question_row, show_id, 'remove_show')

		# manage question links
		if 'question_links' in validated_schema:
			link_ids = [link.id for link in question_row.question_links]
			for link in validated_schema['question_links']:
				link['question_id'] = question_row.id
				if link.get('id'):
					link_row = row_update_helper('QuestionLink', link['id'], **link)
					if link_row.id in link_ids:
						del link_ids[link_ids.index(link_row.id)]
				else:
					link_row = row_create_helper('QuestionLink', **link)

			for link_id in link_ids:
				# print('retrive', retrieve_row('QuestionLink', link_id))
				row_delete_helper('QuestionLink', link_id)

		# update tags
		if 'tags' in validated_schema:
			tag_ids = [ tag.id for tag in question_row.tags ]
			for tag in validated_schema['tags']:
				tag_row = m2m_update_helper('QuestionTag', question_row, tag['id'], 'add_tag')

				if tag_row.id in tag_ids:
					del tag_ids[tag_ids.index(tag_row.id)]

			for tag_id in tag_ids:
				m2m_update_helper('QuestionTag', question_row, tag_id, 'remove_tag')

		# update answers
		if 'answers' in validated_schema:
			answer_ids = [answer.id for answer in question_row.answers]

			for answer in validated_schema['answers']:

				# make sure that the answer is not part of a subset. It must be the parent
				answer_row = retrieve_row('Answer', answer['id'])
				if answer_row and answer_row.parent:
					raise BaseCRUDError(msg="Invalid answer ID. Only \"main answers\" can be assigned to questions.", key="answers")

				answer_row = m2m_update_helper('Answer', question_row, answer['id'], 'add_answer')
				if answer_row.id in answer_ids:
					del answer_ids[answer_ids.index(answer_row.id)]

			for answer_id in answer_ids:
				m2m_update_helper('Answer', question_row, answer_id, "remove_answer")



		# manage answer links
		if 'answer_links' in validated_schema:
			link_ids = [link.id for link in question_row.answer_links]
			for link in validated_schema['answer_links']:
				link['question_id'] = question_row.id
				if link.get('id'):
					link_row = row_update_helper('AnswerLink', link['id'], **link)
					if link_row.id in link_ids:
						del link_ids[link_ids.index(link_row.id)]
				else:
					link_row = row_create_helper('AnswerLink', **link)

			for link_id in link_ids:
				row_delete_helper('AnswerLink', link_id)




		# commit changes
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			raise e

		if format_output:
			return schema.dump(question_row)
		else:
			return question_row
