from flask import Flask, render_template
import re
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

app = Flask(__name__)
LOG_FILE = '/shared_logs/log'  # Volume mount

def parse_logs():
    hosts = {}
    if not os.path.exists(LOG_FILE):
        return hosts

    with open(LOG_FILE, 'r') as f:
        for line in f:
            try:
                line = line.strip()
                if not line:
                    continue

                # Parse lines like:
                # file_created_by_192.168.0.111_2025-04-06_14-42-55.txt
                if not line.endswith('.txt'):
                    continue

                line_core = line[:-4]  # видаляємо ".txt"
                parts = line_core.split('_')

                if len(parts) < 6:
                    continue

                host = parts[3]  # 192.168.0.111
                date = parts[4]  # 2025-04-06
                time = parts[5]  # 14-42-55

                timestamp = datetime.strptime(f"{date}_{time}", '%Y-%m-%d_%H-%M-%S')
                filename = line

                if host not in hosts:
                    hosts[host] = []

                hosts[host].append({
                    'filename': filename,
                    'timestamp': timestamp
                })

            except Exception as e:
                print(f"Failed to parse line: {line} - Error: {str(e)}")
                continue

    return hosts

def generate_plots(hosts):
    if not hosts:
        return []
    # Prepare data
    timestamps = []
    for host_data in hosts.values():
        timestamps.extend([entry['timestamp'] for entry in host_data])

    # Plot 1: Records per host
    plt.figure(1)
    plt.bar(hosts.keys(), [len(v) for v in hosts.values()])
    plt.title('Records per Host')
    plt.xticks(rotation=45)
    buf1 = BytesIO()
    plt.savefig(buf1, format='png')
    plt.close(1)

    # Plot 2: Records per hour
    plt.figure(2)
    hours = [t.hour for t in timestamps]
    plt.hist(hours, bins=24, range=(0,24))
    plt.title('Records per Hour')
    buf2 = BytesIO()
    plt.savefig(buf2, format='png')
    plt.close(2)

    # Plot 3: Records per day
    plt.figure(3)
    days = [t.strftime('%Y-%m-%d') for t in timestamps]
    plt.hist(days, bins=len(set(days)))
    plt.title('Records per Day')
    plt.xticks(rotation=45)
    buf3 = BytesIO()
    plt.savefig(buf3, format='png')
    plt.close(3)

    return [
        base64.b64encode(buf1.getvalue()).decode('utf-8'),
        base64.b64encode(buf2.getvalue()).decode('utf-8'),
        base64.b64encode(buf3.getvalue()).decode('utf-8')
    ]

@app.route('/')
def index():
    hosts = parse_logs()
    plots = generate_plots(hosts) if hosts else []
    return render_template('index.html', hosts=hosts, plots=plots)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
