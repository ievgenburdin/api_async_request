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


class Category(Base):
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


class Product(Base):
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


class Query(Base):
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


class Tip(Base):
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
        self.query = query
        self.category = category
        self.product = product

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

