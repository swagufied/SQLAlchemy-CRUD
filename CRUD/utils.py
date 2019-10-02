


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