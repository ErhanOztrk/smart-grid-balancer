from typing import List
from home import SmartHome

class Grid:
    def __init__(self, initial_capacity: float):
        self.capacity = initial_capacity      # Total kW the grid can supply right now
        self.homes: List[SmartHome] = []      # The grid's network of homes
        self.nominal_frequency = 50.0         # UK standard grid frequency (Hz)

    def add_home(self, home: SmartHome):
        self.homes.append(home)

    def get_total_demand(self) -> float:
        total_demand = 0.0
        # Sum up the load of every single home on the grid
        for home in self.homes:
            total_demand += home.get_current_load()
        return total_demand

    def get_current_frequency(self) -> float:
        demand = self.get_total_demand()
        
        # If we have enough capacity, frequency stays stable at 50.0 Hz
        if demand <= self.capacity:
            return self.nominal_frequency
        
        # PHYSICS SIMULATION: If demand exceeds capacity, frequency drops.
        # For every 1 kW of overload, we simulate a drop of 0.1 Hz.
        overload = demand - self.capacity
        return self.nominal_frequency - (overload * 0.1)

    def get_price_signal(self) -> float:
        # Normal price is 15.0 pence per kWh
        # If frequency drops below 49.8 Hz, we are in danger! Price spikes to 100.0 p/kWh.
        if self.get_current_frequency() < 49.8:
            return 100.0
        return 15.0