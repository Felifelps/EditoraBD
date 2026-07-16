from fastapi import Request
from psycopg import Connection


def get_conn(request: Request) -> Connection:
    with request.app.state.pool.connection() as conn:
        yield conn
