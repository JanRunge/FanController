import database


con = database.connect()
rows = database.select(con, "select * from temperature_log")
for row in rows:
    (val, time) = row
    print(val, time)