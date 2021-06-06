from flask import Flask
from datetime import timezone, datetime
import database

db = database.connect()
app = Flask(__name__)

@app.route("/")
def hello_world():
    data = get_data()
    val, ts = data[0]
    str = f"{val}, {ts}"
    return str

def get_data():
    temp_data = database.select(db, "select temperature, timestamp from temperature_log where timestamp > datetime('now','-2 day','localtime') order by timestamp asc")
    result = []
    for row in temp_data:
        val, timestamp = row
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamp_new = (timestamp - datetime(1970, 1, 1)).total_seconds()
        result.append((val, timestamp_new))
    return result
