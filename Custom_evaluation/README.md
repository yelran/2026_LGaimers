## 📊 LM-Evaluation Harness Tasks Categories

| 평가 카테고리 | 대표 lm-eval task | 설명 | 특징 |
|--------------|------------------|------|------|
| **World Knowledge**<br>(폭넓은 지식 + 객관식) | mmlu, hellaswag, arc_easy, arc_challenge, truthfulqa, triviaqa | 과학적 상식 및 일반 사실 관계 평가<br>양자화 시 지식 파라미터 손실 여부 확인 | metric = accuracy |
| **Math**<br>(논리적 계산, 정답 1개) | gsm8k, mathqa, svamp | gsm8k → 주관식 추론<br>mathqa → 객관식 추론 | metric = exact_match (≈ accuracy)<br>양자화 시 가장 먼저 깨짐 |
| **Coding**<br>(코드 이해/추론) | humaneva, mbpp | Python 코드 생성 능력 평가 | pass@1, pass@k<br>(일반 accuracy와 계산 방식 다름) |
| **Instruction Following**<br>(지시 수행) | alpaca_eval, ifeval | 제약 조건 준수 여부<br>모델의 instruction 이해 능력 | 정량화 어려움<br>lm-eval에서 제한적 지원 |
| **Agentic Tool Use**<br>(도구 사용) | mint, toolbench | API 호출 및 tool 사용 능력 | 소형 모델(1.2B) 측정 어려움<br>실제 대회 metric에는 거의 미반영 |
| **Multilinguality**<br>(다국어 이해/생성) | kobest_copa, kobest_boolq, kobest_hellaswag, mgsm_ko, xwinograd, xcopa, xnli, flores | 한국어 인과 추론(copa)<br>다국어 수학(mgsm) | metric = accuracy / BLEU<br>한국어 모델에 유리 |

---



## 📊 LM-Evaluation Harness Tasks (In-house Evaluation)
https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks


### 1. World Knowledge & Reasoning

#### 🔹 hellaswag
- 문맥상 다음에 올 가장 적절한 상황을 고르는 태스크
- 일반 상식 및 문맥 이해 능력 평가
- **Example**
  - 양자화 파라미터 수정 → 점수 하락 시  
    → 모델의 일반 상식(reasoning capability) 손상 여부 확인 가능

#### 🔹 arc_challenge
- 초중등 수준 과학 문제 중 **난이도 높은 문제**
- 단순 암기가 아닌 **추론 기반 문제**
- 양자화 시 모델의 reasoning 품질 평가에 적합

#### 🔹 mmlu
- 대학 수준의 다양한 학문 지식을 평가하는 **대표 benchmark**
- 글로벌 standard evaluation task

---

### 2. Korean Language Evaluation

#### 🔹 kobest_boolq / kobest_copa / kobest_hellaswag
- **kobest_boolq** → 독해력 및 사실 판단 능력
- **kobest_copa** → 인과관계 추론 능력
- **kobest_hellaswag** → 문맥적 완성도 및 심화 상식

🔹특징
  - 양자화 시 **kobest_hellaswag 성능이 가장 먼저 하락**
  - 한국어 성능 평가를 위해 포함

---

### 3. Mathematical Reasoning

#### 🔹 gsm8k
- 수학 문제 해결 능력 평가 (grade-school math)
- 정답 기반 평가 (exact match)
- 논리적 계산 및 reasoning 능력 확인 가능


---

## 📊 Evaluation Results

## 1. MMLU Pro (English)

| Domain | Accuracy | Output toks/s |
|--------|----------|---------------|
| biology | 0.5254 | 2472.62 |
| business | 0.4316 | 2335.46 |
| computer science | 0.4463 | 2408.27 |
| law | 0.2910 | 1847.03 |
| math | 0.6152 | 2628.99 |


## 2. MMLU Pro (Korean)

| Domain | Accuracy | Output toks/s |
|--------|----------|---------------|
| biology | 0.2237 | 2472.62 |
| business | 0.3066 | 2579.41 |
| computer science | 0.3049 | 1773.81 |
| law | 0.1777 | 1817.85 |
| math | 0.4688 | 2407.02 |

