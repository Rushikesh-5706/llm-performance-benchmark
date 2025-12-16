import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class ModelRunner:
    def __init__(self, model_name: str, device: str = "auto"):
        self.model_name = model_name

        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

    def run(self, prompt: str, max_tokens: int) -> dict:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        start_time = time.perf_counter()

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=False
            )

        end_time = time.perf_counter()

        generated_text = self.tokenizer.decode(
            outputs[0], skip_special_tokens=True
        )

        num_tokens = outputs.shape[-1] - inputs["input_ids"].shape[-1]

        return {
            "text": generated_text,
            "latency": end_time - start_time,
            "tokens_generated": num_tokens
        }

