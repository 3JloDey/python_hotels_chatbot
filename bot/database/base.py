from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(DeclarativeBase, AsyncAttrs):
    """A base class for declarative models that can be used with asynchronous database operations.
    
    This class inherits from both `DeclarativeBase` and `AsyncAttrs`, allowing it to be used with
    SQLAlchemy's ORM and async I/O features.
    """
    pass
