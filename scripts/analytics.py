"""
Steps 7-9 - Behavior Analytics, Churn Prediction and Final Dataset

Player classification thresholds from the project report:
    >= 150 -> Highly Active
    >= 80  -> Active
    >= 30  -> Casual
    < 30   -> Inactive

Churn prediction rules from the report/code:
    session_count < 2 AND engagement_score < 20 -> High Risk
    engagement_score < 50                         -> Medium Risk
    otherwise                                     -> Low Risk

Output:
    data/output/final_analytics.csv
"""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "data" / "output"


def classify_player(score: float) -> str:
    if score >= 150:
        return "Highly Active"
    elif score >= 80:
        return "Active"
    elif score >= 30:
        return "Casual"
    return "Inactive"


def predict_churn(row: pd.Series) -> str:
    if (
        row["session_count"] < 2
        and row["engagement_score"] < 20
    ):
        return "High Risk"

    if row["engagement_score"] < 50:
        return "Medium Risk"

    return "Low Risk"


def add_peak_activity_info(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds optional hourly activity information when timestamps are available.

    This does not change the report's player-level churn rules.
    It simply makes the final dataset more useful for Power BI.
    """
    sessions_path = ROOT / "data" / "clean" / "clean_sessions.csv"

    if not sessions_path.exists():
        return df

    sessions = pd.read_csv(sessions_path)

    if "time" not in sessions.columns:
        return df

    timestamps = pd.to_datetime(sessions["time"], errors="coerce")
    valid = timestamps.dropna()

    if valid.empty:
        return df

    hourly_counts = valid.dt.hour.value_counts().sort_index()

    if hourly_counts.empty:
        return df

    peak_hour = int(hourly_counts.idxmax())
    df["peak_server_activity_hour"] = peak_hour

    return df


def main() -> None:
    input_file = OUTPUT_DIR / "player_metrics.csv"

    if not input_file.exists():
        raise FileNotFoundError(
            f"{input_file} not found. Run scripts/transform.py first."
        )

    df = pd.read_csv(input_file)

    required = [
        "user",
        "session_count",
        "chat_count",
        "block_activity",
        "engagement_score",
        "rage_quit_flag",
    ]

    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"player_metrics.csv is missing: {missing}")

    df["player_type"] = df["engagement_score"].apply(classify_player)
    df["churn_risk"] = df.apply(predict_churn, axis=1)

    df = add_peak_activity_info(df)

    output = OUTPUT_DIR / "final_analytics.csv"
    df.to_csv(output, index=False)

    print("\n===== PLAYER ANALYTICS =====\n")
    print(df.head())

    print("\nMost Active Players:")
    print(
        df.sort_values(
            by="engagement_score",
            ascending=False,
        )[["user", "engagement_score", "player_type"]].head(5)
    )

    print("\nHigh Churn Risk Players:")
    print(
        df[df["churn_risk"] == "High Risk"][
            ["user", "churn_risk"]
        ]
    )

    print(f"\nFinal analytics saved to: {output}")
    print("Analytics Completed!")


if __name__ == "__main__":
    main()
