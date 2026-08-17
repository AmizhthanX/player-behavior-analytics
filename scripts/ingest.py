"""
Step 4 - Data Ingestion
Extracts CoreProtect SQLite tables into CSV files.

Expected CoreProtect database:
    plugins/CoreProtect/database.db

Outputs:
    data/raw/sessions.csv
    data/raw/chat.csv
    data/raw/blocks.csv

The table names are based on the project report:
    co_session
    co_chat
    co_block
"""

from pathlib import Path
import sqlite3
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "plugins" / "CoreProtect" / "database.db"
RAW_DIR = ROOT / "data" / "raw"


def table_exists(connection, table_name: str) -> bool:
    query = """
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=?
    """
    return connection.execute(query, (table_name,)).fetchone() is not None


def extract_table(connection, table_name: str, output_file: Path) -> pd.DataFrame:
    if not table_exists(connection, table_name):
        raise RuntimeError(
            f"Required CoreProtect table '{table_name}' was not found in the database."
        )

    df = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"{table_name}: {len(df):,} rows -> {output_file}")
    return df


def main(db_path: Path = DEFAULT_DB) -> None:
    if not db_path.exists():
        raise FileNotFoundError(
            f"CoreProtect database not found: {db_path}\n"
            "Place database.db at plugins/CoreProtect/database.db "
            "or change DEFAULT_DB in this file."
        )

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        extract_table(connection, "co_session", RAW_DIR / "sessions.csv")
        extract_table(connection, "co_chat", RAW_DIR / "chat.csv")
        extract_table(connection, "co_block", RAW_DIR / "blocks.csv")

    print("\nData ingestion completed successfully.")


if __name__ == "__main__":
    main()
