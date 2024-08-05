class UserRepository:
    def add_user(self, user):
        raise NotImplementedError("Subclasses should implement this method")

    def edit_user(self, user):
        raise NotImplementedError("Subclasses should implement this method")

    def get_user(self, iduser):
        raise NotImplementedError("Subclasses should implement this method")

    def delete_user(self, iduser):
        raise NotImplementedError("Subclasses should implement this method")

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.id] = user

    def edit_user(self, user):
        if user.id in self.users:
            self.users[user.id] = user

    def get_user(self, iduser):
        return self.users.get(iduser)

    def delete_user(self, iduser):
        if iduser in self.users:
            del self.users[iduser]

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    lastname = Column(String)
    firstname = Column(String)
    middlename = Column(String)

class DatabaseUserRepository(UserRepository):
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_user(self, user):
        session = self.Session()
        db_user = UserModel(id=user.id, lastname=user.lastname, firstname=user.firstname, middlename=user.middlename)
        session.add(db_user)
        session.commit()
        session.close()

    def edit_user(self, user):
        session = self.Session()
        db_user = session.query(UserModel).filter_by(id=user.id).first()
        if db_user:
            db_user.lastname = user.lastname
            db_user.firstname = user.firstname
            db_user.middlename = user.middlename
            session.commit()
        session.close()

    def get_user(self, iduser):
        session = self.Session()
        db_user = session.query(UserModel).filter_by(id=iduser).first()
        session.close()
        if db_user:
            return User(db_user.id, db_user.lastname, db_user.firstname, db_user.middlename)
        return None

    def delete_user(self, iduser):
        session = self.Session()
        db_user = session.query(UserModel).filter_by(id=iduser).first()
        if db_user:
            session.delete(db_user)
            session.commit()
        session.close()
