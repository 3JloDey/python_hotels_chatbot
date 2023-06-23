from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.models.hotel import Hotel


async def upload_hotels_from_db(
    user_id: int, session_maker: async_sessionmaker
) -> list[dict[str, Any]]:
    """Retrieves a list of hotels from the database for a given user.

    Args:
        user_id (int): The ID of the user whose hotels should be retrieved.
        session_maker (async_sessionmaker): An async session maker object used to create a new
            database session.

    Returns:
        list[dict[str, Any]]: A list of dictionaries, where each dictionary represents a hotel and
            contains the following keys: "hotel_name", "address", "rating", "users_rating",
            "price", "about", "around", "photos", "latitude", and "longitude". The "photos" key
            contains a list of tuples, where each tuple contains a photo URL and its description.
    """
    async with session_maker() as session:
        async with session.begin():
            stmt = select(Hotel).where(Hotel.id_user == user_id)
            result = await session.execute(stmt)
            hotels = result.scalars().all()

            data = []
            for hotel in hotels:
                data.append(
                    {
                        "hotel_name": hotel.hotel_name,
                        "address": hotel.address,
                        "rating": hotel.rating,
                        "users_rating": hotel.users_rating,
                        "price": hotel.price,
                        "about": hotel.about,
                        "around": hotel.around,
                        "photos": list(zip(hotel.photos_url, hotel.photos_description)),
                        "latitude": float(hotel.latitude),
                        "longitude": float(hotel.longitude),
                    }
                )
            return data
