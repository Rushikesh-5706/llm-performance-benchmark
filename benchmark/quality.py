from typing import Dict


def compute_quality_metrics(text: str) -> Dict[str, float]:
    tokens = text.split()
    total_tokens = len(tokens)
    unique_tokens = len(set(tokens))

    diversity = (
        unique_tokens / total_tokens if total_tokens > 0 else 0.0
    )

    return {
        "output_length": total_tokens,
        "vocab_diversity": diversity
    }

