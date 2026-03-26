from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "postgresql+asyncpg://admin:admin@localhost:5432/python_db"

# Engine async
engine = create_async_engine(
    DATABASE_URL,
    echo=True,        # Log SQL dans console
    future=True,
)

# Session async
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
