import logging

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker

from tabulate import tabulate

LOGGER = logging.getLogger(__name__)

CONNECTION_URL = 'postgresql://postgres:postgres@localhost:5432/postgres'
engine = create_engine(CONNECTION_URL)
Session = sessionmaker(autoflush=False, bind=engine)

meta = MetaData()
test_data = Table(
    'test_data', meta,
    Column('id', Integer, primary_key = True),
    Column('name', String),
    Column('count', Integer),
)

meta.create_all(engine)


def test_connection():
    s = Session()
    r = s.execute('SELECT 1')
    _print_table('test_connection', r)



def _print_table(test_name, result):
    data = result.fetchall()
    headers = result.keys()
    table = tabulate(data, headers, tablefmt='psql')
    LOGGER.debug('%s:\n%s', test_name, table)

