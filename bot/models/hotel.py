from sqlalchemy import ARRAY, Column, Float, Integer, String, Text
from bot.database.base import Base


class Hotel(Base):
    __tablename__ = "favorite_hotels"
    pk = Column(Integer, primary_key=True, autoincrement='auto')
    id_user = Column(Integer, nullable=False)
    hotel_name = Column(String(100))
    address = Column(String(100))
    rating = Column(String(20), nullable=True)
    users_rating = Column(String(20))
    price = Column(Text, nullable=True)
    about = Column(Text, nullable=True)
    around = Column(Text, nullable=True)
    photos_url = Column(ARRAY(Text))
    photos_description = Column(ARRAY(Text))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
