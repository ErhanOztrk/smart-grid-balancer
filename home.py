from typing import List
from appliance import Appliance, Priority

class SmartHome:
    def __init__(self, home_id: str):
        self.home_id = home_id
        self.appliances: List[Appliance] = []

    def add_appliance(self, appliance: Appliance):
        self.appliances.append(appliance)
    
    def get_current_load(self) -> float:
        total_load = 0.0
        for appliance in self.appliances:
            if appliance.is_on:
                total_load += appliance.power_draw
        
        return total_load
    
    def react_to_price(self, current_price: float):
        if current_price > 30.0:
            print(f"\n[{self.home_id}] PRICE SPIKE DETECTED ({current_price}p)! Initiating load shedding...")
            for appliance in self.appliances:
                    if appliance.priority == Priority.LOW and appliance.is_on:
                        appliance.turn_off()
                        print(f"[{self.home_id}] Turned off: {appliance.name} to save money")