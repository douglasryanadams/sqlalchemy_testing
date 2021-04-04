import logging

from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from tabulate import tabulate

LOGGER = logging.getLogger(__name__)


# Set up database

CONNECTION_URL = 'postgresql://postgres:postgres@localhost:5432/postgres'
engine = create_engine(CONNECTION_URL)
Base = declarative_base()
Session = sessionmaker(autoflush=False, bind=engine)

class TestData(Base):
    __tablename__ = 'test_data'
    test_data_id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    count = Column('count', Integer)

Base.metadata.create_all(engine)


# Run Tests

def test_connection():
    s = Session()
    r = s.execute('SELECT 1')
    _print_table('test_connection', r)


def test_crud():
    s = Session()
    try:
        for i in range(0,10):
            td = TestData(name=f'name_{i}', count=22)
            s.add(td)
        s.commit()
        r = s.execute('SELECT * FROM test_data')
        _print_table('test_crud', r)

        s.execute('DELETE FROM test_data')
        s.commit()
    finally:
        s.close()


# Convenience Methods

def _print_table(test_name, result):
    data = result.fetchall()
    headers = result.keys()
    table = tabulate(data, headers, tablefmt='psql')
    LOGGER.debug('%s:\n%s', test_name, table)

