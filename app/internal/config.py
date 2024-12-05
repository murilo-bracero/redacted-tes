from os import getenv
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    """
    Classe responsável por armazenar as configurações do app

    Attributes:
        db_user: database user
        db_password: database password
        db_host: database host
        db_port: database port
        db_name: database name
        db_url: database url (optional)
    """
    db_user: Optional[str] = field(default=getenv("DB_USER"))
    db_password: Optional[str] = field(default=getenv("DB_PASSWORD"))
    db_host: Optional[str] = field(default=getenv("DB_HOST"))
    db_port: Optional[str] = field(default=getenv("DB_PORT"))
    db_name: Optional[str] = field(default=getenv("DB_NAME"))
    db_url: Optional[str] = field(default=None)

    def __post_init__(self):
        env_db_url = getenv("DB_URL")

        if env_db_url is None or env_db_url == "":
            self.db_url = f"postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
            return
        
        self.db_url = env_db_url

config = Config()