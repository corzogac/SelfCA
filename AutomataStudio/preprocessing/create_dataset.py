#
# Automata Studio
# Copyright (c) 2025, Gerald Corzo
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

"""
This module is responsible for taking simulation data from a .nc file
and converting it into a machine-learning-ready dataset. It extracts
neighborhood patterns (X) and their resulting center-cell states (y),
normalizes the features, and saves the split datasets along with
the normalization statistics to a NetCDF file.
"""
import numpy as np
import xarray as xr
import argparse
from sklearn.model_selection import train_test_split

# --- Configuration Constants ---
NEIGHBORHOOD_SIZE = 3
SPLIT_RATIOS = {
    "70-30": {"train": 0.7, "test": 0.3},
    "70-20-10": {"train": 0.7, "val": 0.2, "test": 0.1}
}

def _save_dataset_as_netcdf(output_filename: str, datasets: dict, stats: dict):
    """Helper function to save processed datasets and stats to a NetCDF file."""
    
    # Create an xarray Dataset to hold all our data
    processed_ds = xr.Dataset()
    
    # Store each data split as a separate DataArray
    for name, data in datasets.items():
        if data.ndim == 1: # This is a label vector (y)
            dims = (f"{name.split('_')[1]}_samples",)
        elif 'cnn' in stats.get('data_format', ''): # CNN data
            dims = (f"{name.split('_')[1]}_samples", 'height', 'width', 'channels')
        else: # Tabular data
             dims = (f"{name.split('_')[1]}_samples", 'features')
        
        processed_ds[name] = xr.DataArray(data, dims=dims)
        
    # Store all normalization statistics as global attributes of the file
    processed_ds.attrs.update(stats)
    
    # Save to a NetCDF file
    processed_ds.to_netcdf(output_filename)


def create_ml_dataset(netcdf_file: str, data_format: str = 'cnn', split_config: dict = SPLIT_RATIOS["70-20-10"], normalization: str = 'standardize'):
    """
    Loads, processes, normalizes, and splits simulation data for ML models.
    """
    print(f"🔬 Creating dataset from '{netcdf_file}' with format '{data_format}'...")
    
    # (Steps 1, 2, 3: Load, Extract, Reshape - are unchanged)
    ds = xr.open_dataset(netcdf_file)
    data = ds[list(ds.data_vars)[0]].values
    features, labels = [], []
    radius = NEIGHBORHOOD_SIZE // 2
    for t in range(data.shape[0] - 1):
        padded_grid = np.pad(data[t], pad_width=radius, mode='wrap')
        for y in range(data.shape[1]):
            for x in range(data.shape[2]):
                features.append(padded_grid[y:y+NEIGHBORHOOD_SIZE, x:x+NEIGHBORHOOD_SIZE])
                labels.append(data[t+1, y, x])

    X = np.array(features, dtype=np.float32)
    y = np.array(labels, dtype=np.float32)
    
    if data_format == 'cnn':
        X = X.reshape(-1, NEIGHBORHOOD_SIZE, NEIGHBORHOOD_SIZE, 1)
    elif data_format == 'tabular':
        X = X.reshape(-1, NEIGHBORHOOD_SIZE * NEIGHBORHOOD_SIZE)
    
    # 4. ✂️ Split Data
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, train_size=split_config["train"], stratify=y, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42)
    datasets = {"X_train": X_train, "y_train": y_train, "X_val": X_val, "y_val": y_val, "X_test": X_test, "y_test": y_test}

    # 5. 📊 Calculate Statistics & Normalize Data
    stats_to_save = {'normalization_method': normalization, 'data_format': data_format}
    if normalization:
        # ... (Normalization logic is unchanged, it calculates stats from X_train and applies to all)
        if normalization == 'standardize':
            train_mean, train_std = np.mean(X_train), np.std(X_train)
            if train_std == 0: train_std = 1.0 
            for key in ['X_train', 'X_val', 'X_test']: datasets[key] = (datasets[key] - train_mean) / train_std
            stats_to_save.update({'train_mean': train_mean, 'train_std': train_std})
        # ... (minmax logic is similar)

    # 6. 📦 Save the processed data and stats to a NetCDF file
    output_filename = netcdf_file.replace('.nc', f'_dataset_{data_format}.nc')
    _save_dataset_as_netcdf(output_filename, datasets, stats_to_save)
    print(f"\n✅ Successfully saved datasets and stats to {output_filename}")
    
    # 7. ✨ Expanded Report to Console
    print("   --- Preprocessing Report ---")
    print(f"   Input File: {netcdf_file}")
    print(f"   Total Samples: {len(y)}")
    print(f"   Normalization: {normalization}")
    if normalization == 'standardize':
        print(f"   - train_mean: {stats_to_save['train_mean']:.4f}")
        print(f"   - train_std: {stats_to_save['train_std']:.4f}")
        print(f"   - val_mean (norm): {np.mean(datasets['X_val']):.4f}")
        print(f"   - val_std (norm): {np.std(datasets['X_val']):.4f}")
        print(f"   - test_mean (norm): {np.mean(datasets['X_test']):.4f}")
        print(f"   - test_std (norm): {np.std(datasets['X_test']):.4f}")
    print(f"   ------------------------")

    return output_filename


if __name__ == '__main__':
    # --- Default Configuration for Programmers ---
    DEFAULT_PREPROCESSING_CONFIG = {
        "format": "cnn",
        "norm": "standardize"
    }
    # -------------------------------------------

    parser = argparse.ArgumentParser(description="Create ML datasets from a CA simulation file.")
    parser.add_argument("input_file", type=str, help="Path to the input .nc simulation file.")
    parser.add_argument("--format", type=str, default=DEFAULT_PREPROCESSING_CONFIG["format"], choices=['cnn', 'tabular'], help="Output format.")
    parser.add_argument("--norm", type=str, default=DEFAULT_PREPROCESSING_CONFIG["norm"], choices=['standardize', 'minmax', 'none'], help="Normalization method.")

    args = parser.parse_args()
    
    norm_method = None if args.norm == 'none' else args.norm
    create_ml_dataset(args.input_file, data_format=args.format, normalization=norm_method)