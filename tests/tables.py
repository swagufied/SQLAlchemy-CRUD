from tests import Base
from datetime import datetime
from sqlalchemy import Table, ForeignKey
from sqlalchemy import Integer, Column, DateTime, Boolean
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import joinedload_all
from sqlalchemy.orm import relationship

class TableBase(Base):
	__abstract__ = True
	id = Column(Integer, primary_key=True)
	creation_date = Column(DateTime, default=datetime.utcnow)

user_role = Table('user_role', Base.metadata,
	Column('user_id', Integer, ForeignKey('User.id')),
	Column('role_id', Integer, ForeignKey('Role.id'))
)

class User(TableBase):
	__tablename__ = "User"
	# id = Column(Integer, primary_key=True)
	username = Column(String(50), nullable=False)
	email = Column(String(50), unique=True)

	comments = relationship('Comment', backref='user')
	roles = relationship("Role", secondary=user_role, backref="users")
	details = relationship("UserDetails", uselist=False, back_populates="user")

class UserDetails(TableBase):
	__tablename__ = "UserDetails"
	is_active = Column(Boolean, default=True)
	user_id = Column(Integer, ForeignKey("User.id"))

	user = relationship("User", back_populates="details")

class Role(TableBase):
	__tablename__ = "Role"
	name = Column(String(30))


class Comment(TableBase):
	__tablename__ = "Comment"
	# id = Column(Integer, primary_key=True)
	text = Column(String(100))
	user_id = Column(Integer, ForeignKey("User.id"))
