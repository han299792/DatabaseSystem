from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "postgresql://username:password@localhost:5432/dbname"

database = Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
metadata = MetaData()

