from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_NAME
from app import executor
from app import loop


db_name = DB_NAME + '.db'

engine = create_engine('sqlite:///my_db.db', echo=True)
session = sessionmaker()
session.configure(bind=engine)
session = session()


class DatabaseManager(object):
    session = session
    loop = loop
    sync_executor = executor

    async def get_or_create(self, model, **kwargs):
        instance = await loop.run_in_executor(
            self.sync_executor,
            self.get_or_create_sync, model, kwargs)
        return instance


    def get_or_create_sync(self, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            print("exist", instance)
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            print("created", instance)
            return instance

