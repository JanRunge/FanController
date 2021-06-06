from flask import Flask
from datetime import timezone
import database

db = database.connect()
app = Flask(__name__)

@app.route("/")
def hello_world():
    data = get_data()
    val, ts = data[0]
    str = f"{val}, {ts}"
    return "<p>Hello, World!</p>"

def get_data():
    temp_data = database.select(db, "select * from temperature_log where timestamp < datetime('now','-2 day','localtime') order by timestamp asc")
    result = []
    for row in temp_data:
        val, timestamp = row
        timestamp = timestamp.replace(tzinfo=timezone.utc).timestamp()
        result.append((val, timestamp))
