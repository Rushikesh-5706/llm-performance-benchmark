import json
from pathlib import Path
from typing import List


def load_prompts(dataset_path: str) -> List[str]:
    path = Path(dataset_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

    prompts = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # skip empty lines safely

            record = json.loads(line)
            prompts.append(record["prompt"])

    return prompts

