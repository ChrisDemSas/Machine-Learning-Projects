import torch
import sys
import pandas as pd
from transformers import pipeline
from util import *
import time
from rouge import Rouge
import seaborn as sns

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
results = {'Minimum Length': [], 'Rouge Score': [], 'Time Executed': []}
rouge_scorer = Rouge()

summarizer = pipeline('summarization', model = "google/pegasus-large")

for index, article in enumerate(dataset['Article']):
    country = dataset['Country'][index]
    title = dataset['Title'][index]
    start_time = time.time()
    
    summary = summarizer(article, max_length = 100, min_length = 30, do_sample = False)[0]['summary_text']
    summary += f'({title})'
    score = rouge_scorer.get_scores(hyps = summary, refs = article)[0]['rouge-1']['f']
    #print(summary)
    time_executed = time.time() - start_time
    
    if country in summary_dataset:
        summary_dataset[country] += cleanup(summary)
    else:
        summary_dataset[country] = cleanup(summary)
        
    print(f"{index + 1} out of {len(dataset['Article'])} completed! Rouge Score: {score}, Time Executed: {time_executed}")
    
    """
    results['Rouge Score'].append(avg_rouge/counter)
    results['Minimum Length'].append(length)
    results['Time Executed'].append(timer)
    print(f'=========================== Length: {length} ===========================================')   """


print('=======================================================================')
print('Generating results...')
