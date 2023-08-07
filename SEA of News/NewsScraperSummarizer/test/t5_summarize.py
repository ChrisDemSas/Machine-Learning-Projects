import torch
import sys
import pandas as pd
from reportlab.pdfgen.canvas import Canvas
from transformers import AutoTokenizer, AutoModelWithLMHead
from util import *
import pdfkit
import json
from rouge import Rouge

def cleanup(text):
    """Take in a text and clean it up."""
    
    final_text = ''
    indicator = False
    
    for i in text:
        if i == '>':
            indicator = False
        elif i == '<':
            indicator = True
        elif indicator:
            continue
        else:
            final_text += i
    
    return final_text
        
    
FILENAME = ''

dataset = extract_info(FILENAME)
summary_dataset = {}
tokenizer = AutoTokenizer.from_pretrained('T5-base')
model = AutoModelWithLMHead.from_pretrained('T5-base', return_dict = True)
rouge_scorer = Rouge()

for index, article in enumerate(dataset['Article']):
    country = dataset['Country'][index]
    title = dataset['Title'][index]
    
    inputs=tokenizer.encode("sumarize: " + article,return_tensors='pt', max_length=1024, truncation=True) #Change max_length to 512
    output = model.generate(inputs, min_length = 100, max_length = 400)
    summary = tokenizer.decode(output[0])
    summary += f'({title}). '
    score = rouge_scorer.get_scores(hyps=article, refs=summary)[0]['rouge-1']['f']
    #print(summary)
    
    if country in summary_dataset:
        summary_dataset[country] += cleanup(summary)
    else:
        summary_dataset[country] = cleanup(summary)
    
    print(f"{index + 1} out of {len(dataset['Article'])} completed! Rouge Score: {score}")

print('=======================================================================')
print('Generating PDF...')
print(summary_dataset['Indonesia'])