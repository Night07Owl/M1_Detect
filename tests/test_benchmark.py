"""
Test Suite: System Monitor & Benchmark Aggregation
"""

from benchmark.system_monitor import SystemMonitor

def test_system_monitor_snapshot():
    sm = SystemMonitor()
    snap = sm.get_snapshot()
    sm.close()
    
    assert "system_cpu_percent" in snap
    assert "process_cpu_percent" in snap
    assert "system_ram_percent" in snap
    assert "process_ram_mb" in snap
    assert "gpu_name" in snap
    assert isinstance(snap["process_ram_mb"], float)
