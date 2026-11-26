import json
from statistics import median
from time import perf_counter
from urllib.request import Request, urlopen

URL = "http://127.0.0.1:8080/v1/chat/completions"
PROMPT = "Write a 500-word explanation of how a bicycle's gears work."


def run_once():
    request = Request(
        URL,
        data =json.dumps({
            "messages": [{"role": "user", "content": PROMPT}],
            "stream": True,
            "temperature": 0,
            "max_tokens": 128,
            "cache_prompt": False,
        }).encode(),
        headers={"Content-Type": "application/json"},
    )

    start = perf_counter()
    first_text_ms = None
    timings = {}

    with urlopen(request, timeout=120) as response:
        for line in response:
            if not line.startswith(b"data:"):
                continue
            payload = line[5:].strip()
            if payload == b"[DONE]":
                break

            event = json.loads(payload)
            for choice in event.get("choices", []):
                text = choice.get("delta", {}).get("content")
                if text and first_text_ms is None:
                    first_text_ms = (perf_counter() - start) * 1000

            timings = event.get("timings", timings)

        if first_text_ms is None or not timings:
            raise RuntimeError("The stream did not return text and server timings.")

        return first_text_ms, timings["predicted_per_second"], timings["predicted_n"]


run_once()
runs = [run_once() for _ in range(10)]

print("run,ttft_ms,decode_tok_s,generated_tokens")
for number, (ttft, speed, tokens) in enumerate(runs, start=1):
    print(f"{number},{ttft:.1f},{speed:.2f},{tokens}")

print(f"Median TTFT = {median(row[0] for row in runs):.1f} ms")
print(f"Median decode speed = {median(row[1] for row in runs):.2f} tok/s")

