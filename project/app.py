import os
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from tips.client import TipsClient
from tips.helpers import QueryBuilder
from tips.db_schema import Base

loop = asyncio.get_event_loop()


def create_test_database():
    engine = create_engine('sqlite:///' + config.DB_NAME)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)


def run_client():
    print("Parsing started!")
    qb = QueryBuilder(config.ALPHABET_LIST, config.MAX_QUERY_LENGTH)
    client = TipsClient(config.API_HOST, config.API_URL, qb)
    loop.run_until_complete(client.main())
    print("Parsing queries done!")


if __name__ == "__main__":
    if not os.path.exists('./' + config.DB_NAME ):
        create_test_database()
    run_client()
