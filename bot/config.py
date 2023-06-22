from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    """
    A class representing a Telegram bot.

    Attributes:
        token (str): The bot token.
        use_redis (str): Whether to use Redis or not.
        api_token (str): The API token.

    """

    token: str
    use_redis: str
    api_token: str


@dataclass
class Database:
    username: str
    password: str
    host: str
    name: str
    port: int


@dataclass
class Redis:
    """
    A class representing a Redis instance.

    Attributes:
        url (str): The URL for the Redis instance.

    """

    url: str


@dataclass
class Config:
    """
    A class representing the configuration of the application.

    Attributes:
        tg_bot (TgBot): The Telegram bot configuration.
        redis (Redis): The Redis configuration.

    """

    tg_bot: TgBot
    redis: Redis
    db: Database


def load_config(path: str | None = None) -> Config:
    """
    A function that loads the configuration from environment variables.

    Args:
        path (str | None): Optional path to the .env file.

    Returns:
        Config: The configuration object.

    """
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            use_redis=env.bool("USE_REDIS"),
            api_token=env.str("API_TOKEN"),
        ),
        redis=Redis(url=env.str("REDIS_DSN")),
        db=Database(
            username=env.str("DB_USERNAME"),
            password=env.str("DB_PASSWORD"),
            host=env.str("DB_HOST"),
            name=env.str("DB_NAME"),
            port=env.str("DB_PORT"),
        ),
    )
