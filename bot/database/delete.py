from sqlalchemy import and_, delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.models.hotel import Hotel


async def delete_hotels(user_id: int, hotel_name: str, session_maker: async_sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            stmt = delete(Hotel).where(
                and_(Hotel.id_user == user_id, Hotel.hotel_name == hotel_name)
            )
            await session.execute(stmt)
