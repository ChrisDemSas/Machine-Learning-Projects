import torch
import sys
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelWithLMHead
from util import *
from rouge import Rouge
import time
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

#summarizer = pipeline('summarization', model = "facebook/bart-large-cnn")
tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-cnn')
model = AutoModelWithLMHead.from_pretrained('facebook/bart-large-cnn', return_dict = True)
rouge_scorer = Rouge()

curr_country = None
for index, article in enumerate(dataset['Article']):
    country = dataset['Country'][index]
    title = dataset['Title'][index]
    start_time = time.time()
    
    inputs = tokenizer.encode("sumarize: " + article, return_tensors = 'pt', max_length = 1024, truncation = True)
    output = model.generate(inputs, min_length = 50, max_length = 100)
    summary = tokenizer.decode(output[0])

    """
    try:
        summary = summarizer(article, max_length = 100, min_length = 50, do_sample = False)[0]['summary_text']
    except IndexError:
        print(f'Failed: {title}')
        continue
        """
    
    score = rouge_scorer.get_scores(hyps = summary, refs = article)[0]['rouge-1']['f']
    summary += f'({title}). '
    #print(summary)
    
    if country in summary_dataset:
        summary_dataset[country] += cleanup(summary)
    else:
        summary_dataset[country] = cleanup(summary)
    
    if curr_country != country:
        print(f'========================================== {curr_country} is finished! ====================================')
        curr_country = country  
            
    time_executed = time.time() - start_time
    print(f'{title} is finished!')

print('=======================================================================')
print('Generating results...')

for country in summary_dataset:
    summary = summary_dataset[country]
    print(summary)
    
#print(summary_dataset['Indonesia'])
#sns.lineplot(results['Rouge Score'], results['Minimum Length'])
#sns.lineplot(results['Rouge Score'], results['Time Executed'])
#pd.DataFrame(results).to_excel('bart_results.xlsx')