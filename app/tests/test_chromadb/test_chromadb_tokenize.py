from transformers import AutoTokenizer, LlamaTokenizer
import tiktoken
import keras_hub

#tokenizer = keras_hub.tokenizers.Tokenizer.from_preset("llama3.1_8b")
#asdiasjd
#encoding = tiktoken.model("llama3")
llmtoken = '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'
#tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B", token = llmtoken)
# tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
tokenizer = LlamaTokenizer.from_pretrained("Qwen/Qwen3-8B")