import speedtest
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


def log_network_speed():
    with open(RESULTS_FILE, "a") as file:
        now = datetime.now()
        test_results = internet_test()
        file.write(f'{now.strftime("%b %m")}, {now.strftime("%H:%M")}, {test_results[0]}, {test_results[1]}, {test_results[2]}\n')
        print(f'Results: {now.strftime("%b %m")}, {now.strftime("%H:%M")}, {test_results[0]}, {test_results[1]}, {test_results[2]}')



def check_file():
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "a") as file:
            file.write(f'Date, Time, Ping, Download, Upload')


def monitor_network():
    interval = timedelta(minutes=TIME_INTERVAL)
    next_run = datetime.now()
    iteration = 0

    while True:
        now = datetime.now()
        if now >= next_run:
            print(f'Testing Network: #{iteration}')
            log_network_speed()
            iteration += 1
            next_run += interval
        
        sleep_time = (next_run - datetime.now()).total_seconds()
        if sleep_time > 0:
            print("Sleeping")
            time.sleep(sleep_time)


def main():
    check_file()
    monitor_network()


if __name__ == "__main__":
    main()
