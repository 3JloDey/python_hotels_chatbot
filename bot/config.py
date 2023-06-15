from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    bot_token: str
    api_token: str
    bot_fsm_storage: str
    redis_dsn: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        bot_token=env.str("BOT_TOKEN"),
        api_token=env.str("API_TOKEN"),
        bot_fsm_storage=env.str("BOT_FSM_STORAGE"),
        redis_dsn=env.str("REDIS_DSN"),
    )
