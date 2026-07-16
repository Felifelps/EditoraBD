from pathlib import Path

from psycopg_pool import ConnectionPool

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent.parent / "migrations"


def run_migrations(pool: ConnectionPool, migrations_dir: Path = MIGRATIONS_DIR) -> None:
    with pool.connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                filename   VARCHAR(255) PRIMARY KEY,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        )
        applied = {row[0] for row in conn.execute("SELECT filename FROM schema_migrations").fetchall()}

        for path in sorted(migrations_dir.glob("*.sql")):
            if path.name in applied:
                continue
            with conn.transaction():
                conn.execute(path.read_text())
                conn.execute(
                    "INSERT INTO schema_migrations (filename) VALUES (%s)", (path.name,)
                )
