import os
from typing import Callable

from dotenv import load_dotenv


class Config:

    def read(self) -> None:
        load_dotenv()

        self.discord_log_webhook = self.__must_get_env("DISCORD_LOG_WEBHOOK")
        self.discord_status_webhook = self.__must_get_env("DISCORD_STATUS_WEBHOOK")

        self.fazdb_db_max_retries = self.__must_get_env("FAZDB_DB_MAX_RETRIES", int)

        self.mysql_host = self.__must_get_env("MYSQL_HOST")
        self.mysql_port = self.__must_get_env("MYSQL_PORT", int)
        self.mysql_username = self.__must_get_env("MYSQL_USER")
        self.mysql_password = self.__must_get_env("MYSQL_PASSWORD")
        self.fazdb_db_name = self.__must_get_env("MYSQL_FAZDB_DATABASE")

    def __must_get_env[T](self, key: str, type_strategy: Callable[[str], T] = str) -> T:
        try:
            env = os.getenv(key)
            return type_strategy(env)  # type: ignore
        except ValueError:
            raise ValueError(f"Failed parsing environment variable {key} into type {type_strategy}")
