from sqlmodel import Session, create_engine, SQLModel
from fastapi import Depends
from typing import Annotated

import os
from dotenv import load_dotenv

# para cargar las varianles de entorno
load_dotenv()

MYSQL_URL = os.getenv("MYSQL_URL")

if MYSQL_URL:
    url_connection = MYSQL_URL  # Para producción (Railway)
else:
    # Para desarrollo local
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_DB = os.getenv("MYSQL_DB")
    url_connection = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    
print("URL conexión:", url_connection)
engine = create_engine(url_connection)


def create_db_and_table():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# def reset_db():
#     SQLModel.metadata.drop_all(engine)
#     SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]
