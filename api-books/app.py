from litestar import Litestar

from src.controller.user import UserController
from src.database.conn import db_connection, provide_transaction

app = Litestar(
    route_handlers=[UserController],
    lifespan=[db_connection],
    dependencies={"transaction": provide_transaction},
)
