from sqlalchemy.engine import create_engine, URL
import os

url = URL.create(
    drivername="psycopg2",
    username = os.environ['DB_USER'],
    password = os.environ['DB_PASS'],
    host = os.environ['DB_HOST'],
    port = 5432,
    database = 'dev-academiq'
)
engine = create_engine(url,pool_size = 10)