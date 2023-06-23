from sqlalchemy import URL, MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

def async_engine_create(url: URL | str) -> AsyncEngine:
    """Creates an asynchronous engine instance.
    
    Args:
    - url (URL or str): database connection URL
    
    Returns:
    - AsyncEngine: the created asynchronous engine instance
    """
    return create_async_engine(url=url, pool_pre_ping=True)


async def proceed_schemas(engine: AsyncEngine, metadata: MetaData) -> None:
    """Creates all tables in the database for the given metadata object.
    
    Args:
    - engine (AsyncEngine): asynchronous engine instance to use for creating tables
    - metadata (MetaData): metadata object containing table definitions
    """
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
