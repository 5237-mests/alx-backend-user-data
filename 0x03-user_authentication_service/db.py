#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """adds new user to database"""
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            return None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """find user from db"""
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
            results = self._session.query(User).filter(
                tuple_(*fields).in_([tuple(values)])
            ).first()
            if results is None:
                raise NoResultFound()
            return results

    def update_user(self, user_id: int, **kwargs) -> None:
        """update user based on id"""
        for key, value in kwargs.items():
            if hasattr(User, key):
                try:
                    self.find_user_by(id=user_id)
                except Exception:
                    raise ValueError
                setattr(User, key, value)
                self._session.commit()
                self._session.close()
        return None
