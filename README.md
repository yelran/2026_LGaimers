# ![LG Aimers](https://img.shields.io/badge/LG-A50034?style=flat&logoColor=white)     2026 LG Aimers 8기


> EXAONE-4.0-1.2B 모델을 대상으로 성능 손실 최소화 + 추론 속도 최적화를 목표로 한 LLM 경량화 해커톤


<br>

## 대회 개요
| 항목 | 내용 |
|------|------|
| 주최 | LG AI 연구원  |
| 모델 | EXAONE-4.0-1.2B |
| 평가 환경 | vLLM 0.14.1 / L4 GPU (22.4GiB) |
| 평가 지표 | 성능 비율 × 토큰당 추론시간 감소 비율 |
| 제약 조건 | 제출 ≤ 10GB / 추론 ≤ 20분 |



<br>

## 평가 산식

<br>

<img width="466" height="233" alt="스크린샷 2026-05-07 050353" src="https://github.com/user-attachments/assets/be412e4e-6b65-439b-be81-51a79af674e1" />

<br>
<br>

| 구성 요소 | 설명 |
|-----------|------|
| 성능  | EXAONE-4.0-1.2B 대비 성능 비율 |
| 추론 시간  |EXAONE-4.0-1.2B 대비 토큰당 추론 시간 감소 비율 |



<br>

## 베이스 모델 분석 (EXAONE-4.0-1.2B)
> https://github.com/LG-AI-EXAONE/EXAONE-4.0

<br>

### 모델 구조
| Item | Value |
|------|-------|
| Total Parameters | 1.279B |
| Layers | 30 |
| Hidden dim | 2048 |
| Attention heads | 32 (KV: 8) |
| FFN dim | 4096 (SwiGLU) |
| Vocab size | 102,400 |

<br>

### 모델 크기
| Precision | Size |
|-----------|------|
| FP16 | 2.38 GiB |
| W4 | 0.60 GiB (4.0x compression) |

<br>

### 특징
- Hybrid Attention (local + global)
- GQA (Query 32개, KV 8개)
- SwiGLU FFN
- 최대 65K token context

<br>

## 경량화 기법 및 실험 결과

### 기법 개요
> **GPTQ** : bit(W4A16/W8A16/W4A8/W8A8), calibration data , layer 보호, mixed precision, 수치 안정화 튜닝
>
> **AWQ** : bit/group 설정, Smoothing 전략, Auto→Fallback 매핑, calibration 튜닝

<br>

### 실험 검증 환경
> 베이스 모델 대비 단일·혼합 도메인 성능을 비교하여 리더보드 점수와의 상관관계 분석
> 
> vLLM Serving : `max_gen_toks=2048, limit=512, batch_size=auto, gpu_memory_utilization=0.85`

<img width="1564" height="424" alt="image" src="https://github.com/user-attachments/assets/67db06ee-87e2-4a4b-ad4e-9357ac62947f" />

<br>


### 주요 실험 결과

|  | Method | Score | Inference Time | Size |
|---|--------|-------|----------------|------|
| 1 | GPTQ + Last 4 Layer Protection | 0.5915 | 10m 51s | 1.6GB |
| 2 | GPTQ + Mixed Precision | 0.6059 | 10m 30s | 1.35GB |
| 3 | GPTQ + Calibration Filter | **0.6180** | 10m 26s | 1.4GB |
| 4 | AWQ + 4bit Group Quant | 0.6015 | 10m 51s | - |

<br>

## 가설 및 인사이트

> 4bit(속도↑ 성능↓) vs 8bit(성능↑ 속도↓) — trade-off 균형점 

- 마지막 layer는 error가 크게 튀어 ignore 처리가 효과적
- calibration data 길이 필터링이 성능 향상에 유효
- dampening_frac 조정으로 weight 오차 최소화

<br>

## Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)
![Transformers](https://img.shields.io/badge/Transformers-FF6F00?style=flat&logo=huggingface&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=flat&logo=huggingface&logoColor=black)
![vLLM](https://img.shields.io/badge/vLLM-412991?style=flat&logoColor=white)
![GPTQ](https://img.shields.io/badge/GPTQ-00A550?style=flat&logoColor=white)
![AWQ](https://img.shields.io/badge/AWQ-FF6B6B?style=flat&logoColor=white)
![PEFT](https://img.shields.io/badge/PEFT-FF6B6B?style=flat&logoColor=white)
![LoRA](https://img.shields.io/badge/LoRA-7B2D8B?style=flat&logoColor=white)

<br>

## 프로젝트 구조
```
submit.zip
└── model/
    ├── config.json
    ├── model.safetensors
    ├── tokenizer.json
    ├── tokenizer_config.json
    └── special_tokens_map.json
```
