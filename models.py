import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ =  'publishers'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, unique=True)
    def __repr__(self):
        return f"Publisher(id={self.id}, name={self.name})"


class Book(Base):
    __tablename__ =  'books'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publishers.id"), nullable=False)
    publisher = relationship("Publisher", backref="books")


class Shop(Base):
    __tablename__ =  'shops'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, unique=True)
    def __repr__(self):
        return f"Shop(id={self.id}, name={self.name})"


class Stock(Base):
    __tablename__ = 'stocks'
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("books.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shops.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    book = relationship("Book", backref="stocks")
    shop = relationship("Shop", backref="stocks")
    sales = relationship("Sale", backref="stock")


class Sale(Base):
    __tablename__ = 'sales'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stocks.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)


def create_tables(engine):
    Base.metadata.create_all(engine)
