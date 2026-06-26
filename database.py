import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        # These match the environment variables we set in the Docker command
        self.conn_params = {
            "host": "127.0.0.1",
            "database": "postgres",  # Changed to use the default built-in database
            "user": "postgres",  # Changed from admin to the default postgres superuser
            "password": "fintech",
            "port": "5432"
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establishes connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            # RealDictCursor allows us to access column data by name (like a dictionary)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("✅ Successfully connected to PostgreSQL Database.")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("   (Did you remember to start your Docker container?)")

    def create_tables(self):
        """Initializes the database schema for the risk simulator."""
        if not self.conn:
            self.connect()

        if not self.cursor:
            print("❌ Aborting table creation due to connection failure.")
            return

        # SQL to create our two core tables
        create_telemetry_table = """
        CREATE TABLE IF NOT EXISTS grid_telemetry (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_demand_kw NUMERIC(10, 2),
            grid_capacity_kw NUMERIC(10, 2),
            grid_frequency_hz NUMERIC(5, 2),
            current_price_p_kwh NUMERIC(10, 2),
            status VARCHAR(50)
        );
        """

        create_audit_log_table = """
        CREATE TABLE IF NOT EXISTS risk_mitigation_log (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            home_id VARCHAR(50),
            appliance_name VARCHAR(50),
            action_taken VARCHAR(50),
            money_saved_estimate NUMERIC(10, 2),
            trigger_price_p_kwh NUMERIC(10, 2)
        );
        """

        try:
            self.cursor.execute(create_telemetry_table)
            self.cursor.execute(create_audit_log_table)
            self.conn.commit() # Save the changes
            print("✅ Database tables initialized successfully.")
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
            self.conn.rollback()

    def log_telemetry(self, demand, capacity, frequency, price, status):
        """Inserts a 'tick' of the system state into the database."""
        if not self.cursor:
            print("⚠️ Skipped logging telemetry: No database connection.")
            return
            
        query = """
        INSERT INTO grid_telemetry (total_demand_kw, grid_capacity_kw, grid_frequency_hz, current_price_p_kwh, status)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (demand, capacity, frequency, price, status))
            self.conn.commit()
        except Exception as e:
            print(f"Error logging telemetry: {e}")
            self.conn.rollback()

    def log_risk_action(self, home_id, appliance_name, action, savings, trigger_price):
        """Creates an audit record when the system intervenes."""
        if not self.cursor:
            print("⚠️ Skipped logging risk action: No database connection.")
            return
            
        query = """
        INSERT INTO risk_mitigation_log (home_id, appliance_name, action_taken, money_saved_estimate, trigger_price_p_kwh)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (home_id, appliance_name, action, savings, trigger_price))
            self.conn.commit()
        except Exception as e:
            print(f"Error logging risk action: {e}")
            self.conn.rollback()

    def close(self):
        """Closes the database connection cleanly."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("🔌 Database connection closed.")

# --- Test Block (Only runs if you execute this specific file) ---
if __name__ == "__main__":
    db = DatabaseManager()
    db.create_tables()
    
    # Let's insert a fake test row to prove it works
    db.log_telemetry(demand=8.5, capacity=10.0, frequency=50.0, price=15.0, status="STABLE")
    print("✅ Test row sequence finished.")
    db.close()