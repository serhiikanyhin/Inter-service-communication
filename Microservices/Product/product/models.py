import os
import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from utils.database import get_db, get_db_conn_string

Base = declarative_base()

conn_string = get_db_conn_string(
    db_name=os.getenv('PRODUCT_DB_NAME'),
    port=os.getenv('PRODUCT_DB_PORT'),
    host=os.getenv('PRODUCT_DB_HOST'),
    password=os.getenv('PRODUCT_DB_PASS'),
    user=os.getenv('PRODUCT_DB_USER'),
)


class Product(Base):
    __tablename__ = 'products'

    id = Column(
        String,
        primary_key=True,
        unique=True,
        nullable=False
    )
    name = Column(
        String,
        unique=True,
        nullable=False
    )
    amount = Column(
        Integer,
        nullable=False
    )

    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.amount = 0


engine, db_session = get_db(model_base=Base, conn_string=conn_string)
