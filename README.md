⚡ Predictive Energy Trading & Risk Dashboard

An AI-augmented system architecture simulating automated risk mitigation in volatile markets.

🎯 Project Overview

This project was engineered to demonstrate the architectural parallels between physical system balancing (a Smart Energy Grid) and financial risk management (Portfolio Stop-Loss Execution).

At its core, it is a full-stack, containerized application that ingests real-time telemetry from a chaotic environment, uses a heuristic AI model to forecast volatility, and executes autonomous mitigation actions to protect against price spikes. Every action is logged to an immutable database ledger to ensure strict compliance and auditability.

🏗️ System Architecture & Tech Stack

This system moves beyond basic scripting by utilizing a robust, enterprise-grade architecture:

The Physics Engine (Python OOP): A custom-built backend simulating supply/demand curves and market pricing logic.

The Immutable Ledger (PostgreSQL & Docker): A containerized PostgreSQL database that captures real-time telemetry and acts as a secure audit trail for automated system interventions.

The Executive Dashboard (Streamlit & Plotly): A live-updating UI featuring dual-axis financial charting and AI-driven risk confidence scoring.

⚙️ Core System Flow

Telemetry Ingestion: The engine continuously logs system frequency and market pricing to the grid_telemetry database table.

AI Risk Forecasting: The Streamlit dashboard analyzes demand trends to calculate a rolling probability of a critical system failure or price spike.

Automated Mitigation (Stop-Loss): If the market price crosses the critical threshold (100p/kWh), the backend algorithm autonomously sheds low-priority load.

Compliance Auditing: The exact financial impact and timestamp of the automated action are permanently written to the risk_mitigation_log table.

🚀 How to Run Locally

1. Initialize the Database Infrastructure

Ensure Docker Desktop is running, then spin up the isolated PostgreSQL container:

docker run --name smartgrid-db -e POSTGRES_PASSWORD=fintech -p 5432:5432 -d postgres


2. Install Dependencies

python3 -m pip install psycopg2-binary streamlit pandas plotly


3. Start the Executive Dashboard

python3 -m streamlit run app.py


4. Run the Simulation Engine

Open a second terminal window and execute the backend physics engine to generate live market volatility:

python3 main.py
