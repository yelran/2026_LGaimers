# Speed Score

# run_benchmark.py 파일 생성
benchmark_script = """
import sys
import argparse
import time

# Monkey-patch argparse
_original_add_argument = argparse.ArgumentParser.add_argument
def _patched_add_argument(self, *args, **kwargs):
    if 'deprecated' in kwargs:
        del kwargs['deprecated']
    return _original_add_argument(self, *args, **kwargs)
argparse.ArgumentParser.add_argument = _patched_add_argument

try:
    from vllm.benchmarks.throughput import main, add_cli_args
except ImportError:
    print("vLLM이 설치되지 않았습니다. !pip install vllm을 먼저 실행하세요.")
    sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="vLLM throughput benchmark")
    add_cli_args(parser)
    args = parser.parse_args()
    main(args)
"""

with open("run_benchmark.py", "w") as f:
    f.write(benchmark_script)

print("run_benchmark.py 생성 완료")

# 모델 경로 확인 (실제 경로)
MODEL_PATH="/content/model"

# 벤치마크 실행 (L4 GPU 최적화 옵션 포함)
!python run_benchmark.py \
    --model $MODEL_PATH \
    --dataset-name random \
    --num-prompts 100 \
    --random-input-len 100 \
    --random-output-len 200 \
    --random-range-ratio 0.0 \
    --seed 42 \
    --gpu-memory-utilization 0.85 \
    --trust-remote-code