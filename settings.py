import datetime
from pathlib import Path

import dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent

IMAGES_DIR = Path(BASE_DIR, 'images')

ENV_FILE = Path(BASE_DIR, '.env')
dotenv.load_dotenv(ENV_FILE)

MOSCOW_TIME_DIFFERENCE = datetime.timedelta(hours=3)

BOT_DATA = Path(BASE_DIR, 'bot_data')
BOT_DATA.mkdir(exist_ok=True)


class PostgresSettings(BaseSettings):
    HOST: str
    USER: str
    PASSWORD: str
    DATABASE: str
    PORT: int = 5432

    @property
    def url(self) -> str:
        return f'postgres://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'

    @property
    def url_for_persistence(self) -> str:
        return f'postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'

    class Config:
        case_sensitive = False
        env_prefix = "PG_"


class MongoSettings(BaseSettings):
    HOST: str
    USER: str
    PASSWORD: str
    DATABASE: str = 'admin'
    PORT: int = 27017

    @property
    def url(self) -> str:
        return (
            f'mongodb://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?retryWrites=true&w=majority'
        )

    class Config:
        case_sensitive = False
        env_prefix = "MONGO_"


class BotSettings(BaseSettings):
    TOKEN: str


    MAX_QUESTION_PER_DAY: int = 3

    class Config:
        case_sensitive = False


bot_settings = BotSettings()