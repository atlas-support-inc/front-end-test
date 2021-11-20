import databases
import sqlalchemy

database = databases.Database("sqlite:///./test.db")
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
     "sqlite:///./test.db", connect_args={"check_same_thread": False}
)