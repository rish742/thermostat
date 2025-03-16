import numpy as np
import matplotlib.pyplot as plt
from enum import Enum, auto

class ThermostatMode(Enum):
    OFF = auto()
    HEATING = auto()
    COOLING = auto()

class ThermostatState(Enum):
    OFF = auto()
    H = auto()
    AH = auto()
    C = auto()
    AC = auto()

class Thermostat:
    def __init__(self):
        self.mode = ThermostatMode.OFF
        self.state = ThermostatState.OFF

        self.scheduled_temps = {"Work": 68 , "Home": 72, "Sleep": 65}
        self.schedule_times = {"Work": (7, 16), "Home": (16, 22), "Sleep": (22, 7)}

        self.current_schedule = "Work"
        self.set_temperature = self.scheduled_temps[self.current_schedule]
        self.room_temperature = 72

        self.hold_mode = False
        self.heating_active = False
        self.cooling_active = False
        self.deadband = 1

    def set_mode(self, mode: ThermostatMode):
        self.mode = mode
        if mode == ThermostatMode.OFF:
            self.state = ThermostatState.OFF
            self.heating_active = False
            self.cooling_active = False

    def adjust_temperature(self, up: bool, down: bool):
        if up or down:
            self.hold_mode = True
            self.current_schedule = "Hold"
        if up:
            self.set_temperature += 1
        if down:
            self.set_temperature -= 1

    def update_schedule(self, current_time: float):
        if self.hold_mode:
            # Exit Hold state at the next schedule transition
            for schedule, (start, end) in self.schedule_times.items():
                if abs(current_time - start) < 0.1 or abs(current_time - end) < 0.1:
                    self.hold_mode = False
                    self.current_schedule = schedule
                    self.set_temperature = self.scheduled_temps[schedule]
                    break
        else:
            for schedule, (start, end) in self.schedule_times.items():
                if start <= current_time < end or (end < start and (current_time >= start or current_time < end)):
                    self.current_schedule = schedule
                    self.set_temperature = self.scheduled_temps[schedule]
                    break

    def update_state(self):
        if self.mode == ThermostatMode.HEATING:
            if self.room_temperature < self.set_temperature - self.deadband:
                self.state = ThermostatState.AH
                self.heating_active = True
            elif self.room_temperature > self.set_temperature + self.deadband:
                self.state = ThermostatState.H
                self.heating_active = False
        elif self.mode == ThermostatMode.COOLING:
            if self.room_temperature > self.set_temperature + self.deadband:
                self.state = ThermostatState.AC
                self.cooling_active = True
            elif self.room_temperature < self.set_temperature - self.deadband:
                self.state = ThermostatState.C
                self.cooling_active = False
        else:
            self.state = ThermostatState.OFF
            self.heating_active = False
            self.cooling_active = False

    def simulate_step(self, mode, up, down, room_temp, current_time):
        self.set_mode(ThermostatMode[mode])
        self.update_schedule(current_time)
        self.adjust_temperature(up, down)
        self.room_temperature = room_temp
        self.update_state()

        return {
            "Time": current_time,
            "Schedule": self.current_schedule,
            "Mode": self.mode.name,
            "State": self.state.name,
            "ST": self.set_temperature,
            "RT": self.room_temperature,
            "AH": int(self.heating_active),
            "AC": int(self.cooling_active),
            "Hold": int(self.hold_mode)
        }

# Initialize thermostat
thermostat = Thermostat()

# Simulation parameters
duration_hours = 24
time_step = 0.1
time_points = int(duration_hours / time_step)

# Inputs
modes = ["HEATING", "COOLING", "OFF"]
mode_pattern = []
for i in range(time_points):
    current_time = (i * time_step) % 24
    if 0 <= current_time < 4:
        mode_pattern.append("OFF")
    elif 4 <= current_time < 8:
        mode_pattern.append("HEATING")
    elif 8 <= current_time < 12:
        mode_pattern.append("OFF")
    elif 12 <= current_time < 16:
        mode_pattern.append("COOLING")
    elif 16 <= current_time < 20:
        mode_pattern.append("OFF")
    else:
        mode_pattern.append("HEATING")


# Set toggle times for up and down
toggle_times_up = np.random.choice(time_points, 2, replace=False)
toggle_times_down = np.random.choice(time_points, 2, replace=False)

up_button_signal = np.zeros(time_points, dtype=bool)
down_button_signal = np.zeros(time_points, dtype=bool)

up_button_signal[toggle_times_up] = True
down_button_signal[toggle_times_down] = True

# Room temperature variation
room_temp_pattern = 68 + 4 * np.sin(np.linspace(0, 4 * np.pi, time_points))

# Storage for results
results = []

for i in range(time_points):
    current_time = (i * time_step) % 24
    result = thermostat.simulate_step(
        mode=mode_pattern[i],
        up=up_button_signal[i],
        down=down_button_signal[i],
        room_temp=room_temp_pattern[i],
        current_time=current_time
    )
    results.append(result)

results = {key: [r[key] for r in results] for key in results[0]}

# Map states to numerical values
state_mapping = {'OFF': 0, 'H': 1, 'AH': 2, 'C': -1, 'AC': -2}
results['State'] = [state_mapping[state] for state in results['State']]

# Map schedules to numerical values
schedule_mapping = {'Sleep': 0, 'Work': 1, 'Home': 2, 'Hold': 3}
results['Schedule'] = [schedule_mapping[schedule] for schedule in results['Schedule']]

# Plotting
plt.figure(figsize=(12, 12))

# State plot
plt.subplot(6, 1, 1)
plt.plot(results['Time'], results['State'], label='State')
plt.yticks([-2, -1, 0, 1, 2], ['AC', 'C', 'OFF', 'H', 'AH'])
plt.legend()
plt.title('Thermostat State Changes')

# Up toggle
plt.subplot(6, 1, 2)
plt.plot(results['Time'], up_button_signal, label='Up', linestyle='--')
plt.legend()
plt.title('Up Adjustments')

# Down toggle
plt.subplot(6, 1, 3)
plt.plot(results['Time'], down_button_signal, label='Down', linestyle='--', color='orange')
plt.legend()
plt.title('Down Adjustments')

# Schedule states
plt.subplot(6, 1, 4)
plt.plot(results['Time'], results['Schedule'], label='Schedule')
plt.yticks([0, 1, 2, 3], ['Sleep', 'Work', 'Home', 'Hold'])
plt.legend()
plt.title('Schedule States')

# Room vs Set Temperature
plt.subplot(6, 1, 5)
plt.plot(results['Time'], results['RT'], label='Room Temp')
plt.plot(results['Time'], results['ST'], label='Set Temp')
plt.legend()
plt.title('Room vs Set Temperature')

plt.tight_layout()
plt.show()
