from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "EleutherAI/gpt-neo-1.3B"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model = model.to("cpu")  # ⇨ move to "cuda" if you have a GPU

def generate_with_llm(prompt: str, return_logits: bool = False):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    output = model.generate(
        **inputs,
        max_new_tokens=50,
        output_scores=return_logits,
        return_dict_in_generate=True,
    )

    generated_tokens = output.sequences[0]
    text = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    logits = None
    if return_logits and "scores" in output:
        logits = torch.stack(output.scores).softmax(dim=-1).detach().cpu().numpy()

    return text, logits
