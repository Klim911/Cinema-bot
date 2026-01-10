from dataclasses import dataclass
from environs import Env
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
MOVIES_JSON = BASE_DIR / "movies.json"

@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class LogSettings:
    level: str
    format: str


@dataclass
class Config:
    bot: TgBot
    log: LogSettings


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        bot=TgBot(token=env('BOT_TOKEN')),
        log=LogSettings(level=env("LOG_LEVEL"), format=env("LOG_FORMAT"))
    )