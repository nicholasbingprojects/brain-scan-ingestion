A high-throughput ingestion pipeline designed to ingest, validate, anonymize, and store neuroimaging data (DICOM and NIfTI formats) for research and clinical analytics.

🚀 Key Features
Automated Ingestion: Watches cloud storage buckets (AWS S3 / GCS) or local endpoints for incoming neuroimaging archives.

DICOM Anonymization: Strips Patient Health Information (PHI) compliant with HIPAA and GDPR guidelines while preserving essential anatomical metadata.

Format Conversion: Automatically converts raw DICOM sequences into analysis-ready NIfTI (.nii.gz) formats using tools like dcm2niix.

Quality Control & Validation: Verifies file integrity, checks scan orientation, and ensures mandatory headers (e.g., TR, TE, voxel dimensions) are present.

Metadata Extraction: Extracts key DICOM tags and stores them in a structured PostgreSQL database for fast querying.

🛠️ Tech Stack
Language: Python 3.10+

Imaging Libraries: pydicom, Nibabel, dcm2niix

Storage/Database: PostgreSQL, AWS S3 / Google Cloud Storage

Orchestration: Docker / Kubernetes / Apache Airflow

Project Structure
