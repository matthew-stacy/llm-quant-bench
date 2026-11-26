
# Local LLM Quantization Benchmark

I benchmarked two GGUF quantizations of Qwen2.5-3B-Instruct on my Apple M1 Max using llama.cpp. I measured how long it took to receive the first streamed text and how quickly each model generated tokens.

## Results

| Quantization | Median time to first token ↓ | Median decode speed ↑ |
| --- | ---: | ---: |
| Q4_K_M | 89.8 ms | **80.34 tokens/s** |
| Q8_0 | **79.3 ms** | 68.52 tokens/s |

Q4_K_M had **17.3% higher median decode throughput**. Q8_0 delivered the first streamed text **10.5 ms sooner**. The benchmark used one prompt on one machine and measured performance only.

## Method

- **Hardware and runtime** — Apple M1 Max, llama.cpp with Metal
- **Workload** — One request at a time, one warm-up run, and 10 measured runs per quantization. Every measured run generated 128 tokens.
- **Controls** — Same bicycle-gears prompt, temperature of 0, 128-token output limit, and prompt-cache reuse disabled.
- **Timing** — `bench.py` measures time to first streamed text on the client. Decode throughput comes from the server's timing data.

## Files

- [`bench.py`](bench.py) — Python benchmark client
- [Q4_K_M raw results](q4-verified-results.txt)
- [Q8_0 raw results](q8-verified-results.txt)

