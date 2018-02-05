from pandas import DataFrame
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///otc.db', echo=True)
DBSession = sessionmaker(bind=engine)

base = declarative_base()


class Exchange:
    def __init__(self):
        self.__table_name__ = self.__class__.__name__
        self.id = Column('id', Integer, primary_key=True)
        self.symbol = Column('symbol', String(128))
        self.price = Column('price', Float)
        self.date_time = Column('datetime', DateTime)


class Binance(base, Exchange):
    def __init__(self):
        Exchange.__init__(self)


class Otc(Exchange):
    def __init__(self):
        Exchange.__init__(self)
        self.binance_id = Column(Float, ForeignKey("Binance.id"))
        self.rate = Column(Float)
        self.person_num = Column(Integer)


class Otcbtc(base, Otc):
    pass


class LocalCoins(base, Otc):
    pass


class Coinw(base, Otc):
    pass


def insert(exchange):
    session = DBSession()
    session.add(exchange)
    session.commit()
    session.close()


def query(table, where=None):
    session = DBSession()
    entites = session.query(table).filter(where)
    return DataFrame(entites)
