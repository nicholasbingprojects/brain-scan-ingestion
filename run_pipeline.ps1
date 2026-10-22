<#
.SYNOPSIS
    BRAIN-SCAN Dataset Ingestion and Validation Pipeline Runner for Windows PowerShell.
.DESCRIPTION
    Automates dependency checks, virtual environment setup, and execution of the 
    BIDS validation and DuckDB staging pipeline on Windows.
.PARAMETER DatasetPath
    Path to the root of the neuroimaging dataset to validate and stage.
.PARAMETER DatasetId
    Unique identifier for the dataset (e.g., BRAIN_SCAN_COHORT_01).
.EXAMPLE
    .\run_pipeline.ps1 -DatasetPath "C:\Data\brain_scan_sample" -DatasetId "COHORT_001"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$DatasetPath,

    [Parameter(Mandatory=$true)]
    [string]$DatasetId
)

# Clear screen header
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " BRAIN-SCAN Ingestion & Validation Pipeline (Win)" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Check Python availability
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not found in system PATH."
    exit 1
}

# 2. Check Node.js / bids-validator availability
if (-not (Get-Command bids-validator -ErrorAction SilentlyContinue)) {
    Write-Warning "bids-validator CLI not found globally. Checking npm..."
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
        Write-Error "Node.js and npm are required to run bids-validator. Please install Node.js."
        exit 1
    } else {
        Write-Host "Installing bids-validator globally via npm..." -ForegroundColor Yellow
        npm install -g bids-validator
    }
}

# 3. Setup Python virtual environment if not present
$VenvDir = ".venv"
if (-not (Test-Path $VenvDir)) {
    Write-Host "Creating Python virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv $VenvDir
}

# Activate virtual environment in PowerShell
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$ActivateScript = Join-Path $VenvDir "Scripts/Activate.ps1"
if (Test-Path $ActivateScript) {
    . $ActivateScript
} else {
    Write-Error "Virtual environment activation script not found at $ActivateScript"
    exit 1
}

# 4. Install Python requirements
if (Test-Path "requirements.txt") {
    Write-Host "Installing/updating Python dependencies..." -ForegroundColor Yellow
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
} else {
    Write-Error "requirements.txt not found in the current directory."
    exit 1
}

# 5. Execute the Python pipeline orchestration script
Write-Host "Executing pipeline for Dataset ID: [$DatasetId]..." -ForegroundColor Green
python run_pipeline.py --dataset-path "$DatasetPath" --dataset-id "$DatasetId"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Pipeline completed successfully!" -ForegroundColor Green
} else {
    Write-Error "Pipeline execution failed with exit code $LASTEXITCODE."
    exit $LASTEXITCODE
}