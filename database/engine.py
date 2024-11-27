from model import user_model
from sqlmodel import SQLModel, create_engine
from settings import DB_URL

engine = create_engine(DB_URL, echo=True)


def get_engine():
    SQLModel.metadata.create_all(engine)
