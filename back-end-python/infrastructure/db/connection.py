"""Infrastructure: SQL Server connection factory."""
import os
import warnings

import pyodbc
from contextlib import contextmanager

warnings.filterwarnings(
    "ignore", message="The 'validation_alias' attribute", category=UserWarning
)

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

DEFAULT_CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=OnThiDGNL_DB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", DEFAULT_CONN_STR)


def open_connection() -> pyodbc.Connection:
    conn = pyodbc.connect(DB_CONNECTION_STRING)
    conn.autocommit = False
    return conn


@contextmanager
def get_db():
    conn = open_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
