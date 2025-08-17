#%%
# cellular_automata_utils.py
import xarray as xr
import numpy as np
from scipy.signal import convolve2d

#%%
def read_ca_images(input_file):
    with xr.open_dataset(input_file) as dataset:
        ca_images = dataset["time"].data
        time_sequence = np.arange(len(ca_images))
        ca_array = np.zeros((len(ca_images), *dataset["x"].shape, *dataset["y"].shape), dtype=np.uint8)

        for t in time_sequence:
            ca_array[t] = dataset["__xarray_dataarray_variable__"].isel(time=t).data
            
    return ca_array
#%%
# Example usage
Filename="ca_images2.nc"
ca_array = read_ca_images(Filename)
print(ca_array.shape)

