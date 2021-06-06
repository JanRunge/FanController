##creates the initial DB
import database

temp_log = """CREATE TABLE IF NOT EXISTS temperature_log (
  temperature REAL
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);"""
fan_log = """CREATE TABLE IF NOT EXISTS fan_log (
  power REAL
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);"""

con = database.connect()
database.execute_query(con, temp_log)
database.execute_query(con, fan_log)