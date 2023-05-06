#%%
import numpy as np
import xarray as xr
def generate_ca_images_rule(rule_number, size=(100, 100), steps=10, output_file="ca_images.nc"):
    def step(grid, rule_binary):
        padded_grid = np.pad(grid, pad_width=1, mode='wrap')
        result = np.zeros_like(grid)

        for i in range(1, padded_grid.shape[0] - 1):
            for j in range(1, padded_grid.shape[1] - 1):
                neighborhood = padded_grid[i-1:i+2, j-1:j+2].flatten()
                idx = int("".join(map(str, neighborhood)), 2)
                if 0 <= idx < 8:
                    result[i-1, j-1] = rule_binary[7 - idx]

        return result

    rule_binary = np.array([int(b) for b in format(rule_number, '08b')])
    grid = np.random.randint(0, 2, size)
    ca_images = np.zeros((steps, *size), dtype=np.uint8)

    for t in range(steps):
        grid = step(grid, rule_binary)
        ca_images[t] = grid

    ca_images_da = xr.DataArray(ca_images, dims=["time", "x", "y"], coords={"time": np.arange(steps)})
    ca_images_da.to_netcdf(output_file)


# %%
# Example usage
generate_ca_images_rule(2, size=(100, 100), steps=100, output_file="ca_images2.nc")

# %%
