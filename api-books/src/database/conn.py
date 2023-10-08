from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar.exceptions import ClientException, NotFoundException
from litestar.status_codes import HTTP_409_CONFLICT

from litestar import Litestar
from litestar.datastructures import State
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from os import getenv


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    engine = getattr(app.state, "engine", None)
    if engine is None:
        engine = create_async_engine(
            f"postgresql+asyncpg://{getenv('POSTGRES_USER')}@postgres/{getenv('POSTGRES_DB')}",
            echo=True,
        )
        app.state.engine = engine

    try:
        yield
    finally:
        await engine.dispose()


sessionmaker = async_sessionmaker(expire_on_commit=False)


async def provide_transaction(state: State) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker(bind=state.engine) as session:
        try:
            async with session.begin():
                yield session
        except IntegrityError as exc:
            raise ClientException(
                status_code=HTTP_409_CONFLICT,
                detail=str(exc),
            ) from exc
