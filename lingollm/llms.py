from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import transformers
import time
import torch
import openai
from .consts import OPENAI_API_KEY, arapaho_morphology

valid_models = [
    "gpt-3.5-turbo-1106",
    "gpt-4o-2024-08-06",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "gpt-4o-mini-2024-07-18"
    # add your favorite models here
]

class LLMWrapper:
    def __call__(self, messages):
        raise NotImplementedError

class ChatGPTWrapper(LLMWrapper):
    def __init__(self, model_id):
        self.api_key = OPENAI_API_KEY
        self.model_id = model_id
    
    def __call__(self, messages) -> str:
        client = openai.OpenAI(api_key=self.api_key)
        stream = client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            stream=True,
            top_p=0.5,
        )
        content = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                # print(chunk.choices[0].delta.content, end="", flush=True)
                content += chunk.choices[0].delta.content
        return content
    
class HFWrapper(LLMWrapper):
    def __init__(self, model_id):
        self.model_id = model_id
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        if self.model_id == "mistralai/Mixtral-8x7B-Instruct-v0.1":
            self.quantization_config = quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16
            )
            self.model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=quantization_config, device_map="auto")
        else:
            self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, torch_dtype=torch.float16, device_map="auto")
    
    def __call__(self, messages):
        if self.model_id == "mistralai/Mixtral-8x7B-Instruct-v0.1" or self.model_id == "mistralai/Mistral-7B-Instruct-v0.2":
            if len(messages[1]["content"]) > 300000:
                pos = messages[1]["content"].find("Please help me translate the following sentence from ")
                messages[1]["content"] = f"""\
Here is a grammar book of Arapaho:

{arapaho_morphology}

""" + messages[1]["content"][pos:]
                
            messages = [
                {"role": "user", "content": messages[0]["content"] + messages[1]["content"]},
            ] + messages[2:]
        tokenized_chat = self.tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        )
        # tokenized_chat = tokenized_chat 
        outputs = self.model.generate(
            tokenized_chat.to(self.model.device),
            max_new_tokens=32000, do_sample=True, top_p=0.9,
            eos_token_id=self.tokenizer.eos_token_id,
        )
        return self.tokenizer.decode(outputs[0][len(tokenized_chat[0]):], skip_special_tokens=True)

def get_llm_wrapper(model_id) -> LLMWrapper:
    if "gpt" in model_id:
        return ChatGPTWrapper(model_id)
    else:
        return HFWrapper(model_id)