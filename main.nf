process EXTRACT_BRAIN_FEATURES {
    tag "$subject_id"
    publishDir "${params.outdir}/features", mode: 'copy'

    conda "conda-forge::python=3.11 conda-forge::numpy=1.25 conda-forge::pandas=2.0 conda-forge::nibabel=5.1"
    container "python:3.11-slim"

    input:
    tuple val(subject_id), path(nii_file)

    output:
    path("${subject_id}_metrics.csv"), emit: metrics_csv

    script:
    """
    python -m pip install --no-cache-dir nibabel numpy pandas
    python ${workflow.projectDir}/bin/compute_brain_metrics.py --nii ${nii_file} --out ${subject_id}_metrics.csv
    """
}