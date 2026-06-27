import pandas as pd
import psycopg2
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Energy Risk Engine", page_icon="⚡", layout="wide")

# --- DATABASE CONNECTION ---
# We use st.cache_data so Streamlit doesn't open a new connection on every single click
@st.cache_data(ttl=5) # Refreshes data every 5 seconds
def fetch_data(query):
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="postgres",
            user="postgres",
            password="fintech", 
            port="5432"
        )
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return pd.DataFrame()

# --- FETCH THE DATA ---
telemetry_df = fetch_data("SELECT * FROM grid_telemetry ORDER BY timestamp ASC")
audit_df = fetch_data("SELECT * FROM risk_mitigation_log ORDER BY timestamp DESC")

# --- UI HEADER ---
st.title("⚡ Predictive Energy Trading & Risk Dashboard")
st.markdown("Real-time telemetry and automated risk mitigation ledger.")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("Simulation Settings")
    st.markdown("Adjust parameters to test system volatility.")
    
    selected_node = st.selectbox(
        "Select Simulation Node:",
        ["Primary Grid", "Substation Alpha", "House Level Log"]
    )
    
    risk_threshold = st.number_input(
        "Set Critical Risk Threshold (p/kWh):", 
        min_value=10.0, 
        max_value=100.0, 
        value=30.0,
        step=1.0
    )
    
    st.divider()
    
    trigger_action = st.button("Force Emergency Stop-Loss", type="primary")
    
    # NEW LOGIC: Wire up the button to write to the database
    if trigger_action:
        try:
            # Connect to PostgreSQL using your existing parameters
            conn = psycopg2.connect(
                host="127.0.0.1",
                database="postgres",
                user="postgres",
                password="fintech", 
                port="5432"
            )
            cursor = conn.cursor()
            
            # Insert a manual override event into the audit log
            query = """
            INSERT INTO risk_mitigation_log (home_id, appliance_name, action_taken, money_saved_estimate, trigger_price_p_kwh)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, ("SYSTEM_OVERRIDE", "All Non-Critical", "EMERGENCY_SHUTDOWN", 0.0, risk_threshold))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            # Clear the cache so Streamlit fetches the new data instantly
            fetch_data.clear()
            st.success("Emergency Stop-Loss Executed!")
            st.rerun() # Instantly refresh the UI to show the new row
            
        except Exception as e:
            st.error(f"Failed to execute emergency override: {e}")

# --- TOP METRICS ROW ---
if not telemetry_df.empty:
    latest_data = telemetry_df.iloc[-1] # Get the most recent row
    
    # --- AI PREDICTIVE LOGIC ---
    # Calculate demand trend over the last 3 ticks to forecast risk
    if len(telemetry_df) >= 3:
        demand_trend = telemetry_df['total_demand_kw'].diff().tail(3).mean()
        utilization = latest_data['total_demand_kw'] / latest_data['grid_capacity_kw']
        
        # Heuristic algorithm to simulate AI risk confidence
        base_risk = utilization * 60
        trend_multiplier = max(0, demand_trend * 15)
        ai_risk_score = min(99.9, base_risk + trend_multiplier)
    else:
        ai_risk_score = 5.0
        
    risk_label = "⚠️ High Risk" if ai_risk_score > 75 else "✅ Stable"
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Grid Frequency", f"{latest_data['grid_frequency_hz']} Hz")
    col2.metric("Market Price", f"{latest_data['current_price_p_kwh']} p/kWh", delta="Spike" if latest_data['current_price_p_kwh'] > 30 else "Normal", delta_color="inverse")
    col3.metric("Total Demand", f"{latest_data['total_demand_kw']} kW")
    col4.metric("System Status", latest_data['status'])
    col5.metric("AI Risk Forecast", f"{ai_risk_score:.1f}%", risk_label, delta_color="inverse" if ai_risk_score > 75 else "normal")

    # --- CHARTS ---
    st.divider()
    st.subheader("📈 Market Price vs Grid Frequency")
    
    # Professional Dual-Axis Chart using Plotly
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=telemetry_df['timestamp'], y=telemetry_df['current_price_p_kwh'], name="Market Price (p/kWh)", line=dict(color="#FF4B4B", width=3)),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=telemetry_df['timestamp'], y=telemetry_df['grid_frequency_hz'], name="Grid Frequency (Hz)", line=dict(color="#1F77B4", width=3, dash="dot")),
        secondary_y=True,
    )
    
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0), hovermode="x unified")
    fig.update_yaxes(title_text="Price", secondary_y=False)
    fig.update_yaxes(title_text="Frequency", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

# --- AUDIT LOG ---
st.divider()
st.subheader("🛡️ Automated Risk Mitigation Ledger")
st.markdown("Immutable audit trail of autonomous load-shedding events executed to minimize financial exposure.")

if not audit_df.empty:
    # Display the dataframe cleanly
    st.dataframe(audit_df, use_container_width=True)
else:
    st.info("No risk mitigation events have been triggered yet.")