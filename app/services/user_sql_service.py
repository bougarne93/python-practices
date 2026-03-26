from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import async_session
from app.models.user_sql import UserSQL
from app.models.user import User, UserUpdate
from app.security.password import hash_password
from app.security.password import verify_password

class UserSQLService:

    @staticmethod
    async def create_user(data: User):
        async with async_session() as session:
            user = UserSQL(id=data.id, name=data.name, email=data.email)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def get_user(user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(UserSQL).where(UserSQL.id == user_id)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def get_all_users():
        async with async_session() as session:
            result = await session.execute(select(UserSQL))
            return result.scalars().all()

    @staticmethod
    async def update_user(user_id: int, data: UserUpdate):
        async with async_session() as session:
            # Récupérer l’utilisateur
            result = await session.execute(
                select(UserSQL).where(UserSQL.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                return None

            # UPDATE PARTIEL : mettre à jour uniquement ce qui est envoyé
            if data.name is not None:
                user.name = data.name

            if data.email is not None:
                user.email = data.email

            # Sauvegarde
            await session.commit()
            await session.refresh(user)

            return user

    @staticmethod
    async def delete_user(user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(UserSQL).where(UserSQL.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                return None

            await session.delete(user)
            await session.commit()
            return True
    @staticmethod
    async def register_user(data):
        async with async_session() as session:
            user = UserSQL(
                name=data.name,
                email=data.email,
                password_hash=hash_password(data.password)
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def authenticate(email: str, password: str):
        async with async_session() as session:
            result = await session.execute(
                select(UserSQL).where(UserSQL.email == email)
            )
            user = result.scalar_one_or_none()

            if not user:
                return None

            if not verify_password(password, user.password_hash):
                return None

            return user