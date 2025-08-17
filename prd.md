1. Objective
To create an interactive and educational web-based playground for researching Self-Learning Cellular Automata (SLCA). The framework will serve as a dual-purpose tool: an educational platform for learning CA fundamentals through classic examples and a research workbench for comparing advanced ML models (TensorFlow/CNNs) on complex spatial analysis tasks.

2. Core Features & User Stories
(Features 1 and 2 for the backend and ML engine remain the same)

Feature 3: Interactive Research Dashboard & Playground (Revised)
This feature redefines the web interface as a central, interactive hub for learning and experimentation.

User Story (Learner): "As a new user, I want to select 'Conway's Game of Life' from a list of classic examples to understand the basic principles of cellular automata before trying the advanced features."

User Story (Researcher): "As a researcher, I need a dashboard with controls to configure my entire experiment. I want to select a problem type, choose my ML model from a dropdown, upload a target image, and tune parameters before running the simulation."

Functionality:

Problem Selection: A main control panel where users can choose the task:

Classic CA: (e.g., Conway's Game of Life, Rule 30).

Learn from Image: The core SLCA feature.

Spatiotemporal Inpainting: The remote sensing application.

Parameter Controls: Interactive widgets (sliders, dropdowns) for setting up the experiment, mirroring the TensorFlow Playground's usability. This includes model selection, data input, and simulation settings.

Integrated Visualization: A multi-pane view that displays:

The live CA simulation.

Real-time charts of model training metrics (loss, accuracy).

The original source image or data for reference.

4. Applications & Success Metrics (Updated)
Educational Value: A new user can successfully launch the "Game of Life" simulation within their first minute on the site.

Research Usability: A researcher can set up, run, and get visual feedback on a custom "Learn from Image" experiment entirely through the dashboard interface.

(Other metrics remain the same)

This "Playground" concept gives the project a much clearer identity and a more engaging user experience. It perfectly balances the goals of education and advanced research.

📁 File Name and Location
File Name: PRD.md
This is a standard and clean convention. Using the .md extension means it will be correctly formatted as Markdown on GitHub, making it easy to read.

Location: The root of your project folder (e.g., SelfCA/PRD.md).
Placing it here ensures it's one of the first things a new contributor sees, alongside your README.md. For larger projects, you might create a docs/ folder, but for now, the root is perfect for visibility.

Staring project structure should now look something like this:

SelfCA/
├── .git/
├── venv/
├── CA_Generate.py
├── CA_Read.py
├── CA_visualize.py
├── PRD.md
├── README.md
└── requirements.txt