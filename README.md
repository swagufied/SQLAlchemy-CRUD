**SQLAlchemy CRUD Tool**

This is a project that can ease the integration of SQLAlchemy into your project. The goal is to minimize the amount of code necessary, particularly in updating relationships. There are other SQLAlchemy CRUD tools out there, but this is something they don't do.

**How will it work?**

- Assuming you have data as outlined below, you only require a single line and reference to the main table that is being updated to manage all of its relationships. No need to loop through each list item in a relationship field and update them individually.
```
import SQLAlchemyCRUD

data = {
  'username': 'user',
  'nicknames': [{    # one-to-many-relationship
      'name': 'bob'
    },{
      'name': 'joe'
    }]
  'roles': [{        # many-to-many relationship
      'role': 'admin'
    },{
      'role': 'member'
    }]
}
SQLAlchemyCRUD.create(User, data)
```



**What features will it have?**
Listed below are featured aside from direct CRUD functions.

- Detection of basic constraints. At the moment, its not clear how far this feature can extend, but it does work for unique constraints. For example, if a table has a unique constraint on a column and the constraint is being violated by input data, SQLAlchemyCRUD would return an error object that contains information for customizeable error messages (e.g. column of violation, row that input violated, etc). Currently, all you would know is that some constraint was violated (e.g. Integrity Error). This works by running a query first to search for any violations rather than carrying out the CRUD procedure and catching errors.


- Customized constraints. This feature's implementation is not fully fleshed out, but it might look like something as follows. Both implementations would make sure that the username input data does not exist in the User table before committing.
```
constraints = {
  'ne': ['username']
}

SQLAlchemyCRUD.configure(User, create_constraints=constraints)

or

SQLAlchemyCRUD.create(User, data, constraints=constraints)
```

- A search function that is meant to work as a filter function, but can also serve as a full text search. A preview into how it will work can be seen below. The function will return a statement that can be run by session.filter(). The results will return all rows that include "sam" in the username and not equal to "sammy".
```
filters = {
  'and': [
    {'like': ['username', 'sam']}
    {'ne': ['username', 'sammy']}
  ]
}

query = sqlize_dict(User, filters)
session.filter(query).all()
```
