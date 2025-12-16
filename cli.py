import argparse
import pandas as pd
from tqdm import tqdm

from benchmark.config_loader import load_config
from benchmark.data_loader import load_prompts
from benchmark.model_runner import ModelRunner
from benchmark.metrics import PerformanceMonitor
from benchmark.quality import compute_quality_metrics


def main():
    parser = argparse.ArgumentParser(
        description="LLM Performance Benchmarking Tool"
    )
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to benchmark configuration file"
    )

    args = parser.parse_args()

    config = load_config(args.config)
    prompts = load_prompts(config["dataset"]["path"])

    results = []
    monitor = PerformanceMonitor()

    for model_cfg in config["models"]:
        model_name = model_cfg["name"]
        max_tokens = model_cfg["max_tokens"]

        print(f"\nBenchmarking model: {model_name}")
        runner = ModelRunner(
            model_name=model_name,
            device=config.get("device", "auto")
        )

        for prompt in tqdm(prompts, desc=f"{model_name}"):
            monitored = monitor.monitor(
                runner.run, prompt, max_tokens
            )

            run_result = monitored["result"]
            quality = compute_quality_metrics(run_result["text"])

            throughput = (
                run_result["tokens_generated"] / run_result["latency"]
                if run_result["latency"] > 0 else 0.0
            )

            results.append({
                "model": model_name,
                "prompt": prompt,
                "latency_sec": run_result["latency"],
                "throughput_tps": throughput,
                "tokens_generated": run_result["tokens_generated"],
                "peak_ram_mb": monitored["peak_ram_mb"],
                "peak_gpu_mb": monitored["peak_gpu_mb"],
                "output_length": quality["output_length"],
                "vocab_diversity": quality["vocab_diversity"]
            })

    df = pd.DataFrame(results)
    output_path = config["output"]["results_file"]
    df.to_csv(output_path, index=False)

    print("\nBenchmark completed successfully.")
    print("\nSummary (average per model):")
    print(
        df.groupby("model")[
            ["latency_sec", "throughput_tps", "peak_ram_mb"]
        ].mean()
    )


if __name__ == "__main__":
    main()

