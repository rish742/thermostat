import time
import matplotlib.pyplot as plt
import numpy as np

class Thermostat:
    def __init__(self, initial_temp=22, set_temp=22):
        self.current_temp = initial_temp  # Room Temperature
        self.set_temp = set_temp  # Target Temperature
        self.mode = "Off"  # Modes: Off, H, AH, C, AC
        self.hold = False  # If True, ignore signals

        # Temperature change rates
        self.heat_rate = 0.2  # Heating effect per time step
        self.cool_rate = 0.15  # Cooling effect per time step
        self.passive_loss = 0.05  # Cooling when Off

        # Signals per hour
        self.signals = {
            "Day 1": {6: "UP", 8: "H", 12: "DOWN", 16: "C", 18: "UP", 22: "Off"},
            "Day 2": {7: "H", 10: "DOWN", 14: "C", 17: "UP", 21: "Off"}
        }

        # Logging
        self.time_log = []
        self.temp_log = []
        self.set_temp_log = []
        self.signal_log = []

    def press_mode(self, mode):
        """Manually change the mode"""
        if mode in ["H", "C", "Off"]:
            self.mode = mode
            print(f"Mode set to {self.mode}")

    def press_up(self):
        """Increase set temperature and enter Hold mode"""
        self.set_temp += 1
        self.hold = True
        self.signal_log.append(("Up", len(self.time_log)))
        print(f"Set temperature increased to {self.set_temp}°C")

    def press_down(self):
        """Decrease set temperature and enter Hold mode"""
        self.set_temp -= 1
        self.hold = True
        self.signal_log.append(("Down", len(self.time_log)))
        print(f"Set temperature decreased to {self.set_temp}°C")

    def adjust_temperature(self):
        """Simulate temperature dynamics"""
        if self.mode == "AH":  # Active Heating
            self.current_temp += self.heat_rate
        elif self.mode == "AC":  # Active Cooling
            self.current_temp -= self.cool_rate
        elif self.mode == "Off":  # Passive Cooling
            self.current_temp -= self.passive_loss

        # Switch states based on current vs set temperature
        if self.mode == "H" and self.current_temp < self.set_temp - 1:
            self.mode = "AH"  # Activate heating
            self.signal_log.append(("Heating", len(self.time_log)))
        elif self.mode == "C" and self.current_temp > self.set_temp + 1:
            self.mode = "AC"  # Activate cooling
            self.signal_log.append(("Cooling", len(self.time_log)))

    def process_signal(self, day, hour):
        """Process predefined signals"""
        if hour in self.signals[day]:
            action = self.signals[day][hour]
            if action == "UP":
                self.press_up()
            elif action == "DOWN":
                self.press_down()
            elif action in ["H", "C", "Off"]:
                self.press_mode(action)
                self.signal_log.append((action, len(self.time_log)))

    def run_simulation(self):
        """Simulate 2 days (48-hour cycle)"""
        for day in ["Day 1", "Day 2"]:
            print(f"\n===== {day} =====")
            for hour in range(24):
                timestamp = f"{day} {hour}:00"
                print(f"Time: {timestamp} | Mode: {self.mode} | Temp: {self.current_temp:.1f}°C | Set Temp: {self.set_temp}°C")

                self.process_signal(day, hour)
                self.adjust_temperature()

                # Store data for plotting
                self.time_log.append(timestamp)
                self.temp_log.append(self.current_temp)
                self.set_temp_log.append(self.set_temp)

                time.sleep(0.1)  # Simulate real-time passing

        self.plot_results()

    def plot_results(self):
        """Plot temperature changes and control signals"""

        fig, axs = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [2, 1]})

        # Temperature plot
        axs[0].plot(self.temp_log, label="Room Temperature", marker="o", markersize=4, linewidth=2)
        axs[0].plot(self.set_temp_log, label="Set Temperature", linewidth=2, color="orange")

        axs[0].set_xticks(np.linspace(0, len(self.time_log)-1, num=10, dtype=int))
        axs[0].set_xticklabels([self.time_log[i] for i in np.linspace(0, len(self.time_log)-1, num=10, dtype=int)], rotation=45)
        axs[0].set_ylabel("Temperature (°C)")
        axs[0].set_title("Thermostat Temperature Simulation (2 Days)")
        axs[0].legend()
        axs[0].grid(True, linestyle="--", alpha=0.7)

        # Control signals plot
        y_labels = ["Cooling", "Down", "Off", "Up", "Heating"]
        y_positions = range(len(y_labels))

        for signal, time_idx in self.signal_log:
            y_value = y_labels.index(signal) if signal in y_labels else None
            if y_value is not None:
                axs[1].scatter(time_idx, y_value, color="red", marker="s", label="Signals" if time_idx == self.signal_log[0][1] else "")

        axs[1].set_yticks(y_positions)
        axs[1].set_yticklabels(y_labels)
        axs[1].set_xticks(np.linspace(0, len(self.time_log)-1, num=10, dtype=int))
        axs[1].set_xticklabels([self.time_log[i] for i in np.linspace(0, len(self.time_log)-1, num=10, dtype=int)], rotation=45)
        axs[1].set_title("Thermostat Control Signals")
        axs[1].legend()
        axs[1].grid(True, linestyle="--", alpha=0.7)

        plt.tight_layout()
        plt.show()

# Run the simulation
t = Thermostat()
t.run_simulation()
