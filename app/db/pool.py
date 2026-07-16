from psycopg_pool import ConnectionPool

from app.config import Settings


def build_pool(settings: Settings) -> ConnectionPool:
    return ConnectionPool(
        conninfo=settings.database_url,
        min_size=2,
        max_size=10,
        open=False,
    )
