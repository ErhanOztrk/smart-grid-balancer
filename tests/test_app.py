import pytest
import pandas as pd
from unittest.mock import patch
from app import fetch_data

# TEST 1: Does it handle a database crash gracefully?
@patch('app.psycopg2.connect') # Intercept the database connection
def test_fetch_data_graceful_failure(mock_connect):
    # 1. ARRANGE: Tell the stunt double to simulate a database crash
    mock_connect.side_effect = Exception("Simulated DB Timeout")
    
    # 2. ACT: Call the function
    result_df = fetch_data("SELECT * FROM grid_telemetry")
    
    # 3. ASSERT: Prove it returned an empty DataFrame instead of crashing
    assert isinstance(result_df, pd.DataFrame)
    assert result_df.empty is True

# TEST 2: Does it fetch data correctly when the DB is working?
@patch('app.pd.read_sql')      # Intercept Pandas reading SQL
@patch('app.psycopg2.connect') # Intercept the database connection
def test_fetch_data_success(mock_connect, mock_read_sql):
    # 1. ARRANGE: Create fake data for the stunt double to return
    fake_data = pd.DataFrame({
        'timestamp': ['2026-08-03 10:00:00'],
        'total_demand_kw': [50.5]
    })
    mock_read_sql.return_value = fake_data
    
    # 2. ACT: Call the function
    result_df = fetch_data("SELECT * FROM grid_telemetry")
    
    # 3. ASSERT: Prove the function returns the data correctly
    assert not result_df.empty
    assert result_df['total_demand_kw'].iloc[0] == 50.5