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
	name = Column(String(50), nullable=False)

	comments = relationship('Comment', backref='user') #o2m with backref
	nicknames = relationship('NickName', back_populates="user") #o2m with back_populates

	roles = relationship("Role", secondary=user_role, backref="users") #m2m with backref

	#m2m with back_populates

	details = relationship("UserDetails", uselist=False, back_populates="user") # o2o with back_populates
	sensitive_info = relationship("UserSensitiveInfo", uselist=False, backref="user") # o2o with backref

	def __repr__(self):
		return "<User {}: {}>".format(self.id, self.name)

class NickName(TableBase):
	__tablename__ = "NickName"
	name = Column(String(50))
	user_id = Column(Integer, ForeignKey("User.id"))

	user = relationship("User", back_populates="nicknames")

class UserDetails(TableBase):
	__tablename__ = "UserDetails"
	is_active = Column(Boolean, default=True)
	user_id = Column(Integer, ForeignKey("User.id"))

	user = relationship("User", back_populates="details")

class UserSensitiveInfo(TableBase):
	__tablename__ = "UserSensitiveInfo"
	password = Column(String(50))
	user_id = Column(Integer, ForeignKey("User.id"))


class Role(TableBase):
	__tablename__ = "Role"
	name = Column(String(30))


class Comment(TableBase):
	__tablename__ = "Comment"
	# id = Column(Integer, primary_key=True)
	text = Column(String(100))
	user_id = Column(Integer, ForeignKey("User.id"))

	# replies =
