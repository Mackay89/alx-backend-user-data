#!/usr/bin/env python3
"""DB module
Handles database interactions for managing users.
"""
import logging
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User

logging.disable(logging.WARNING)


class DB:
    """DB class
    Provides methods for interacting with the database to manage users.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        Creates the SQLite database and initializes a session object.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        Creates a new session if one does not exist.
        Returns:
            Session: A SQLAlchemy Session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.

        Args:
            email (str): The email address of the new user.
            hashed_password (str): The hashed password of the new user.

        Returns:
            User: The newly created User object.

        Raises:
            Exception: If there is an error adding the user to the database.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            logging.error(f"Error adding user to database: {e}")
            self._session.rollback()
            raise
        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """Find a user by specified attributes.

        Args:
            **kwargs: Arbitrary keyword arguments corresponding to user
            attributes for filtering.

        Returns:
            User: The first user found that matches the provided attributes.

        Raises:
            NoResultFound: If no user is found matching the criteria.
            InvalidRequestError: If the query is invalid.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return user

    def update_user(self, user_id: int, **kwargs: Dict[str, str]) -> None:
        """Updates a user's attributes by their user ID.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Keyword arguments representing the user's attributes to
            update.

        Raises:
            ValueError: If the user is not found or an invalid attribute is
            provided.
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError(f"User with id {user_id} not found")

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"User has no attribute {key}")
            setattr(user, key, value)

        try:
            self._session.commit()
        except InvalidRequestError:
            raise ValueError("Invalid request to update user")
