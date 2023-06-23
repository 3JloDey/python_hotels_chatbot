from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.models.hotel import Hotel


async def select_hotels(user_id: int, session_maker: async_sessionmaker) -> list[dict[str, Any]]:
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
