import os
import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from utils.database import get_db, get_db_conn_string

Base = declarative_base()

conn_string = get_db_conn_string(
    db_name=os.getenv('ORDER_DB_NAME'),
    port=os.getenv('ORDER_DB_PORT'),
    host=os.getenv('ORDER_DB_HOST'),
    password=os.getenv('ORDER_DB_PASS'),
    user=os.getenv('ORDER_DB_USER'),
)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(
        String,
        primary_key=True,
        unique=True,
        nullable=False
    )
    amount = Column(
        Integer,
        nullable=False
    )
    product_id = Column(
        String,
        nullable=False
    )
    user_id = Column(
        String,
        nullable=False
    )

    def __init__(self, amount: int, product_id: str, user_id: str):
        self.id = str(uuid.uuid4())
        self.amount = amount
        self.product_id = product_id
        self.user_id = user_id


engine, db_session = get_db(model_base=Base, conn_string=conn_string)
