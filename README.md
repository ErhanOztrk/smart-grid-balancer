# Smart Grid Balancer 🌍⚡

This is my very first backend Python project! I built this command-line application to learn the fundamentals of Object-Oriented Programming (OOP) and to see how code can be used to model real-world problems.

The project simulates the "Duck Curve" phenomenon on an energy grid. It shows what happens when renewable energy drops off but consumer demand spikes, and how a "Smart Home" might autonomously react to save the grid.

## What I Learned Building This

Building this from scratch was a massive learning experience. Through this project, I learned how to:

- **Write Python Logic:** Mastered Python's strict indentation rules and syntax.
- **Object-Oriented Programming:** Created separate modules (`Classes`) so the code is clean and organized.
- **State Management:** Tracked changing variables (like whether an appliance is `on` or `off`).
- **Debugging:** Learned how to read tracebacks, clear `__pycache__`, and resolve file-locking issues in the terminal.
- **Version Control:** Used Git to make atomic commits and track my history.

## How the Code is Organized

Instead of putting everything in one giant file, I separated the logic into three distinct blueprints:

1. **`grid.py`:** Calculates the total energy demand and drops the grid frequency if it gets overloaded.
2. **`home.py`:** Contains appliances and listens to the grid. If the price spikes, it automatically turns off low-priority appliances.
3. **`appliance.py`:** A basic blueprint for things like an EV Charger or a Fridge, tracking their power draw and priority level.

## How to Run It

1. Make sure you have Python 3 installed.
2. Clone this repository to your machine.
3. Run the main simulation from your terminal:
   ```bash
   python3 main.py
   ```
