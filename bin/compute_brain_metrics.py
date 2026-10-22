#!/usr/bin/env python3
import argparse
from pathlib import Path
import nibabel as nib
import numpy as np
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Extract volumetric and intensity metrics from NIfTI image")
    parser.add_argument("--nii", required=True, type=str, help="Path to input .nii or .nii.gz file")
    parser.add_argument("--out", required=True, type=str, help="Output CSV path")
    args = parser.parse_args()

    nii_path = Path(args.nii)
    img = nib.load(str(nii_path))
    data = img.get_fdata()
    
    # Compute basic metrics
    voxel_volumes = np.prod(img.header.get_zooms()[:3])
    non_zero_voxels = np.count_nonzero(data)
    total_volume_mm3 = non_zero_voxels * voxel_volumes
    mean_intensity = float(np.mean(data[data > 0])) if non_zero_voxels > 0 else 0.0

    metrics = {
        "file_name": [nii_path.name],
        "shape": [str(img.shape)],
        "total_volume_mm3": [total_volume_mm3],
        "mean_intensity": [mean_intensity]
    }

    df = pd.DataFrame(metrics)
    df.to_csv(args.out, index=False)
    print(f"Successfully extracted metrics for {nii_path.name}")

if __name__ == "__main__":
    main()