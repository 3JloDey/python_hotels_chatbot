from sqlalchemy import delete, and_
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.models.hotel import Hotel


async def delete_hotels_by_user_id(user_id: int, hotel_name: str, session_maker: async_sessionmaker):
    async with session_maker() as session:
        stmt = delete(Hotel).where(
            and_(Hotel.id_user == user_id, Hotel.hotel_name == hotel_name)
        )
        await session.execute(stmt)
        await session.commit()
