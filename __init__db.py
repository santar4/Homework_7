import asyncio
from passlib.hash import bcrypt

from werkzeug.security import generate_password_hash

from settings import Base, async_session, engine
from schemas import UserRegistration
from models import User


async def create_bd():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_data():
    async with async_session() as sess:
        u1 = User(
            first_name="Іван",
            last_name="Іванов",
            email="ivanov@example.com",
            password=generate_password_hash("usff"),
            phone="+380501234567"

        )
        u2 = User(
            first_name="Марія",
            last_name="Петренко",
            email="maria.petrenko@example.com",
            password_hash=generate_password_hash("user"),
            phone="+380671112233"
        )

        sess.add_all([u1, u2])
        await sess.commit()


async def main():
    await create_bd()
    print("database created")
    await insert_data()
    print("data added")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
