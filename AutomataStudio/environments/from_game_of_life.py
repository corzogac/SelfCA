#
# Automata Studio
# Copyright (c) 2025, Gerald Corzo
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

"""
This module provides a generator for the classic "Conway's Game of Life"
cellular automaton simulation. It can be run directly to generate, report on,
and visualize a simulation.
"""

import numpy as np
import argparse
from scipy.signal import convolve2d
from .common import save_as_netcdf, generate_report, visualize_simulation

def generate_game_of_life(size: tuple = (100, 100), steps: int = 100, output_file: str = "game_of_life.nc"):
    """Generates a simulation of Conway's Game of Life."""

    grid = np.random.randint(0, 2, size, dtype=np.uint8)
    ca_images = np.zeros((steps, *size), dtype=np.uint8)
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    for t in range(steps):
        ca_images[t] = grid
        neighbor_count = convolve2d(grid, kernel, mode='same', boundary='wrap')
        survives = (grid == 1) & ((neighbor_count == 2) | (neighbor_count == 3))
        born = (grid == 0) & (neighbor_count == 3)
        grid = (survives | born).astype(np.uint8)

    save_as_netcdf(ca_images, variable_name="life_state", output_file=output_file)
    return output_file

if __name__ == "__main__":
    # --- Default Configuration for Programmers ---
    # Easily change these values for quick tests.
    DEFAULT_TEST_CONFIG = {
        "size": 128,
        "steps": 200,
        "output": "game_of_life_sim.nc"
    }
    # -------------------------------------------

    parser = argparse.ArgumentParser(description="Generate, report on, and visualize a Game of Life simulation.")
    parser.add_argument("--size", type=int, default=DEFAULT_TEST_CONFIG["size"], help="The grid size.")
    parser.add_argument("--steps", type=int, default=DEFAULT_TEST_CONFIG["steps"], help="The number of time steps.")
    parser.add_argument("--output", type=str, default=DEFAULT_TEST_CONFIG["output"], help="The output NetCDF file name.")
    parser.add_argument("--no-animation", action="store_true", help="Skip launching the animation.")

    args = parser.parse_args()

    # --- Full Workflow ---
    print("--- 1. Generating Simulation ---")
    output_filename = generate_game_of_life(
        size=(args.size, args.size),
        steps=args.steps,
        output_file=args.output
    )

    print("\n--- 2. Generating Report ---")
    report_dir = args.output.replace('.nc', '_report')
    generate_report(output_filename, report_dir=report_dir)

    if not args.no_animation:
        print("\n--- 3. Launching Animation ---")
        visualize_simulation(output_filename, save_gif=True)

    print("\n--- Workflow Complete ---")