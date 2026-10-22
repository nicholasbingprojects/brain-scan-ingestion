from pathlib import Path
import nibabel as nib
import duckdb


class NIfTIQualityAuditor:
    def __init__(self, db_path: str = "brain_scan_staging.duckdb"):
        self.db_path = db_path

    def audit_nifti_headers(self, dataset_id: str, dataset_path: Path) -> list:
        con = duckdb.connect(self.db_path)
        con.execute("""
            CREATE TABLE IF NOT EXISTS audit_nifti_quality (
                dataset_id VARCHAR,
                file_name VARCHAR,
                dimensions VARCHAR,
                voxel_sizes VARCHAR,
                data_type VARCHAR,
                status VARCHAR,
                error_message VARCHAR,
                audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        issues = []
        nii_files = list(Path(dataset_path).rglob("*.nii*"))

        for file_path in nii_files:
            try:
                img = nib.load(str(file_path))
                shape = str(img.shape)
                zooms = str(img.header.get_zooms())
                dtype = str(img.get_data_dtype())

                con.execute(
                    "INSERT INTO audit_nifti_quality (dataset_id, file_name, dimensions, voxel_sizes, data_type, status) VALUES (?, ?, ?, ?, ?, ?)",
                    [dataset_id, file_path.name, shape, zooms, dtype, "VALID"]
                )
            except Exception as e:
                err_msg = str(e)
                issues.append((file_path.name, err_msg))
                con.execute(
                    "INSERT INTO audit_nifti_quality (dataset_id, file_name, dimensions, voxel_sizes, data_type, status, error_message) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [dataset_id, file_path.name, "N/A", "N/A", "N/A", "CORRUPT", err_msg]
                )

        con.close()
        return issues