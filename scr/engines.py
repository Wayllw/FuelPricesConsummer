from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

def get_postgres_engine() -> Engine:
    """Retorna o engine de conexão para o PostgreSQL."""
    return create_engine(
        "postgresql+psycopg2://admin:adminpassword@localhost:5432/portfoliodb"
    )

def get_mysql_engine():
    return create_engine(
        "mysql+pymysql://admin:adminpassword@localhost:3306/portfoliodb",
    )

def get_oracle_engine() -> Engine:
    """Retorna o engine de conexão para o Oracle Database."""
    return create_engine(
        "oracle+oracledb://SYSTEM:adminpassword@localhost:1521/?service_name=FREEPDB1"
    )