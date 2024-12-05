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
    """
    db_user: Optional[str] = field(default=getenv("DB_USER"))
    db_password: Optional[str] = field(default=getenv("DB_PASSWORD"))
    db_host: Optional[str] = field(default=getenv("DB_HOST"))
    db_port: Optional[str] = field(default=getenv("DB_PORT"))
    db_name: Optional[str] = field(default=getenv("DB_NAME"))
    db_url: Optional[str] = field(default=None)

    def __post_init__(self):
        # create a database URL using psycopg
        self.db_url = f"postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

config = Config()