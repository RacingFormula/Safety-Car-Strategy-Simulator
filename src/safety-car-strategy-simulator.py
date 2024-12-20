import numpy as np
import pandas as pd

class SafetyCarSimulator:
    def __init__(self, config):
        self.config = config
        self.race_distance = config.get("race_distance", 50)
        self.safety_car_laps = set(config.get("safety_car_laps", []))
        self.initial_fuel_load = config.get("initial_fuel_load", 100)
        self.tyre_degradation_rate = config.get("tyre_degradation_rate", 0.02)
        self.pit_stop_time = config.get("pit_stop_time", 20)  # in seconds
        self.lap_time_variation = config.get("lap_time_variation", 0.1)

    def calculate_lap_time(self, lap, fuel_remaining):
        base_lap_time = 90  # seconds, baseline lap time
        tyre_penalty = self.tyre_degradation_rate * lap
        fuel_penalty = (1 - fuel_remaining / 100) * 0.5  # seconds per percentage
        random_variation = np.random.normal(0, self.lap_time_variation)
        return base_lap_time + tyre_penalty + fuel_penalty + random_variation

    def simulate_pit_stop(self, lap):
        return {"lap": lap, "event": "Pit Stop", "time_loss": self.pit_stop_time}

    def run(self):
        results = []
        current_fuel = self.initial_fuel_load
        total_time = 0

        for lap in range(1, self.race_distance + 1):
            if lap in self.safety_car_laps:
                time_loss = 10  # seconds slower per lap under safety car
                total_time += time_loss
                results.append({"lap": lap, "event": "Safety Car", "lap_time": time_loss})
            else:
                lap_time = self.calculate_lap_time(lap, current_fuel)
                total_time += lap_time

                # Simulate pit stops (basic logic: pit every 15 laps)
                if lap % 15 == 0:
                    pit_stop = self.simulate_pit_stop(lap)
                    total_time += pit_stop["time_loss"]
                    results.append(pit_stop)
                    current_fuel = self.initial_fuel_load

                current_fuel -= 2  # fuel consumption per lap (percentage)
                results.append({"lap": lap, "lap_time": lap_time, "fuel_remaining": current_fuel})

        summary = pd.DataFrame(results)
        summary["cumulative_time"] = summary["lap_time"].cumsum()
        return summary

if __name__ == "__main__":
    config = {
        "race_distance": 50,
        "safety_car_laps": [15, 30],
        "initial_fuel_load": 100,
        "tyre_degradation_rate": 0.02,
        "pit_stop_time": 20,
        "lap_time_variation": 0.1,
    }

    simulator = SafetyCarSimulator(config)
    results = simulator.run()
    print(results)