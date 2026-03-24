# PPL score
import torch
from tqdm import tqdm

def evaluate_model_ppl_chat(model_path, n_samples=200, max_seq_len_filter=512, min_seq_len_filter=64):
    print(f"[INFO] PPL 측정을 위해 모델 로드 중: {model_path}")
    
    # 평가용 모델과 토크나이저 로드
    eval_tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    eval_model = AutoModelForCausalLM.from_pretrained(
        model_path, 
        device_map="auto", 
        torch_dtype=torch.bfloat16,
        trust_remote_code=True
    )
    eval_model.eval()

    # 데이터셋 로드 (MANTA-1M 사용)
    test_ds = load_dataset("LGAI-EXAONE/MANTA-1M", split="train", streaming=True)
    
    nlls = []
    count = 0
    
    print(f"[INFO] {n_samples}개의 샘플로 PPL 측정 시작...")
    
    for example in tqdm(test_ds):
        if count >= n_samples:
            break
            
        # 채팅 템플릿 적용
        text = eval_tokenizer.apply_chat_template(
            example["conversations"], 
            add_generation_prompt=False, 
            tokenize=False
        )
        
        inputs = eval_tokenizer(text, return_tensors="pt", truncation=True, max_length=max_seq_len_filter)
        input_ids = inputs["input_ids"].to(eval_model.device)
        
        # 필터 조건 확인 (너무 짧거나 긴 문장 제외)
        if input_ids.size(1) < min_seq_len_filter:
            continue
            
        target_ids = input_ids.clone()
        
        with torch.no_grad():
            outputs = eval_model(input_ids, labels=target_ids)
            neg_log_likelihood = outputs.loss
            nlls.append(neg_log_likelihood)
            
        count += 1

    ppl = torch.exp(torch.stack(nlls).mean()).item()
    
    # 메모리 정리
    del eval_model
    del eval_tokenizer
    torch.cuda.empty_cache()
    
    return ppl