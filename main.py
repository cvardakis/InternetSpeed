import speedtest
import sys
import json
import subprocess
import time
from datetime import datetime, timedelta
import os

RESULTS_FILE = "results.csv"
TIME_INTERVAL = 1

def internet_test():
    st = speedtest.Speedtest()
    st.get_best_server()  # Triggers ping and selects best server
    ping = st.results.ping
    download = round(st.download() / 1_000_000, 2)  # Mbps
    upload = round(st.upload() / 1_000_000, 2)      # Mbps
    return ping, download, upload


def cli_internet_test():
    try:
        output = subprocess.check_output(["speedtest", "--json"], text=True)
        data = json.loads(output)
        ping = data["ping"]
        download = round(data["download"] / 1_000_000, 2)  # Mbps
        upload = round(data["upload"] / 1_000_000, 2)      # Mbps
        return ping, download, upload
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Failed CLI SpeedTest")


def log_network_speed(mode):
    with open(RESULTS_FILE, "a") as file:
        try:
            now = datetime.now()
            if mode == 0:
                print("Testing with python package")
                test_results = internet_test()
            elif mode == 1:
                print("Testing with CLI")
                test_results = cli_internet_test()
            else:
                raise RuntimeError(f"Invalid Mode Provided: {mode}")
        
            file.write(f'{now.strftime("%b %m")}, {now.strftime("%H:%M")}, {test_results[0]}, {test_results[1]}, {test_results[2]}\n')
            print(f'Results: {now.strftime("%b %m")}, {now.strftime("%H:%M")}, {test_results[0]}, {test_results[1]}, {test_results[2]}')
        
        except:
            raise RuntimeError(f'Failed to collect data')

def check_file():
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "a") as file:
            file.write(f'Date, Time, Ping, Download, Upload\n')


def monitor_network(mode):
    interval = timedelta(minutes=TIME_INTERVAL)
    next_run = datetime.now()
    iteration = 0

    while True:
        now = datetime.now()
        if now >= next_run:
            print(f'Testing Network: #{iteration}')
            log_network_speed(mode)
            iteration += 1
            next_run += interval
        
        sleep_time = (next_run - datetime.now()).total_seconds()
        if sleep_time > 0:
            print("Sleeping")
            time.sleep(sleep_time)


def main():
    mode = int(sys.argv[1])
    check_file()
    monitor_network(mode)


if __name__ == "__main__":
    main()
