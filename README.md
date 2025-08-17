# 🤖 Automata Studio

Automata Studio is an interactive, web-based playground for researching and learning about Self-Learning Cellular Automata (SLCA). This project provides a full suite of tools to generate simulation data, preprocess it for machine learning, train models like CNNs, and visually analyze the results.

## ✨ Project Status

* **Backend:** ✅ The Python backend scripts for generation, preprocessing, and training are complete and operational via the command line.
* **Frontend:** 🏗️ The web-based dashboard is currently in development.

## 🔧 Installation & Setup (with `uv`)

1.  Clone the repository:
    ```bash
    git clone [https://github.com/corzogac/SelfCA.git](https://github.com/corzogac/SelfCA.git)
    cd SelfCA
    ```
2.  Create and activate a virtual environment using `uv`:
    ```bash
    uv venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  Install the required packages:
    ```bash
    uv pip install -r requirements.txt
    ```

## 🖥️ Backend Command-Line Usage

You can run the full workflow from your terminal.

### 1. Generate an Environment
Create a 100-step Game of Life simulation and save it.
```bash
python -m environments.from_game_of_life --output gol_sim.nc --steps 100