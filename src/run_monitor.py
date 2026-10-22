import hashlib
from pathlib import Path
import duckdb


class IntegrityAuditor:
    def __init__(self, repo_root: Path, db_path: str = "brain_scan_staging.duckdb"):
        self.repository_root = Path(repo_root)
        self.db_path = db_path

    @staticmethod
    def compute_sha256(file_path: Path, chunk_size: int = 8192) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def audit_directory(self, dataset_id: str) -> dict:
        """Audits file integrity across a dataset directory and logs results."""
        con = duckdb.connect(self.db_path)
        con.execute("""
            CREATE TABLE IF NOT EXISTS audit_integrity_logs (
                dataset_id VARCHAR,
                file_path VARCHAR,
                sha256_checksum VARCHAR,
                file_size_bytes BIGINT,
                audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR
            );
        """)

        audit_summary = {"total_files": 0, "passed": 0, "failed": 0}
        
        # Scan target dataset path
        target_path = self.repository_root / dataset_id
        if not target_path.exists():
            raise FileNotFoundError(f"Dataset path {target_path} does not exist.")

        for file_path in target_path.rglob("*"):
            if file_path.is_file():
                audit_summary["total_files"] += 1
                try:
                    file_size = file_path.stat().st_size
                    checksum = self.compute_sha256(file_path)
                    
                    con.execute(
                        "INSERT INTO audit_integrity_logs (dataset_id, file_path, sha256_checksum, file_size_bytes, status) VALUES (?, ?, ?, ?, ?)",
                        [dataset_id, str(file_path.relative_to(self.repository_root)), checksum, file_size, "OK"]
                    )
                    audit_summary["passed"] += 1
                except Exception as e:
                    audit_summary["failed"] += 1
                    con.execute(
                        "INSERT INTO audit_integrity_logs (dataset_id, file_path, sha256_checksum, file_size_bytes, status) VALUES (?, ?, ?, ?, ?)",
                        [dataset_id, str(file_path.relative_to(self.repository_root)), "ERROR", 0, f"FAILED: {str(e)}"]
                    )

        con.close()
        return audit_summary