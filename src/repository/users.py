from libgravatar import Gravatar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models import User
from src.schemas import UserModel

async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).filter_by(email=email))
    return result.scalars().first()

async def create_user(body: UserModel, db: AsyncSession):
    g = Gravatar(body.email)
    new_user = User(**body.model_dump(), avatar=g.get_image())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_token(user: User, refresh_token: str, db: AsyncSession):
    user.refresh_token = refresh_token
    await db.commit()
