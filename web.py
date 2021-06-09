from flask import Flask, Markup, render_template
from datetime import timezone, datetime
import database

db = database.connect()
app = Flask(__name__)

@app.route("/")
def hello_world():
    (temp_values,temp_labels) = get_temp_data()
    (fan_values,fan_labels) = get_fan_data()
    return render_template('line_chart.html', title='All the info', max=50, labels=temp_labels, values=temp_values, max2=1, labels2=fan_labels, values2=fan_values)

def get_temp_data():
    temp_data = database.select(db, "select temperature, timestamp from temperature_log where timestamp > datetime('now','-2 day','localtime') order by timestamp asc")
    values = []
    labels = []
    for row in temp_data:
        process_row(row, values, labels)
    return (values,labels)

def get_fan_data():
    temp_data = database.select(db, "select power, timestamp from fan_log where timestamp > datetime('now','-2 day','localtime') order by timestamp asc")
    values = []
    labels = []
    for row in temp_data:
        process_row(row, values, labels)
    return (values,labels)

def process_row(row, values, labels):
    val, timestamp = row
    timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    timestamp_new = (timestamp - datetime(1970, 1, 1)).total_seconds()
    values.append(val)
    labels.append(timestamp)