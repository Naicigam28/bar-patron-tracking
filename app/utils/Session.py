from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .Settings import settings

postgress_user = settings.postgres_user
postgress_password = settings.postgres_password
postgress_host = settings.postgres_host
postgress_port = settings.postgres_port
postgress_db = settings.postgres_db


postgres_url = f"postgresql://{postgress_user}:{postgress_password}@{postgress_host}:{postgress_port}/{postgress_db}"

connect_args = {}
engine = create_engine(postgres_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
