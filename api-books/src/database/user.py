from typing import Any
from uuid import UUID

from litestar.exceptions import NotFoundException
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

UserType = dict[str, Any]
UserCollectionType = list[UserType]


class Base(DeclarativeBase):
    first_name: str
    last_name: str
    id: UUID


class User(Base):
    __tablename__ = "user"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]


def serialize_todo(u: User) -> UserType:
    return {"first_name": u.first_name, "last_name": u.last_name, "id": u.id}


# async def get_todo_by_title(todo_name, session: AsyncSession) -> UserType:
#     query = select(UserType).where(UserType.title == todo_name)
#     result = await session.execute(query)
#     try:
#         return result.scalar_one()
#     except NoResultFound as e:
#         raise NotFoundException(detail=f"TODO {todo_name!r} not found") from e


# async def get_todo_list(done: bool | None, session: AsyncSession) -> list[UserType]:
#     query = select(UserType)
#     if done is not None:
#         query = query.where(UserType.done.is_(done))

#     result = await session.execute(query)
#     return result.scalars().all()
