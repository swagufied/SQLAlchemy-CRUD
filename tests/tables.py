from tests import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, Column, DateTime
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import joinedload_all
from sqlalchemy.orm import relationship

class TableBase(Base):
	__abstract__ = True
	id = Column(Integer, primary_key=True)
	creation_date = Column(DateTime, default=datetime.utcnow)


class User(TableBase):
	__tablename__ = "User"
	# id = Column(Integer, primary_key=True)
	username = Column(String(50), nullable=False)
	email = Column(String(50), unique=True)

	comments = relationship('Comment', backref='user')

class Comment(TableBase):
	__tablename__ = "Comment"
	# id = Column(Integer, primary_key=True)
	text = Column(String(100))
	user_id = Column(Integer, ForeignKey("User.id"))
