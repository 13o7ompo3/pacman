import hashlib
import json
from pathlib import Path
from typing import Dict
from pydantic import BaseModel, Field, ValidationError, model_validator
import logging

logger = logging.getLogger(__name__)


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
        self.loged_in_user: User | None = None
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
        path = self.db_dir / f"{user.username}.json"
        self.db_dir.mkdir(parents=True, exist_ok=True)
        if path.exists():
            path.unlink()
        with open(path, "w") as f:
            json.dump(user.model_dump(), f, indent=4)

        logger.info(f"User data for '{user.username}' saved successfully.")

    def is_existing_user(self, username: str) -> bool:
        return username in self.users

    def create_new_user(self, username: str, password: str) -> None:
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
        if not self.is_existing_user(username):
            raise ValueError(f"User '{username}' does not exist.")

        user = self.users[username]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if user.password != hashed_password:
            raise ValueError("Incorrect password.")

        logger.info(f"User authenticated successfully: {username}")
        self.loged_in_user = user
    
    def update_highscore(self, new_score: int) -> None:
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
        if self.loged_in_user is not None:
            logger.info(f"User '{self.loged_in_user.username}' logged out.")
            self.loged_in_user = None
        else:
            logger.warning("No user is currently logged in to log out.")
    
    def get_leaderboard(self) -> list[User]:
        return sorted(
            self.users.values(), key=lambda user: user.highscore, reverse=True
        )
