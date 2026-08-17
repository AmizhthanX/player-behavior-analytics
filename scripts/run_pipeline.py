"""
Complete ETL pipeline runner.

Run this file after placing the CoreProtect database at:
    plugins/CoreProtect/database.db

Pipeline:
    1. Ingest SQLite -> CSV
    2. Clean raw CSVs
    3. Transform into player metrics
    4. Classify player behavior and predict churn
"""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"


def run(script_name: str) -> None:
    script = SCRIPTS_DIR / script_name

    print("\n" + "=" * 60)
    print(f"RUNNING: {script_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(
            f"\nPipeline stopped because {script_name} failed."
        )


def main() -> None:
    run("ingest.py")
    run("clean.py")
    run("transform.py")
    run("analytics.py")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("Final dataset:")
    print("data/output/final_analytics.csv")


if __name__ == "__main__":
    main()
