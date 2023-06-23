from sqlalchemy import and_, delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.models.hotel import Hotel


async def delete_from_db(
    user_id: int, hotel_name: str, session_maker: async_sessionmaker
) -> None:
    """Delete a hotel from the database for a given user.

    Args:
        user_id (int): The ID of the user who owns the hotel.
        hotel_name (str): The name of the hotel to delete.
        session_maker (async_sessionmaker): An async session maker object used to create a new
            database session.

    Returns:
        None
    """
    async with session_maker() as session:
        async with session.begin():
            delete_query = delete(Hotel).where(
                and_(Hotel.id_user == user_id, Hotel.hotel_name == hotel_name)
            )
            await session.execute(delete_query)
