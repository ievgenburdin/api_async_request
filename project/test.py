import asyncio
from concurrent.futures import ThreadPoolExecutor

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from database import DB_NAME
from tips.client import TipsClient
from tips.helpers import QueryBuilder

# def create_test_database():
#     engine = create_engine('sqlite:///' + DB_NAME)
#     session = sessionmaker()
#     session.configure(bind=engine)
#     Base.metadata.create_all(engine)
#
# def remove_test_database():
#     pass

def test_tips_client():
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=4)
    qb = QueryBuilder(config.ALPHABET_LIST, config.MAX_QUERY_LENGTH)
    client = TipsClient(config.API_HOST, config.API_URL, qb)
    loop.run_until_complete(client.main())



if __name__ == "__main__":
    test_tips_client()

