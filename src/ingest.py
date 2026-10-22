import duckdb
from pathlib import Path
import pandas as pd


class DuckDBStagingManager:
    def __init__(self, db_path: str = "brain_scan_staging.duckdb"):
        self.db_path = db_path

    def stage_dataset(self, dataset_id: str, dataset_path: Path):
        con = duckdb.connect(self.db_path)
        
        # Create staging schemas if not exist
        con.execute("""
            CREATE TABLE IF NOT EXISTS staging_datasets (
                dataset_id VARCHAR,
                ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR
            );
            CREATE TABLE IF NOT EXISTS staging_participants (
                dataset_id VARCHAR,
                participant_id VARCHAR,
                age DOUBLE,
                sex VARCHAR,
                handedness VARCHAR
            );
        """)

        # Load participants.tsv
        tsv_path = dataset_path / "participants.tsv"
        if tsv_path.exists():
            df = pd.read_csv(tsv_path, sep="\t")
            df.insert(0, "dataset_id", dataset_id)
            con.execute("INSERT INTO staging_participants SELECT * FROM df")

        # Log dataset staging status
        con.execute(
            "INSERT INTO staging_datasets (dataset_id, status) VALUES (?, ?)",
            [dataset_id, "VALIDATED_AND_STAGED"]
        )
        con.close()
        print(f"Dataset {dataset_id} successfully staged into DuckDB lakehouse.")