# SelfCA
Self learning celular automata functions

This repository...



The first function is to create a CA binary sequence of images in Netcdf files
# Cellular Automata Image Generator

This Python script contains a function called `generate_ca_images_rule` that generates a sequence of cellular automata (CA) images based on a specified rule number. The generated images are saved in a NetCDF file format using the xarray library.

## Function Usage

The `generate_ca_images_rule` function has the following parameters:

- `rule_number` (integer): The rule number defining the cellular automata behavior. The rule number is converted into a binary representation to determine cell updates.
- `size` (tuple of two integers): The size of the generated CA grid (default: (100, 100)).
- `steps` (integer): The number of time steps to run the cellular automata simulation (default: 10).
- `output_file` (string): The output file name for the NetCDF file (default: "ca_images.nc").

### Example

To generate a sequence of 100 CA images with rule number 2 and grid size of 100x100, run the following code:

```python
generate_ca_images_rule(2, size=(100, 100), steps=100, output_file="ca_images2.nc")


