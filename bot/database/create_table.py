from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base

# Создаем объект engine для подключения к базе данных
engine = create_engine('postgresql://postgres:qwepoi99@localhost/postgres')
# Создаем базовый класс моделей
Base = declarative_base()


# Определяем модель для таблицы
class Hotel(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True, autoincrement='auto')
    id_user = Column(Integer, nullable=False)
    hotel_name = Column(String(100))
    address = Column(String(100))
    rating = Column(String(20))
    users_rating = Column(String(20))
    price = Column(Text)
    about = Column(Text)
    around = Column(Text)
    photos_url = Column(ARRAY(Text))
    photos_description = Column(ARRAY(Text))
    latitude = Column(Float)
    longitude = Column(Float)


# Создаем таблицу
Base.metadata.create_all(engine)
