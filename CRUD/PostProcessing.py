class PostProcessing:


	def postprocess(row, schema=schema, format_output=format_output):
		return


	def dump(query, depth = 1):
		"""
		takes a sqlalchemy query result and converts it to a dict
		"""
		def dictify(query, depth):
			return

		return_dict = None
		if isinstance(query, list):
			return_dict = []
			for q in query:
				return_dict.append(dictify(q, depth))
		else:
			return_dict = dictify(query, depth)

		return return_dict