import os

import pandas as pd
import time
from process_monitor.helper_functions import create_data_csv_files, get_current_time, print_processes_data_as_a_table, \
    load_config
from process_monitor.mysql_db import DatabaseManager
from process_monitor.process import ProcessMonitor


def start_monitoring(monitoring_interval_in_second, monitoring_duration_in_second):
    start_time = get_current_time()
    while (get_current_time() - start_time).seconds < monitoring_duration_in_second:
        print(f"\n\n----------------------------Start Monitoring {start_time}----------------------------\n\n")
        time.sleep(monitoring_interval_in_second)
        processes = process.get_all_running_processes(name_to_exclude=processes_to_exclude)
        print(f"\n\n----------------------------Monitoring After 5 seconds----------------------------\n\n")

        print_processes_data_as_a_table(processes)
        create_data_csv_files(processes, output_csv_file=output_csv_file)
    finish_time = get_current_time()
    return start_time, finish_time


def summarize_data(start_monitoring_time, end_monitoring_time):
    df = pd.read_csv(output_csv_file)
    grouped = df.groupby(['process_id', 'process_name']).agg({
        'cpu_percent': 'mean',
        'memory_usage': 'mean'
    }).reset_index()
    grouped = grouped.rename(columns={
        'cpu_percent': 'Average CPU %',
        'memory_usage': 'Average Memory (MB)'
    })
    grouped['start_time'] = start_monitoring_time
    grouped['end_time'] = end_monitoring_time
    mysql_db.insert_summary_data(grouped)


if __name__ == "__main__":
    config = load_config('process_monitor/config.json')
    monitoring_interval = config.get("monitoring_interval", 5)
    monitoring_duration = config.get("monitoring_duration", 60)
    processes_to_exclude = config.get("processes_to_exclude", [])
    output_csv_file = config.get("data_file_name", 60)
    processes_details = config.get("processes_details", ["PID", "Process Name", "CPU %", "Memory (MB)", "Timestamp"])

    if os.path.exists(output_csv_file):
        os.remove(output_csv_file)

    process = ProcessMonitor()

    db_config = config["db"]
    mysql_db = DatabaseManager(db_config)
    mysql_db.connect()

    start_time_monitoring, finish_time_monitoring = start_monitoring(monitoring_interval, monitoring_duration)
    summarize_data(start_time_monitoring, finish_time_monitoring)

    mysql_db.commit()

    mysql_db.close()
