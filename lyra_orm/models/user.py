from lyra_orm.config import session
from lyra_orm.config import Base
from sqlalchemy import Column, String, Integer, Text, Boolean, Unicode
from sqlalchemy.dialects.mysql import BOOLEAN


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(Text)
    is_admin = Column(BOOLEAN, default=False)
    is_active = Column(BOOLEAN, default=True)

    def is_user_admin(self):
        return True if self.is_admin == True else False

    @classmethod
    def find_by_username(cls, username):
        return session.query(cls).filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        user = session.query(cls).filter_by(id=_id).first()
        return user

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id).encode("utf-8").decode("utf-8")

    def save_to_db(self):
        session.add(self)
        session.commit()
        session.close()

    def delete_from_db(self):
        session.delete(self)
        session.commit()
        session.close()
