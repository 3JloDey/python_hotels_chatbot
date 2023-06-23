from sqlalchemy import ARRAY, Column, Float, Integer, String, Text
from bot.database.base import Base


class Hotel(Base):
    """
    Represents a favorite hotel.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        pk (int): The primary key of the hotel.
        id_user (int): The ID of the user who favorited the hotel.
        hotel_name (str): The name of the hotel.
        address (str): The address of the hotel.
        rating (str): The rating of the hotel.
        users_rating (str): The rating given by the user.
        price (str): The price of the hotel.
        about (str): Information about the hotel.
        around (str): Information about the surrounding area.
        photos_url (list): URLs of photos of the hotel.
        photos_description (list): Descriptions of the photos.
        latitude (float): The latitude of the hotel's location.
        longitude (float): The longitude of the hotel's location.
    """
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
