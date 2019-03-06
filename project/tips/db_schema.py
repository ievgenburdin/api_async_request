from datetime import datetime
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import database as db


Base = declarative_base()


category_association_table = Table('category_association', Base.metadata,
    Column('tips_id', Integer, ForeignKey('tips.id')),
    Column('categories_id', Integer, ForeignKey('categories.id'), nullable=True),
)

product_association_table = Table('product_association', Base.metadata,
    Column('tips_id', Integer, ForeignKey('tips.id')),
    Column('products_id', Integer, ForeignKey('products.id'), nullable=True),
)

query_association_table = Table('query_association', Base.metadata,
    Column('tips_id', Integer, ForeignKey('tips.id')),
    Column('queries_id', Integer, ForeignKey('queries.id'), nullable=True),
)


class BaseExtendMixin(object):

    @classmethod
    def create(cls, kwargs):
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def filter(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs).all()


class Category(BaseExtendMixin, Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    external_id = Column(Integer)
    name = Column(Integer)

    tip = relationship("Tip",
                       secondary=category_association_table,
                       back_populates="category")

    def __init__(self, external_id, name):
        self.external_id = external_id
        self.name = name

    def __repr__(self):
        return "<Query(name='%s',)>" % (self.name)

    @classmethod
    def get_or_create(cls, kwargs):
        external_id = kwargs.get('external_id')
        name = kwargs.get('name')
        instance = db.session.query(cls).filter_by(external_id=external_id, name=name).first()

        if instance:
            return instance

        else:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()

            return instance


class Product(BaseExtendMixin, Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    url = Column(String)
    price = Column(Float)
    special_price = Column(Float)
    currency = Column(String)

    tip = relationship("Tip",
                       secondary=product_association_table,
                       back_populates="product")

    def __init__(self, name, image=None, url=None, price=None, special_price=None, currency=None):
        self.name = name
        self.image = image
        self.url = url
        self.price = price
        self.speciel_price = special_price
        self.currency = currency

    def __repr__(self):
        return "<Query(name='%s', price='%s')>" % (self.name, self.price)

    @classmethod
    def get_or_create(cls, kwargs):
        url = kwargs.get('url')
        name = kwargs.get('name')
        price = kwargs.get('price')
        special_price = kwargs.get('special_price')
        instance = db.session.query(cls).filter_by(name=name, price=price,
                                                   special_price=special_price,
                                                   url=url).first()
        if instance:
            return instance
        else:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance


class Query(BaseExtendMixin, Base):
    __tablename__ = 'queries'
    id = Column(Integer, primary_key=True)
    text_query = Column(String)

    tip = relationship("Tip",
                       secondary=query_association_table,
                       back_populates="query")

    def __inet__(self, text_query):
        self.text_query = text_query

    def __repr__(self):
        return "<Query(text_query='%s')>" % self.text_query

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_or_create(cls, kwargs):
        text_query = kwargs.get('text_query')

        instance = db.session.query(cls).filter_by(text_query=text_query).first()

        if instance:
            return instance

        else:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()

            return instance


class Tip(BaseExtendMixin, Base):
    __tablename__ = 'tips'
    id = Column(Integer, primary_key=True)
    text_query = Column(String)
    created = Column(DateTime(timezone=False), default=datetime.now)

    category = relationship("Category",
                            secondary=category_association_table,
                            back_populates="tip",)
    product = relationship("Product",
                           secondary=product_association_table,
                           back_populates="tip")
    query = relationship("Query",
                         secondary=query_association_table,
                         back_populates="tip")

    def __init__(self, text_query, product=None, query=None, category=None):
        self.text_query = text_query
        self.query = list(map(lambda x: db.session.merge(x), query))
        self.category = list(map(lambda x: db.session.merge(x), category))
        self.product = list(map(lambda x: db.session.merge(x), product))

    @classmethod
    def get_or_create(cls, **kwargs):
        text_query = kwargs.get('text_query')
        instance = db.session.query(cls).filter_by(price=text_query).first()

        if instance:
            return instance

        else:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()

            return instance

    @classmethod
    def get_latest(cls):
        tips = db.session.query(cls).order_by(cls.created.desc())
        latest = tips.first()

        return latest