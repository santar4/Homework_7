import uvicorn
from fastapi import FastAPI, HTTPException, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from werkzeug.security import generate_password_hash

from models import User
from schemas import UserRegistration
from sqlalchemy import select

from settings import async_session, get_session

app = FastAPI()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.post("/register")
async def register_user(user: UserRegistration, db: AsyncSession = Depends(get_session)):
    stmt = select(User).filter_by(email=user.email, password=user.password)
    user = await db.scalar(stmt)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is exists")
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=generate_password_hash(user.password),
        phone=user.phone,
        create_date=user.create_date
    )
    db.add(new_user)
    await db.commit()

    return {"message": "Користувача успішно зареєстровано"}


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
