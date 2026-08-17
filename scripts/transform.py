"""
Step 6 - Data Transformation

Creates player-level metrics from cleaned datasets.

Metrics from the project report:
    session_count
    chat_count
    block_activity
    engagement_score
    rage_quit_flag

Engagement formula:
    (Session Count * 2) + (Chat Count * 1) + (Block Activity * 3)

Rage quit rule:
    session_count < 2

Output:
    data/output/player_metrics.csv
"""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CLEAN_DIR = ROOT / "data" / "clean"
OUTPUT_DIR = ROOT / "data" / "output"


def count_by_user(path: Path, metric_name: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    if "user" not in df.columns:
        raise ValueError(f"{path.name} must contain a 'user' column.")

    return df.groupby("user").size().reset_index(name=metric_name)


def main() -> None:
    session_count = count_by_user(
        CLEAN_DIR / "clean_sessions.csv",
        "session_count",
    )

    chat_count = count_by_user(
        CLEAN_DIR / "clean_chat.csv",
        "chat_count",
    )

    block_activity = count_by_user(
        CLEAN_DIR / "clean_blocks.csv",
        "block_activity",
    )

    player_metrics = session_count.merge(
        chat_count,
        on="user",
        how="outer",
    )

    player_metrics = player_metrics.merge(
        block_activity,
        on="user",
        how="outer",
    )

    player_metrics = player_metrics.fillna(0)

    numeric_columns = [
        "session_count",
        "chat_count",
        "block_activity",
    ]
    player_metrics[numeric_columns] = player_metrics[numeric_columns].astype(int)

    player_metrics["engagement_score"] = (
        player_metrics["session_count"] * 2
        + player_metrics["chat_count"] * 1
        + player_metrics["block_activity"] * 3
    )

    player_metrics["rage_quit_flag"] = (
        player_metrics["session_count"] < 2
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output = OUTPUT_DIR / "player_metrics.csv"
    player_metrics.to_csv(output, index=False)

    print("Transformation completed!")
    print(f"Players: {len(player_metrics):,}")
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
