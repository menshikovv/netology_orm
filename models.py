import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Модель данных для магазинов
class Shop(Base):
    __tablename__ = 'shops'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, unique=True)

    def __repr__(self):
        return f"Shop(id={self.id}, name={self.name})"

# Модель данных для запасов книг в магазинах
class Stock(Base):
    __tablename__ = 'stocks'
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("books.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shops.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    book = relationship("Book", back_populates="stocks")
    shop = relationship("Shop", back_populates="stocks")
    sales = relationship("Sale", back_populates="stock")

# Модель данных для фактов продажи
class Sale(Base):
    __tablename__ = 'sales'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stocks.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

# Создаем соединение с базой данных (здесь используется SQLite в памяти)
engine = sq.create_engine('sqlite:///:memory:')

# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
db_session = Session()

# Функция для получения информации о продажах
def get_sales(publisher_id_or_name):
    if publisher_id_or_name.isdigit():
        sales = db_session.query(
            Book.title,
            Shop.name,
            Sale.price,
            Sale.date_sale
        ).join(
            (Stock, Stock.id_book == Book.id),
            (Sale, Sale.id_stock == Stock.id)
        ).filter(
            Stock.id_shop == Shop.id,
            Book.publisher_id == int(publisher_id_or_name)
        ).all()
    else:
        sales = db_session.query(
            Book.title,
            Shop.name,
            Sale.price,
            Sale.date_sale
        ).join(
            (Stock, Stock.id_book == Book.id),
            (Sale, Sale.id_stock == Stock.id)
        ).filter(
            Stock.id_shop == Shop.id,
            Book.publisher.has(Publisher.name == publisher_id_or_name)
        ).all()

    print(f"{'Название книги': <40} | {'Название магазина': <10} | {'Стоимость продажи': <8} | {'Дата продажи'}")
    for title, shop, price, date_sale in sales:
        print(f"{title: <40} | {shop: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}")

if __name__ == '__main__':
    publisher_id_or_name = input("Введите ID издателя или его имя: ")
    get_sales(publisher_id_or_name)
