#Python
from datetime import date,datetime
#SqlAlchemy
from sqlalchemy import Boolean, Column,ForeignKey,DateTime, Integer, String,Date
from sqlalchemy.orm import relationship
#TwitterApi
from .database import Base

class User(Base):
    __tablename__="users"
    id= Column(Integer,primary_key=True,index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    first_name=Column(String)
    last_name=Column(String)
    birth_date=Column(Date)

    tweets= relationship(
        "Tweet",
        back_populates="users",
        passive_deletes=True,
        cascade="all, delete",
        )

class Tweet(Base):
    __tablename__="tweets"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime,default=datetime.today())
    updated_at = Column(DateTime,default=datetime.today())

    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"))
    users = relationship("User", back_populates="tweets")
    