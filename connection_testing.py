import logging
import time

from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from tabulate import tabulate

import pytest

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

    def __repr__(self):
        return f'TestData<{self.test_data_id=};{self.name=};{self.count=}>'

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


def test_donothing_sessions():
    for i in range(0,100):
        s = Session()
    _check_status('test_donothing_sessions')


def test_readonly_hanging_sessions():
    s_alpha = Session()
    try:
        td = TestData(name='testdata_alpha', count=1)
        s_alpha.add(td)
        s_alpha.commit()
    except:
        s_alpha.rollback()

    stale_sessions = []
    try:
        for i in range(0,10):
            s = Session()
            stale_sessions.append(s)
            query = s.query(TestData)
            found = query.first()

        _check_status('before closing test_readonly_hanging_sessions')
    finally:
        for s in stale_sessions:
            s.close()
    _check_status('after closing test_readonly_hanging_sessions')


# Convenience Methods

def _print_table(test_name, result):
    data = result.fetchall()
    headers = result.keys()
    table = tabulate(data, headers, tablefmt='psql')
    LOGGER.debug('%s:\n%s', test_name, table)

def _check_status(test_name):
    pool = engine.pool
    headers = ['property', 'value']
    data = [
        ('size', pool.size()),
        ('timeout', pool.timeout()),
        ('checkedin', pool.checkedin()),
        ('checkedout', pool.checkedout()),
        ('overflow', pool.overflow()),
    ]
    table = tabulate(data,headers, tablefmt='simple')
    LOGGER.debug('DB Status (%s):\n%s', test_name, table)
    return pool
