from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Favorite(Base):
    __tablename__ = "favorites_hotel"
