import json
import subprocess
from pathlib import Path
import pandas as pd
from src.models import ParticipantRecord, DatasetDescription


class BIDSValidatorEngine:
    def __init__(self, dataset_path: Path):
        self.dataset_path = Path(dataset_path)
        self.errors = []

    def run_bids_validator_cli(self) -> bool:
        """Runs the official JavaScript/Node bids-validator CLI container or tool."""
        try:
            # Assumes bids-validator is installed in the container environment
            result = subprocess.run(
                ["bids-validator", str(self.dataset_path), "--json"],
                capture_output=True,
                text=True,
                check=False
            )
            output = json.loads(result.stdout)
            if output.get("issues", {}).get("total", 0) > 0:
                self.errors.append(f"BIDS Validator structural issues found: {output['issues']}")
                return False
            return True
        except Exception as e:
            self.errors.append(f"Failed to execute bids-validator CLI: {str(e)}")
            return False

    def validate_participants_tsv(self) -> bool:
        """Validates participants.tsv using Pydantic v2 models row-by-row."""
        tsv_path = self.dataset_path / "participants.tsv"
        if not tsv_path.exists():
            self.errors.append("Missing mandatory 'participants.tsv' file at dataset root.")
            return False

        try:
            df = pd.read_csv(tsv_path, sep="\t")
            for idx, row in df.iterrows():
                try:
                    ParticipantRecord(**row.to_dict())
                except Exception as val_err:
                    self.errors.append(f"Row {idx + 1} validation error: {val_err}")
            return len(self.errors) == 0
        except Exception as e:
            self.errors.append(f"Failed to parse participants.tsv: {str(e)}")
            return False

    def execute_validation_suite(self) -> tuple[bool, list[str]]:
        bids_pass = self.run_bids_validator_cli()
        tsv_pass = self.validate_participants_tsv()
        is_valid = bids_pass and tsv_pass
        return is_valid, self.errors