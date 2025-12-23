from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Mapping, Sequence, Any


def connect_sqlite(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=FULL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def connect_duckdb(path: Path):
    try:
        import duckdb
    except Exception as e:
        raise RuntimeError("duckdb_not_available") from e
    return duckdb.connect(str(path))


def execute_sql(conn: Any, sql: str) -> None:
    parts = [p.strip() for p in sql.split(";")]
    for p in parts:
        if p:
            conn.execute(p)


def execute_sql_file(conn: Any, path: Path) -> None:
    execute_sql(conn, path.read_text(encoding="utf-8"))


def create_table(conn: Any, name: str, columns: Sequence[str]) -> None:
    cols = ", ".join(columns)
    conn.execute(f"CREATE TABLE IF NOT EXISTS {name} ({cols});")


def insert_many(conn: Any, name: str, rows: Iterable[Mapping[str, object]]) -> int:
    rows_list = list(rows)
    if not rows_list:
        return 0
    keys = list(rows_list[0].keys())
    placeholders = ",".join(["?"] * len(keys))
    sql = f"INSERT INTO {name} ({','.join(keys)}) VALUES ({placeholders});"
    conn.executemany(sql, [[r.get(k) for k in keys] for r in rows_list])
    return len(rows_list)
