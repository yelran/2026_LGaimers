# Accuracy (lm-eval-harness test)

# 패키지 설치
!pip -q install lm-eval
!pip -q install ray
!pip -q install vllm==0.14.1

# 환경 변수 설정
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"
print("HF_HUB_ENABLE_HF_TRANSFER =", os.environ["HF_HUB_ENABLE_HF_TRANSFER"])

# lm-eval 실행
!python -m lm_eval \
  --model vllm \
  --model_args pretrained=/content/model,gpu_memory_utilization=0.8,trust_remote_code=True \
  --tasks gsm8k,kobest_copa,piqa,mmlu_humanities,mmlu_other,mmlu_social_sciences,mmlu_stem \
  --device cuda \
  --batch_size auto \
  --num_fewshot 5 \
  --limit 512