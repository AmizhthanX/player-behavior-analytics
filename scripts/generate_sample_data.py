"""
Optional development/demo data generator.

Use this only when the real CoreProtect database is unavailable.
It creates realistic-looking raw CSV files with the same columns expected
by the ETL pipeline.

Output:
    data/raw/sessions.csv
    data/raw/chat.csv
    data/raw/blocks.csv

This is useful for testing the GitHub project and Power BI dashboard.
"""

from pathlib import Path
from datetime import datetime, timedelta
import random
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"

random.seed(42)

PLAYERS = [f"Player{i:03d}" for i in range(1, 101)]

CHAT_MESSAGES = [
    "hello",
    "hi everyone",
    "anyone want to play?",
    "nice build",
    "where is the base?",
    "good game",
    "thanks",
    "lets explore",
]

BLOCK_TYPES = [
    "STONE",
    "DIRT",
    "WOOD",
    "COBBLESTONE",
    "GLASS",
    "SAND",
    "IRON_ORE",
    "COAL_ORE",
]


def random_time(start: datetime, days: int = 30) -> datetime:
    return start + timedelta(
        days=random.randint(0, days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )


def generate() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    start = datetime(2026, 7, 1)

    sessions = []
    chats = []
    blocks = []

    for player in PLAYERS:
        # Some players are deliberately less active to produce
        # different player types and churn-risk categories.
        activity = random.choices(
            ["low", "medium", "high"],
            weights=[20, 50, 30],
            k=1,
        )[0]

        if activity == "low":
            session_count = random.randint(1, 3)
            chat_count = random.randint(0, 5)
            block_count = random.randint(0, 8)
        elif activity == "medium":
            session_count = random.randint(4, 15)
            chat_count = random.randint(3, 25)
            block_count = random.randint(10, 80)
        else:
            session_count = random.randint(15, 35)
            chat_count = random.randint(10, 60)
            block_count = random.randint(50, 250)

        for session_number in range(session_count):
            login_time = random_time(start)
            logout_time = login_time + timedelta(
                minutes=random.randint(10, 180)
            )

            sessions.append({
                "user": player,
                "time": login_time.strftime("%Y-%m-%d %H:%M:%S"),
                "wid": 1,
            })

            sessions.append({
                "user": player,
                "time": logout_time.strftime("%Y-%m-%d %H:%M:%S"),
                "wid": 1,
            })

        for _ in range(chat_count):
            chats.append({
                "user": player,
                "message": random.choice(CHAT_MESSAGES),
                "time": random_time(start).strftime("%Y-%m-%d %H:%M:%S"),
            })

        for _ in range(block_count):
            blocks.append({
                "user": player,
                "action": random.choice(["break", "place"]),
                "type": random.choice(BLOCK_TYPES),
                "time": random_time(start).strftime("%Y-%m-%d %H:%M:%S"),
            })

    pd.DataFrame(sessions).to_csv(
        RAW_DIR / "sessions.csv",
        index=False,
    )
    pd.DataFrame(chats).to_csv(
        RAW_DIR / "chat.csv",
        index=False,
    )
    pd.DataFrame(blocks).to_csv(
        RAW_DIR / "blocks.csv",
        index=False,
    )

    print("Sample datasets generated successfully.")
    print(f"Players: {len(PLAYERS)}")
    print(f"Sessions rows: {len(sessions):,}")
    print(f"Chat rows: {len(chats):,}")
    print(f"Block rows: {len(blocks):,}")


if __name__ == "__main__":
    generate()
