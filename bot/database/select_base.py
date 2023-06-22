from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.models.hotel import Hotel


async def get_hotels_by_user_id(user_id: int, session_maker: async_sessionmaker):
    async with session_maker() as session:
        stmt = select(Hotel).where(Hotel.id_user == user_id)
        result = await session.execute(stmt)
        hotels = result.scalars().all()
        for hotel in hotels:
            print(hotel.hotel_name)
