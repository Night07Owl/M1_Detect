"""
System Telemetry & Hardware Resource Profiler
Monitors CPU, System RAM, Process Memory, GPU Utilization, VRAM, and Temperatures.
"""

import os
import sys
import psutil

try:
    import pynvml
    pynvml.nvmlInit()
    HAS_NVML = True
    NVML_HANDLE = pynvml.nvmlDeviceGetHandleByIndex(0)
    NVML_DEVICE_NAME = pynvml.nvmlDeviceGetName(NVML_HANDLE)
except Exception:
    HAS_NVML = False
    NVML_HANDLE = None
    NVML_DEVICE_NAME = "Unavailable"

class SystemMonitor:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        # Prime psutil cpu measurement
        psutil.cpu_percent(interval=None)
        self.process.cpu_percent(interval=None)

    def get_snapshot(self):
        """Capture an instantaneous snapshot of system and process resource utilization."""
        # CPU Metrics
        sys_cpu = psutil.cpu_percent(interval=None)
        proc_cpu = self.process.cpu_percent(interval=None)
        
        # RAM Metrics
        vm = psutil.virtual_memory()
        proc_mem = self.process.memory_info()
        proc_ram_mb = proc_mem.rss / (1024 * 1024)
        sys_ram_percent = vm.percent
        sys_ram_used_mb = vm.used / (1024 * 1024)
        
        # GPU Metrics via NVML
        gpu_util = None
        gpu_mem_used_mb = None
        gpu_temp = None
        gpu_power_w = None
        
        if HAS_NVML and NVML_HANDLE is not None:
            try:
                util = pynvml.nvmlDeviceGetUtilizationRates(NVML_HANDLE)
                mem = pynvml.nvmlDeviceGetMemoryInfo(NVML_HANDLE)
                temp = pynvml.nvmlDeviceGetTemperature(NVML_HANDLE, pynvml.NVML_TEMPERATURE_GPU)
                power = pynvml.nvmlDeviceGetPowerUsage(NVML_HANDLE) / 1000.0  # mW to W
                
                gpu_util = float(util.gpu)
                gpu_mem_used_mb = round(float(mem.used / (1024 * 1024)), 1)
                gpu_temp = float(temp)
                gpu_power_w = round(float(power), 1)
            except Exception:
                pass
                
        # CPU Temperature where accessible
        cpu_temp = None
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if entries:
                            cpu_temp = entries[0].current
                            break
        except Exception:
            pass

        return {
            "system_cpu_percent": sys_cpu,
            "process_cpu_percent": proc_cpu,
            "system_ram_percent": sys_ram_percent,
            "system_ram_used_mb": round(sys_ram_used_mb, 1),
            "process_ram_mb": round(proc_ram_mb, 1),
            "gpu_name": NVML_DEVICE_NAME,
            "gpu_utilization_percent": gpu_util if gpu_util is not None else "Unavailable",
            "gpu_memory_used_mb": gpu_mem_used_mb if gpu_mem_used_mb is not None else "Unavailable",
            "gpu_temperature_c": gpu_temp if gpu_temp is not None else "Unavailable",
            "gpu_power_watts": gpu_power_w if gpu_power_w is not None else "Unavailable",
            "cpu_temperature_c": cpu_temp if cpu_temp is not None else "Unavailable (OS restriction)"
        }

    def close(self):
        if HAS_NVML:
            try:
                pynvml.nvmlShutdown()
            except Exception:
                pass

