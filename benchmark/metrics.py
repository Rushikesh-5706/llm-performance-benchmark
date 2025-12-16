import psutil
import os
import time

try:
    import pynvml
    pynvml.nvmlInit()
    GPU_AVAILABLE = True
except Exception:
    GPU_AVAILABLE = False


class PerformanceMonitor:
    def __init__(self):
        self.process = psutil.Process(os.getpid())

    def get_ram_usage_mb(self) -> float:
        return self.process.memory_info().rss / (1024 ** 2)

    def get_gpu_memory_mb(self) -> float:
        if not GPU_AVAILABLE:
            return 0.0

        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return mem_info.used / (1024 ** 2)

    def monitor(self, func, *args, **kwargs) -> dict:
        ram_before = self.get_ram_usage_mb()
        gpu_before = self.get_gpu_memory_mb()

        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        ram_after = self.get_ram_usage_mb()
        gpu_after = self.get_gpu_memory_mb()

        return {
            "result": result,
            "peak_ram_mb": max(ram_before, ram_after),
            "peak_gpu_mb": max(gpu_before, gpu_after),
            "wall_time": end_time - start_time
        }

