import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USER = os.getenv("COGNODB_USER")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")
COGNODB_DATABASE = os.getenv("COGNODB_DATABASE", "neo4j")

_driver = None


def get_driver():
    global _driver

    if _driver is None:
        if not COGNODB_URI:
            raise RuntimeError("COGNODB_URI is not configured")

        if not COGNODB_PASSWORD:
            raise RuntimeError("COGNODB_PASSWORD is not configured")

        _driver = GraphDatabase.driver(
            COGNODB_URI,
            auth=(COGNODB_USER, COGNODB_PASSWORD),
        )

    return _driver


# def verify_connection():
#     driver = get_driver()
#     driver.verify_connectivity()

def verify_connection():
    driver = get_driver()

    with driver.session(database=COGNODB_DATABASE) as session:
        result = session.run("""
            MATCH (n)
            RETURN labels(n)[0] AS label, count(n) AS count
            ORDER BY count DESC
        """)

        for record in result:
            print(record.data())

def run_query(query: str, parameters: dict | None = None):
    driver = get_driver()

    with driver.session(database=COGNODB_DATABASE) as session:
        result = session.run(
            query,
            parameters or {},
        )

        return [record.data() for record in result]


def close_driver():
    global _driver

    if _driver:
        _driver.close()
        _driver = None


