import hashlib
import json
from pathlib import Path
from typing import Dict
from pydantic import BaseModel, Field, ValidationError, model_validator
import logging

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


class User(BaseModel):
    username: str = Field(..., min_length=1, max_length=10)
    password: str  # This will store the hashed password
    highscore: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_user(self):
        if not self.username.replace(" ", "").isalnum():
            raise ValueError("Username must be alphanumeric and spaces only.")
        return self


class UserManager:
    def __init__(self, db_dir: str = "./database") -> None:
        self.db_dir = Path(db_dir)
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.users: Dict[str, User] = {}
        self.load_all_users()

    def load_all_users(self) -> None:
        for user_file in self.db_dir.glob("*.json"):
            try:
                with open(user_file, "r") as f:
                    user_data = json.load(f)
                    user = User(**user_data)
                    self.users[user.username] = user
                logging.info(f"Loaded user '{user.username}' data.")
            except json.JSONDecodeError as e:
                logging.warning(
                    f"Invalid user JSON in database {user_file}: {e}"
                )
            except ValidationError as e:
                for error in e.errors():
                    logging.warning(
                        "Invalid user data in database "
                        f"{user_file}: {error['msg']}"
                    )
            except ValueError as e:
                logging.warning(
                    f"Invalid user data in database {user_file}: {e}"
                )
            except Exception as e:
                logging.warning(
                    "Unexpected error while loading user from "
                    f"{user_file}: {e}"
                )
        logging.info(f"Total users loaded: {len(self.users)}")

    def save_user_data(self, user: User) -> None:
        path = self.db_dir / f"{user.username}.json"
        self.db_dir.mkdir(parents=True, exist_ok=True)
        if path.exists():
            path.unlink()
        with open(path, "w") as f:
            json.dump(user.model_dump(), f, indent=4)

        logging.info(f"User data for '{user.username}' saved successfully.")

    def is_existing_user(self, username: str) -> bool:
        return username in self.users

    def create_new_user(self, username: str, password: str) -> User:
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

        logging.info(f"User created successfully: {username}")
        return user

    def authenticate_user(self, username: str, password: str) -> User:
        if not self.is_existing_user(username):
            raise ValueError(f"User '{username}' does not exist.")

        user = self.users[username]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if user.password != hashed_password:
            raise ValueError("Incorrect password.")

        logging.info(f"User authenticated successfully: {username}")
        return user
