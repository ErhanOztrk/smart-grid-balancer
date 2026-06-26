import time
from appliance import Appliance, Priority
from home import SmartHome
from grid import Grid
from database import DatabaseManager

def run_simulation():
    print("Initializing Smart Grid Balancer...\n")
    
    # 1. Initialize Database Connection
    db = DatabaseManager()
    db.create_tables()

    # 2. Setup Physical Grid and Home
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
    
    # --- CRITERIA 2.3: ITERATION (LOOPING) ---
    # We loop through 3 simulated days of grid activity
    for day in range(1, 4):
        print(f"\n========== STARTING DAY {day} ==========")
        
        # --- TICK 1: MORNING ---
        print("\n--- MORNING: (Low Demand, High Solar) ---")
        uk_grid.capacity = 10.0
        charger.turn_off() # Reset from previous evening
        oven.turn_off()
        
        # Log State to Database
        db.log_telemetry(
            demand=uk_grid.get_total_demand(),
            capacity=uk_grid.capacity,
            frequency=uk_grid.get_current_frequency(),
            price=uk_grid.get_price_signal(),
            status="STABLE"
        )
        time.sleep(3) # Pause for 3 seconds so dashboard can update

        # --- TICK 2: EVENING PEAK ---
        print("\n--- EVENING PEAK (The Duck Curve strikes) ---")
        uk_grid.capacity = 5.0
        charger.turn_on()
        oven.turn_on()

        current_freq = uk_grid.get_current_frequency()
        current_price = uk_grid.get_price_signal()

        # Log Crisis State to Database
        db.log_telemetry(
            demand=uk_grid.get_total_demand(),
            capacity=uk_grid.capacity,
            frequency=current_freq,
            price=current_price,
            status="CRITICAL SPIKE" if current_price > 30.0 else "WARNING"
        )
        time.sleep(3)

        # --- TICK 3: AUTONOMOUS INTERVENTION ---
        print("\n--- AUTONOMOUS INTERVENTION ---")
        my_home.react_to_price(current_price)
        
        # Audit Log: Record the automated mitigation action
        if current_price > 30.0:
            db.log_risk_action(
                home_id=my_home.home_id,
                appliance_name=charger.name,
                action="SHED_LOAD",
                savings=current_price * charger.power_draw, 
                trigger_price=current_price
            )
        time.sleep(3)

        # --- TICK 4: STABILIZATION ---
        print("\n--- TICK 4: STABILIZATION ---")
        # Log Recovered State to Database
        db.log_telemetry(
            demand=uk_grid.get_total_demand(),
            capacity=uk_grid.capacity,
            frequency=uk_grid.get_current_frequency(),
            price=uk_grid.get_price_signal(),
            status="STABLE"
        )
        time.sleep(3)

    db.close()
    print("\n✅ 3-Day Simulation complete. All data securely logged to PostgreSQL.")

if __name__ == "__main__":
    run_simulation()