from typing import List
from home import SmartHome

class Grid:
    def __init__(self, initial_capacity: float):
        self.capacity = initial_capacity
        self.homes: List[SmartHome] = []
        self.nominal_frequency = 50.0

        def add_home(self, home:SmartHome):
            self.homes.append(home)

        def get_total_demand(self) -> float:
            total_demand =0.0

            for home in self.homes:
                total_demand += home.get_current_load()
            return total_demand
        
        def get_current_frequency(self) -> float:
            demand = self.get_total_demand()

            if demand <= self.capacity:
                return self.nominal_frequency
            overload = demand - self.capacity
            return self.nominal_frequency - (overload*0.1)
        
        def get_price_signals(self) -> float:
            if self.get_current_frequency() < 49.8:
                return 100.0
            return 15.0