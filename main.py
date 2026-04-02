from appliance import Appliance, Priority
from home import SmartHome
from grid import Grid


def run_simulation():
    print("Initializing Smart Grid Balancer...\n")

    uk_grid = Grid(initial_capacity=10.0)
    my_home = SmartHome(home_id="House_001")
    uk_grid.add_home(my_home)

    charger = Appliance(name="EV charger", power_draw=7.2, priority=Priority.LOW)
    oven = Appliance(name="Oven", power_draw=3.0, priority=Priority.HIGH)
    fridge = Appliance(name="Fridge", power_draw=0.8, priority=Priority.CRITICAL)

    my_home.add_appliance(charger)
    my_home.add_appliance(oven)
    my_home.add_appliance(fridge)

    fridge.turn_on()

    print("MORNING: (Low Demand, High Solar")
    print(f"Grid Capacity: {uk_grid.capacity}kW")
    print(f"Total Demand: {uk_grid.get_total_demand()}")
    print(f"Grid Frequency:{uk_grid.get_current_frequency()}Hz")
    print(f"Current Price:{uk_grid.get_price_signal()}p/kWh")

    input("\n[Press Enter to advance to Evening Peak...]")

    print("EVENING PEAK (The Duck Curve strikes)")
    print("Sun goes down. Solar drops off.")
    print("Homeowner plugs in the EV and turns on the oven.")

    uk_grid.capacity = 5.0
    charger.turn_on()
    oven.turn_on()

    current_freq = uk_grid.get_current_frequency()
    print(f"Grid Frequency drops to: {current_freq} Hz")

    current_price = uk_grid.get_price_signal()
    print(f"📈 Price spikes to: {current_price} p/kWh")

    input("\n[Press Enter to broadcast price signal to homes...]")

    print("AUTONOMOUS INTERVENTION")
    my_home.react_to_price(current_price)

    print("TICK 4: STABILIZATION")
    print(f"Total Demand is now: {uk_grid.get_total_demand()} kW")
    print(f"Grid Frequency recovers to: {uk_grid.get_current_frequency()} Hz")
    print(f"Current Price normalizes to: {uk_grid.get_price_signal()} p/kWh")


if __name__ == "__main__":
    run_simulation()
