# SelfCA

Self learning celular automata functions folder contains the tools needed to generate and analyze files that will be trained and later on used as rules. The concept of rules is applied here in a way that a 8 bits represent all the possible states of the neighbors, and by applying a linear mapping is possible to generate transitions of this binary combinations of the 8 neighbors.

1.  Cellular Automata Image Generator
2. Reading Cellular Automata Images from a netCDF File
3. Visualization of the file with a sliding bar

The first function is to create a CA binary sequence of images in Netcdf files
## Cellular Automata Image Generator

This Python script contains a function called `generate_ca_images_rule` that generates a sequence of cellular automata (CA) images based on a specified rule number. The generated images are saved in a NetCDF file format using the xarray library.

### Function Usage

The `generate_ca_images_rule` function has the following parameters:

- `rule_number` (integer): The rule number defining the cellular automata behavior. The rule number is converted into a binary representation to determine cell updates.
- `size` (tuple of two integers): The size of the generated CA grid (default: (100, 100)).
- `steps` (integer): The number of time steps to run the cellular automata simulation (default: 10).
- `output_file` (string): The output file name for the NetCDF file (default: "ca_images.nc").

#### Example

To generate a sequence of 100 CA images with rule number 2 and grid size of 100x100, run the following code:

```python
generate_ca_images_rule(2, size=(100, 100), steps=100, output_file="ca_images2.nc")
```


## Reading Cellular Automata Images from a netCDF File

The `read_ca_images` function reads Cellular Automata images stored in a netCDF file and returns them as a NumPy array. The input to the function is the path to the netCDF file, and the output is a NumPy array with the dimensions (time, x, y), where `time` represents the time sequence of the Cellular Automata images.

### Function signature
```python
def read_ca_images(input_file: str) -> np.ndarray:
```

**Parameters**
input_file: A string representing the path to the netCDF file containing the Cellular Automata images.
Returns

A NumPy array with the dimensions (time, x, y), containing the Cellular Automata images.

#### Example usage
python 
```python
filename = "ca_images2.nc"
ca_array = read_ca_images(filename)
print(ca_array.shape)
```
In the example above, the function read_ca_images reads the Cellular Automata images from the specified netCDF file and returns a NumPy array. The shape of the array is printed, showing the dimensions (time, x, y) of the images.
