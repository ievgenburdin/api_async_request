import asyncio
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import DB_NAME, DEBUG


loop = asyncio.get_event_loop()

db_name = DB_NAME
engine = create_engine('sqlite:///%s?check_same_thread=False' % db_name, echo=DEBUG)
session = scoped_session(sessionmaker(bind=engine))
db = session()


class AsyncDatabaseManager(object):

    executor = ThreadPoolExecutor(max_workers=4)

    async def get_or_create(self, model, **kwargs):

        instance = await loop.run_in_executor(
            self.executor, model.get_or_create, kwargs)

        return instance

    async def get_latest(self, model):

        instance = await loop.run_in_executor(
            self.executor, model.get_latest)

        return instance

    async def create(self, model, **kwargs):

        instance = await loop.run_in_executor(
            self.executor,
            model.create, kwargs)

        return instance

    async def filter(self, model, **kwargs):

        def filter_sync(self, model, kwargs):
            instance = db.query(model).filter_by(**kwargs).first()
            if instance:
                return instance
            else:
                instance = model(**kwargs)
                db.add(instance)
                db.commit()
                return instance

        instance = await loop.run_in_executor(
            self.executor,
            filter_sync, model, kwargs)

        return instance
