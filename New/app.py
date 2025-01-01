import os
import csv
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Path to store the logs
log_file_path = os.path.join('track', 'availability_logs.csv')

# Ensure the 'track' directory exists
if not os.path.exists('track'):
    os.makedirs('track')

# Function to read logs from the CSV file
def read_logs():
    logs = []
    if os.path.exists(log_file_path):
        with open(log_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                logs.append(row)
    return logs

# Function to write a new log to the CSV file
def write_log(entry):
    fieldnames = ['employee_name', 'date', 'time_slot', 'status', 'timestamp']
    file_exists = os.path.exists(log_file_path)
    
    with open(log_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()  # Write header if the file is new
        
        writer.writerow(entry)

@app.route('/')
def index():
    # Read the existing logs
    availability_log = read_logs()
    return render_template('index.html', availability_log=availability_log, confirmation=None)

@app.route('/submit', methods=['POST'])
def submit():
    employee_name = request.form['employee_name']
    date = request.form['date']
    time_slot = request.form['time_slot']
    status = request.form['status']
    
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Create a new log entry
    log_entry = {
        'employee_name': employee_name,
        'date': date,
        'time_slot': time_slot,
        'status': status,
        'timestamp': timestamp
    }
    
    # Write the log entry to the CSV file
    write_log(log_entry)
    
    # Read the updated logs and pass them to the template
    availability_log = read_logs()
    
    # Redirect to the home page with confirmation
    return render_template('index.html', availability_log=availability_log, confirmation=True)

if __name__ == '__main__':
    app.run(debug=True)
