import unittest
from process_monitor.process import ProcessMonitor


class TestProcessMonitor(unittest.TestCase):

    def test_get_all_running_processes(self):
        monitor = ProcessMonitor()
        processes = monitor.get_all_running_processes()
        assert type(processes) == list, f"Expected list but got {type(processes)}"

    def test_get_all_running_processes_with_exclude(self):
        processes_to_exclude = ["Chrome"]
        monitor = ProcessMonitor()
        processes = monitor.get_all_running_processes(name_to_exclude=processes_to_exclude)
        assert type(processes) == list, f"Expected list but got {type(processes)}"
        for proc_name in processes_to_exclude:
            assert proc_name not in [d['process_name'] for d in processes if
                                     'process_name' in d], f"{proc_name} should be excluded"

    def test_get_cpu_percent_for_process(self):
        monitor = ProcessMonitor()
        random_process = monitor.get_random_process()
        cpu = monitor.get_cpu_percent_for_specific_process(random_process)
        assert isinstance(cpu, float), f"CPU percent should be float but got {type(cpu)}"

    def test_get_memory_usage_for_first_process(self):
        monitor = ProcessMonitor()
        random_process = monitor.get_random_process()
        memory = monitor.get_memory_usage_from_process(random_process)
        assert isinstance(memory, float), f"Memory usage should be float but got {type(memory)}"


if __name__ == '__main__':
    unittest.main()
