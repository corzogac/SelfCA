# PRD (v4): "Automata Studio" Playground

## 1. Objective

To create an interactive, web-based playground for researching and learning about Self-Learning Cellular Automata (SLCA). The application will guide users through the complete workflow—from environment generation to model training and visual analysis—using a clean, intuitive dashboard interface powered by a Python/FastAPI backend.

## 2. Project Modules & Status

### Backend (Complete)
The core backend logic is implemented in three distinct Python modules:
* **`environments`**: Generates simulation data (e.g., Game of Life, from images) and saves it in `.nc` format. Includes standardized reporting and visualization.
* **`preprocessing`**: Takes simulation data and creates ML-ready datasets (`.nc`), handling normalization, data formatting (CNN/Tabular), and splitting, while saving key statistics.
* **`models`**: Defines, trains, and evaluates a flexible CNN model. Saves the trained model (`.keras`) and generates advanced analysis visualizations (rule heatmaps, predictive animations).

### Frontend (In-Planning)
The frontend will be a single-page web application that provides a user interface for the backend modules.

## 3. Core Frontend Features (User Stories)

The dashboard will be organized into a logical workflow, likely through tabs or sequential sections.

### Feature 1: The "Generator" Hub
* **User Story:** As a user, I want to select a generator (e.g., "Game of Life"), set parameters like grid size and steps, and click a button to create and view a new simulation environment.
* **Backend Hook:** This will trigger a FastAPI endpoint that runs the selected script from the `environments` module and makes the resulting animation and report available for download or viewing.

### Feature 2: The "Preprocessor" Factory
* **User Story:** As a user, I want to select a generated simulation file from a list, choose a data format ('CNN' or 'Tabular'), and click 'Process' to create a training dataset.
* **Backend Hook:** Triggers an endpoint that runs the `preprocessing/create_dataset.py` script and reports the outcome.

### Feature 3: The "Training Ground"
* **User Story:** As a user, I want to select a processed dataset, configure basic model parameters (initially fixed, later expandable), and click 'Train' to build a model.
* **User Story:** While the model trains, I want to see a live-updating chart of the training and validation accuracy/loss.
* **Backend Hook:** Triggers the `models/cnn_trainer.py` script. Live updates will be pushed from the server to the client via WebSockets.

### Feature 4: The "Analysis Lab"
* **User Story:** As a user, I want to select a trained model and an original simulation file to see the side-by-side predictive animation, rule heatmap, and other analysis plots directly in my browser.

## 4. Technical Stack (Revised)

* **Backend:** Python, FastAPI, Uvicorn
* **Data/ML:** Xarray, NumPy, TensorFlow/Keras
* **Frontend:** HTML5, CSS3, JavaScript
* **JS Framework (Recommended):** Vue.js or React for managing the dashboard's complex state.
* **JS Libraries:** Chart.js (for training graphs), p5.js or HTML Canvas API (for animations).
* **Real-time Communication:** WebSockets (for live training feedback).
