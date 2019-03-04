from concurrent.futures import ThreadPoolExecutor

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import DB_NAME, DEBUG
from app import loop


db_name = DB_NAME + '.db'

engine = create_engine('sqlite:///my_db.db?check_same_thread=False', echo=DEBUG)
session = scoped_session(sessionmaker(bind=engine))
db = session()


class AsyncDatabaseManager(object):
    executor = ThreadPoolExecutor(max_workers=4)

    async def get_or_create(self, model, **kwargs):

        def get_or_create_sync(model, kwargs):
            instance = db.query(model).filter_by(**kwargs).first()
            if instance:
                print("exist", instance)
                return instance
            else:
                instance = model(**kwargs)
                db.add(instance)
                db.commit()
                return instance

        instance = await loop.run_in_executor(
            self.executor,
            get_or_create_sync, model, kwargs)

        return instance

    async def create(self, model, **kwargs):

        def create_sync(model, kwargs):
            instance = model(**kwargs)
            db.add(instance)
            db.commit()
            return instance

        instance = await loop.run_in_executor(
            self.executor,
            create_sync, model, kwargs)

        return instance

    async def filter(self, model, **kwargs):

        def filter_sync(self, model, kwargs):
            instance = db.query(model).filter_by(**kwargs).first()
            if instance:
                print("exist", instance)
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
