from litestar import Controller, delete, get, patch, post, put
from litestar.dto import DTOData
from litestar.exceptions import HTTPException
from pydantic import UUID4

from src.model.dto import PartialUserDTO, User
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(self, data: User, transaction: AsyncSession) -> User:
        transaction.add(data)
        return data

    # async def add_item(data: TodoType, transaction: AsyncSession) -> TodoType:
    #     new_todo = TodoItem(title=data["title"], done=data["done"])
    #     transaction.add(new_todo)
    #     return serialize_todo(new_todo)

    @get()
    async def list_users(self) -> list[User]:
        return None

    @patch(path="/{user_id:uuid}", dto=PartialUserDTO)
    async def partial_update_user(self, user_id: UUID4, data: DTOData[User]) -> User:
        pass

    @put(path="/{user_id:uuid}")
    async def update_user(self, user_id: UUID4, data: User) -> User:
        pass

    @get(path="/{user_id:uuid}")
    async def get_user(self, user_id: UUID4) -> User:
        pass

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4) -> None:
        pass
