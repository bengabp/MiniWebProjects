from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
import math
import torch

model_name = "fabiochiu/t5-base-medium-title-generation"
max_input_length = 512
temperature = 0.06
num_titles = 1

print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
nltk.download('punkt')
print("Model loaded!")


def generate_text_title(st_text_area):
    print("INPUT TEXT : ",st_text_area)
    # tokenize text
    inputs = ["summarize: " + st_text_area]
    inputs = tokenizer(inputs, return_tensors="pt")

    # compute span boundaries
    num_tokens = len(inputs["input_ids"][0])
    max_input_length = 500
    num_spans = math.ceil(num_tokens / max_input_length)
    overlap = math.ceil(
    (num_spans * max_input_length - num_tokens) / max(num_spans - 1, 1))
    spans_boundaries = []
    start = 0
  
    for i in range(num_spans):
        spans_boundaries.append(
        [start + max_input_length * i, start + max_input_length * (i + 1)])
        start -= overlap
        spans_boundaries_selected = []
        j = 0

    for _ in range(num_titles):
        spans_boundaries_selected.append(spans_boundaries[j])
        j += 1
        if j == len(spans_boundaries):
            j = 0

    # transform input with spans
    tensor_ids = [
        inputs["input_ids"][0][boundary[0]:boundary[1]]
        for boundary in spans_boundaries_selected
    ]
    tensor_masks = [
        inputs["attention_mask"][0][boundary[0]:boundary[1]]
        for boundary in spans_boundaries_selected
    ]

    inputs = {
        "input_ids": torch.stack(tensor_ids),
        "attention_mask": torch.stack(tensor_masks)
    }

    # compute predictions
    outputs = model.generate(**inputs, do_sample=True, temperature=temperature, max_new_tokens = 50)
    decoded_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    predicted_titles = [
        nltk.sent_tokenize(decoded_output.strip())[0]
        for decoded_output in decoded_outputs
    ]

    if predicted_titles:
        return predicted_titles[0]
        
    else:
        return None