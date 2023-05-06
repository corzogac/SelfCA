# %%
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider
from CA_Read import read_ca_images


def visualize_ca_images(ca_array):
    def plot_ca_image(time_step):
        plt.figure(figsize=(8, 8))
        plt.imshow(ca_array[time_step], cmap='binary')
        plt.title(f'Time step: {time_step}')
        plt.axis('off')
        plt.show()

    interact(plot_ca_image, time_step=IntSlider(min=0, max=len(ca_array) - 1, step=1, value=0))

#%%
# Example usage
ca_array = read_ca_images("ca_images2.nc")
visualize_ca_images(ca_array)
# %%
