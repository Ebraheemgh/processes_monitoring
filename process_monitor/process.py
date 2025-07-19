import random

import psutil

from process_monitor.helper_functions import get_current_time


class ProcessMonitor:
    def get_all_running_processes(self, name_to_exclude=None):
        if name_to_exclude is None:
            name_to_exclude = []

        processes_table_data = []
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            try:
                if any(ex.lower() in proc.info['name'].lower() for ex in name_to_exclude):
                    continue

                cpu_percent = self.get_cpu_percent_for_specific_process(proc)
                memory_usage = self.get_memory_usage_from_process(proc)
                timestamp = get_current_time()

                processes_table_data.append({
                    "process_id": proc.info['pid'],
                    "process_name": proc.info['name'],
                    "cpu_percent": cpu_percent,
                    "memory_usage": memory_usage,
                    "timestamp": timestamp}
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        return processes_table_data

    @staticmethod
    def get_memory_usage_from_process(process):
        if type(process) == psutil.Process:
            try:
                mem_info = process.memory_info()
                memory_mb = mem_info.rss / (1024 * 1024)
                return memory_mb
            except psutil.NoSuchProcess:
                print(f"Process no longer exists")
                return None
        elif type(process) == dict:
            cpu = process['memory_usage']
        else:
            return None
        return cpu

    @staticmethod
    def get_cpu_percent_for_specific_process(process):
        if type(process) == psutil.Process:
            cpu = process.cpu_percent(interval=None)
        elif type(process) == dict:
            cpu = process['cpu_percent']
        else:
            return None
        return cpu

    def get_random_process(self):
        return random.choice(self.get_all_running_processes())
