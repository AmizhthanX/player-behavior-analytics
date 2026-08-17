"""
Step 5 - Data Cleaning
Cleans the three datasets produced by ingest.py.

Outputs:
    data/clean/clean_sessions.csv
    data/clean/clean_chat.csv
    data/clean/clean_blocks.csv

The column names follow the project report:
    sessions -> user, time, wid
    chat     -> user, message, time
    blocks   -> user, action, type, time
"""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
CLEAN_DIR = ROOT / "data" / "clean"


def require_columns(df: pd.DataFrame, columns: list[str], file_name: str) -> None:
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(
            f"{file_name} is missing required columns: {missing}. "
            f"Available columns: {list(df.columns)}"
        )


def clean_sessions() -> pd.DataFrame:
    path = RAW_DIR / "sessions.csv"
    df = pd.read_csv(path)

    require_columns(df, ["user", "time", "wid"], path.name)

    df = df.dropna(subset=["user", "time"])
    df = df.drop_duplicates()
    df = df[["user", "time", "wid"]]

    return df


def clean_chat() -> pd.DataFrame:
    path = RAW_DIR / "chat.csv"
    df = pd.read_csv(path)

    require_columns(df, ["user", "message", "time"], path.name)

    df = df.dropna(subset=["user", "message", "time"])
    df = df.drop_duplicates()
    df["message"] = df["message"].astype(str).str.strip()
    df = df[df["message"] != ""]
    df = df[["user", "message", "time"]]

    return df


def clean_blocks() -> pd.DataFrame:
    path = RAW_DIR / "blocks.csv"
    df = pd.read_csv(path)

    require_columns(df, ["user", "action", "type", "time"], path.name)

    df = df.dropna(subset=["user", "time"])
    df = df.drop_duplicates()
    df = df[["user", "action", "type", "time"]]

    return df


def main() -> None:
    required = [
        RAW_DIR / "sessions.csv",
        RAW_DIR / "chat.csv",
        RAW_DIR / "blocks.csv",
    ]

    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing raw datasets:\n" + "\n".join(missing) +
            "\nRun scripts/ingest.py first."
        )

    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    sessions = clean_sessions()
    chat = clean_chat()
    blocks = clean_blocks()

    sessions.to_csv(CLEAN_DIR / "clean_sessions.csv", index=False)
    chat.to_csv(CLEAN_DIR / "clean_chat.csv", index=False)
    blocks.to_csv(CLEAN_DIR / "clean_blocks.csv", index=False)

    print("Data Cleaning Completed!")
    print(f"Clean sessions: {len(sessions):,}")
    print(f"Clean chat:     {len(chat):,}")
    print(f"Clean blocks:   {len(blocks):,}")


if __name__ == "__main__":
    main()
