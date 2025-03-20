#!/usr/bin/env python3

import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("rinna/japanese-gpt-neox-3.6b-instruction-sft", use_fast=False)
# 標準
#model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-neox-3.6b-instruction-sft")
# 自動
#model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-neox-3.6b-instruction-sft", device_map='auto')
# 自動(VRAM16GB以下でも8GBはNG)
# model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-neox-3.6b-instruction-sft", torch_dtype=torch.float16, device_map='auto')
# CPU指定
model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-neox-3.6b-instruction-sft").to("cpu")
# GPU指定
#model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-neox-3.6b-instruction-sft").to("cuda")
# GPU指定(VRAM16GB以下でも8GBはNG)
#model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-neox-3.6b-instruction-sft", torch_dtype=torch.float16).to("cuda")


#繰り返し(抜けるのはCtl+c)
prompt = ""
while True:
    # 質問を入力
    question = input("質問をどうぞ： ")

    if question.lower() == 'clear':
        question = ""
        prompt = ""

    prompt = prompt+f"ユーザー: {question}<NL>システム: "

    # 時間計測開始
    start = time.time()

    token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")

    with torch.no_grad():
        output_ids = model.generate(
            token_ids.to(model.device),
            do_sample=True,
            max_new_tokens=128,
            temperature=0.7,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    output = tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])
    output = output.replace("<NL>", "\n")

    # 時間表示
    end = time.time()
    print(end-start)

#    print(prompt)
    print(output)
    prompt = prompt+output+"<NL>"

