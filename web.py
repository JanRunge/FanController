from flask import Flask, Markup, render_template
from datetime import timezone, datetime
import database

db = database.connect()
app = Flask(__name__)

@app.route("/")
def hello_world():
    (values,labels) = get_data()
    
    return render_template('line_chart.html', title='Bitcoin Monthly Price in USD', max=100, labels=labels, values=values)

def get_data():
    temp_data = database.select(db, "select temperature, timestamp from temperature_log where timestamp > datetime('now','-2 day','localtime') order by timestamp asc")
    values = []
    labels = []
    for row in temp_data:
        val, timestamp = row
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamp_new = (timestamp - datetime(1970, 1, 1)).total_seconds()
        values.append(val)
        labels.append(labels)
    return (values,labels)
