# 🌀 Thermostat Simulation Project

This project simulates a smart thermostat that adjusts its behavior based on:
- System mode (HEATING, COOLING, or OFF)
- Scheduled temperature preferences (Work, Home, Sleep)
- Manual user inputs (temperature up/down)
- Room temperature changes over time

---

## 🗂️ Project Structure

```
📁 Python_Simulation
    └── thermostat.py               # Core thermostat class and simulation logic

📁 Statechart
    ├── thermostat_statechart.py   # Script for visualizing thermostat states
    ├── thermostat_statechart.png  # Generated statechart image
    └── thermostat_statechart.txt  # Optional state definition or description

🔹 .gitignore
🔹 requirements.txt                # List of Python dependencies
🔹 README.md                       # Project overview and instructions
```

## 🔧 Features

- **Thermostat Modes**: User-settable to `HEATING`, `COOLING`, or `OFF` (exclusive).
- **Temperature States**:
  - `AH`: Active Heating
  - `H`: Heating mode but idle
  - `AC`: Active Cooling
  - `C`: Cooling mode but idle
  - `OFF`: Neither heating nor cooling
- **Schedules**:
  - `Work`, `Home`, `Sleep`, or `Hold` mode (Hold overrides the schedule)
- **Manual Control**: Users can simulate pressing "up" or "down" buttons.
- **Deadband**: Prevents frequent toggling between heating/cooling.
- **Mode Scheduling**: Simulated timeline that includes OFF periods to save energy.

---

## ▶️ How to Run the Simulation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
