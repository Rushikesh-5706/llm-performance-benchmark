import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def generate_plots(results_csv: str, output_dir: str):
    df = pd.read_csv(results_csv)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Average latency per model
    latency = df.groupby("model")["latency_sec"].mean()
    latency.plot(kind="bar", title="Average Latency per Model")
    plt.ylabel("Latency (seconds)")
    plt.tight_layout()
    plt.savefig(output_path / "latency_comparison.png")
    plt.clf()

    # Average peak RAM usage per model
    memory = df.groupby("model")["peak_ram_mb"].mean()
    memory.plot(kind="bar", title="Average Peak RAM Usage per Model")
    plt.ylabel("RAM (MB)")
    plt.tight_layout()
    plt.savefig(output_path / "memory_usage.png")
    plt.clf()

