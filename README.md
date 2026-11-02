# brain-scan-ingestion
The BRAIN-SCAN Data Management & Analytics Platform is a production-grade, open-source data ingestion, validation, and analytics pipeline built for neuroimaging research. Engineered to address rigorous Brain Imaging Data Structure (BIDS) standards, this platform automates the ingestion, cryptographic auditing, quality control (QA/QC), and lakehouse staging of 3D neuroimaging datasets (NIfTI format).

Designed with modern data engineering principles, it bridges raw clinical scans with cloud-scale distributed compute architectures using Python (Pydantic v2), DuckDB, Nextflow (DSL2), and Seqera Platform.

Architecture & System Workflow

[ Raw NIfTI Scans / BIDS Directory ]
               │
               ▼
   ┌───────────────────────┐
   │ Pydantic v2 Validator │  ──► Parses dataset_description.json & participants.tsv
   └───────────────────────┘
               │
               ▼
   ┌───────────────────────┐
   │ SHA-256 Crypto Audit  │  ──► Detects bit-rot, file corruption & header discrepancies
   └───────────────────────┘
               │
               ▼
   ┌───────────────────────┐
   │ Nibabel Inspection    │  ──► Audits voxel dimensions, orientations & data types
   └───────────────────────┘
               │
               ▼
   ┌───────────────────────┐
   │ DuckDB Lakehouse      │  ──► Staging, indexing & relational querying
   └───────────────────────┘
               │
               ▼
   ┌───────────────────────┐
   │ Nextflow DSL2 Workflow│  ──► Containerized feature extraction on AWS Batch via Seqera Platform
   └───────────────────────┘


Core Technical Modules

1. BIDS Ingestion & Validation Engine (validator.py)

Framework: Python, Pydantic v2, Regular Expressions.

Functionality: Parses structural metadata files (dataset_description.json, participants.tsv, and scan sidecars) against strict BIDS schema boundaries. Ensures required participant demographic variables and modality directories are correctly structured prior to pipeline execution.

2. Repository Integrity & Quality Audit Framework (auditor.py)

Framework: Python, Cryptography (SHA-256), Nibabel.

Functionality:

Computes cryptographic SHA-256 file hashes across incoming imaging sessions to guarantee immutability and track data lineage.

Utilizes nibabel to inspect header metadata, catching orientation anomalies, out-of-bound voxel dimensions, and slice-timing discrepancies before staging data into analytics storage.

3. DuckDB Staging Lakehouse (lakehouse.sql / loader.py)

Framework: DuckDB, SQL, Pandas.

Functionality: Ingests validated BIDS clinical tabular data and extracted neuroimaging metrics into an embedded, high-performance columnar DuckDB lakehouse. Enables fast, SQL-based cohort filtering and cross-modal data queries.

4. Scalable Nextflow Feature Extraction Workflow (main.nf)

Framework: Nextflow (DSL2), Docker, Seqera Platform CLI (tw), AWS Batch.

Functionality: Modularized workflow that spins up containerized Docker environments to compute volumetric brain metrics and intensity feature distributions from 3D NIfTI volumes in parallel across elastic AWS Batch compute instances.

Tech Stack

Programming & Scripting: Python 3.11+, SQL, Bash / Unix Shell

Data Validation & Modeling: Pydantic v2, Pandas, NumPy

Neuroimaging Libraries: Nibabel, BIDS Standard Specifications

Data Architecture: DuckDB Lakehouse

Workflow Orchestration & Cloud: Nextflow DSL2, Docker, Seqera Platform (Tower), AWS Batch

Version Control & CI/CD: Git, GitHub Actions

Getting Started / Installation

Clone the Repository:

git clone https://github.com/nicholasbingprojects/brain-scan-ingestion.git
cd brain-scan-ingestion


Set Up Python Virtual Environment:

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt


Run BIDS Validation Script:

python src/validator.py --dataset_dir /path/to/bids/dataset


Execute Nextflow Pipeline Locally:

nextflow run main.nf -profile docker
