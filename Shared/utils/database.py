from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_conn_string(db_name, host, port, user, password):
    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'


def get_db(model_base, conn_string):
    engine = create_engine(conn_string)
    db_session = sessionmaker(bind=engine)()
    model_base.metadata.create_all(engine)
    return engine, db_session
