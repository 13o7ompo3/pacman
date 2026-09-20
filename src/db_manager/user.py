"""
This module provides classes and methods for managing user data
in a Pacman game.
It includes the User class for representing individual users
and the UserManager class for handling user-related operations
"""

import hashlib
import json
import logging
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError, model_validator

logger = logging.getLogger(__name__)


class User(BaseModel):
    """
    Represents a user in the system.

    Attributes:
        username (str): The username of the user.
        password (str): The hashed password of the user.
        highscore (int): The highscore of the user.
    """

    username: str = Field(..., min_length=1, max_length=10)
    password: str
    highscore: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_user(self) -> "User":
        """Validates the user data after model initialization.

        Returns:
            User: The validated user instance.
        """
        if not self.username.replace(" ", "").isalnum():
            raise ValueError("Username must be alphanumeric and spaces only.")
        return self


class UserManager:
    """Class for managing user data."""

    def __init__(self, db_dir: str = "./database") -> None:
        """
        Initializes the UserManager with a specified database directory.

        Args:
            db_dir (str): The directory where user data will be stored.
        """
        self.loged_in_user: User | None = None
        self.db_dir = Path(db_dir)
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.users: dict[str, User] = {}
        self.load_all_users()

    def load_all_users(self) -> None:
        """
        Loads all user data from the database directory into memory.
        """
        for user_file in self.db_dir.glob("*.json"):
            try:
                with open(user_file, "r") as f:
                    user_data = json.load(f)
                    user = User(**user_data)
                    if user.username != user_file.stem:
                        logger.warning(
                            f"Username in file {user_file} does not match "
                            "the filename. Skipping this user."
                        )
                        continue
                    self.users[user.username] = user
                logger.info(f"Loaded user '{user.username}' data.")
            except json.JSONDecodeError as e:
                logger.warning(
                    f"Invalid user JSON in database {user_file}: {e}"
                )
            except ValidationError as e:
                for error in e.errors():
                    logger.warning(
                        "Invalid user data in database "
                        f"{user_file}: {error['msg']}"
                    )
            except ValueError as e:
                logger.warning(
                    f"Invalid user data in database {user_file}: {e}"
                )
            except Exception as e:
                logger.warning(
                    "Unexpected error while loading user from "
                    f"{user_file}: {e}"
                )
        logger.info(f"Total users loaded: {len(self.users)}")

    def save_user_data(self, user: User) -> None:
        """
        Saves the user data to a JSON file in the database directory.

        Args:
            user (User): The user object to save.
        """
        path = self.db_dir / f"{user.username}.json"
        self.db_dir.mkdir(parents=True, exist_ok=True)
        if path.exists():
            path.unlink()
        with open(path, "w") as f:
            json.dump(user.model_dump(), f, indent=4)

        logger.info(f"User data for '{user.username}' saved successfully.")

    def is_existing_user(self, username: str) -> bool:
        """
        Checks if a user with the given username exists.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return username in self.users

    def create_new_user(self, username: str, password: str) -> None:
        """
        Creates a new user with the given username and password.

        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.
        """
        if self.is_existing_user(username):
            raise ValueError(f"User '{username}' already exists.")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            user = User(username=username, password=hashed_password)
        except ValidationError as e:
            error_msg = e.errors()[0]["msg"]
            raise ValueError(
                f"Invalid user data for '{username}': {error_msg}"
            )

        self.save_user_data(user)
        self.users[username] = user

        logger.info(f"User created successfully: {username}")
        logger.info(f"User '{username}' is now logged in.")
        self.loged_in_user = user

    def authenticate_user(self, username: str, password: str) -> None:
        """
        Authenticates a user with the given username and password.

        Args:
            username (str): The username of the user to authenticate.
            password (str): The password of the user to authenticate.
        """
        if not self.is_existing_user(username):
            raise ValueError(f"User '{username}' does not exist.")

        user = self.users[username]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if user.password != hashed_password:
            raise ValueError("Incorrect password.")

        logger.info(f"User authenticated successfully: {username}")
        self.loged_in_user = user

    def update_highscore(self, new_score: int) -> None:
        """
        Updates the highscore for the currently logged-in user.

        Args:
            new_score (int): The new highscore to set.
        """
        if self.loged_in_user is None:
            raise ValueError("No user is currently logged in.")

        if new_score > self.loged_in_user.highscore:
            self.loged_in_user.highscore = new_score
            self.save_user_data(self.loged_in_user)
            logger.info(
                f"Highscore updated for user '{self.loged_in_user.username}' "
                f"to {new_score}."
            )
        else:
            logger.info(
                f"New score {new_score} is not higher than the current "
                f"highscore {self.loged_in_user.highscore} for user "
                f"'{self.loged_in_user.username}'."
            )

    def logout_user(self) -> None:
        """
        Logs out the currently logged-in user.
        """
        if self.loged_in_user is not None:
            logger.info(f"User '{self.loged_in_user.username}' logged out.")
            self.loged_in_user = None
        else:
            logger.warning("No user is currently logged in to log out.")

    def get_leaderboard(self) -> list[User]:
        """
        Returns a list of users sorted by their highscore in descending order.

        Returns:
            list[User]: A list of User objects sorted by highscore.
        """
        return sorted(
            self.users.values(), key=lambda user: user.highscore, reverse=True
        )
