from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("kaiyuy/leandojo-lean4-tacgen-byt5-small")       # Or "lean3" -> "lean4"
model = AutoModelForSeq2SeqLM.from_pretrained("kaiyuy/leandojo-lean4-tacgen-byt5-small")   # Or "lean3" -> "lean4"
"""
def get_tactic(state):
    tokenized_state = tokenizer(state, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Generate a single tactic.
    tactic_ids = model.generate(tokenized_state.input_ids, max_length=1024)
    tactic = tokenizer.decode(tactic_ids[0], skip_special_tokens=True)
    #print(tactic, end="\n\n")
    return tactic
"""
def get_tactic(state):
    tokenized_state = tokenizer(state, return_tensors="pt", padding=True, truncation=True, max_length=512)
    # Generate multiple tactics via beam search.
    tactic_candidates_ids = model.generate(
        tokenized_state.input_ids,
        max_length=1024,
        num_beams=10,
        length_penalty=0.0,
        do_sample=False,
        num_return_sequences=10,
        early_stopping=False,
    )
    tactic_candidates = tokenizer.batch_decode(
        tactic_candidates_ids, skip_special_tokens=True
    )
    return tactic_candidates