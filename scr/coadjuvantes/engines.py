from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
import os

load_dotenv()
postgres_url= os.getenv("DB_POSTGRES_RDS")
mysql_url= os.getenv("DB_MYSQL_RDS")
oracle_url= os.getenv("DB_ORACLE")


def get_postgres_engine() -> Engine:
    return create_engine(
        postgres_url,
    )

def get_mysql_engine():
    return create_engine(
        mysql_url,
    )

def get_oracle_engine() -> Engine:
    return create_engine(
        oracle_url,
    )