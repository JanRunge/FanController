##creates the initial DB
import database

temp_log = """DROP TABLE temperature_log;"""
fan_log = """DROP TABLE fan_log;"""

con = database.connect()
database.execute_query(con, temp_log)
database.execute_query(con, fan_log)