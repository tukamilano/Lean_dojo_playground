#Using ppo(consider using ilql later)

import torch

from trl import AutoModelForSeq2SeqLMWithValueHead, PPOConfig, PPOTrainer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
tokenizer = AutoTokenizer.from_pretrained("kaiyuy/leandojo-lean4-tacgen-byt5-small")       # Or "lean3" -> "lean4"
model = AutoModelForSeq2SeqLMWithValueHead.from_pretrained("kaiyuy/leandojo-lean4-tacgen-byt5-small") 
model_ref = AutoModelForSeq2SeqLMWithValueHead.from_pretrained("kaiyuy/leandojo-lean4-tacgen-byt5-small")
# ある程度学習が進んだら PPOTrainer(config, model, model_ref, tokenizer) -> PPOTrainer(config, model_ref, model_ref_new, tokenizer)とかにするのアリかも
tokenizer.pad_token = tokenizer.eos_token 
# 2. initialize trainer
ppo_config = {"batch_size": 1}
config = PPOConfig(**ppo_config)
ppo_trainer = PPOTrainer(config, model, model_ref, tokenizer)

#datasetをランダムにする必要あり？+並列処理
def train(dataset):
    for i in range(len(dataset)):
        if dataset [i][3] == None:
            continue
        else:
            state = dataset[i][0].pp
            tokenized_state = tokenizer(state, return_tensors="pt")
            tactic = dataset[i][1]
            reward = [torch.tensor(float(dataset[i][3]))]
            tokenized_tactic = tokenizer(tactic, return_tensors="pt")
            train_stats = ppo_trainer.step([tokenized_state['input_ids'][0]], [tokenized_tactic['input_ids'][0]], reward)