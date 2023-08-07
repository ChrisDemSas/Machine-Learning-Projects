# SEA of News: Data Scraping News Headlines and Summarization of South East Asian News

## Quick Summary
SEA of News aims to quickly gather from popular news outlets in Singapore, Myanmar and Indonesia in order to expedite the research process for those who want to monitor the geopolitics of these countries. Initially, the aim was to simply summarize the current day's news in order to give a brief overview of the daily events occuring in these countries, but eventually, I decided to store the headlines and other key information (dates, country source etc.) in an sqlite database and let it grow over time. The method used was to use Extract-Transform-Load for the database part, using the web scraping to scrape headlines from the outlets and then using the pipeline to load the data into a sqlite database. Then, the url was then used again to scrape the article content of the headlines, while carefully ignoring the articles not written on the current day. Finally, the entire project was deployed using Prefect and then automatically run daily so that a news summary can be generated daily. This entire project managed to expedite the research of geopolitical developments by at least 10% and greatly reduced the burden of going to individual news outlets and sifting through irrelavant news. 

## Problem Statement and Introduction
The geopolitical landscape during the year 2023, has seen tremendous developments and keeping up with current events is difficult due to numerous sources providing different versions of events. For geopolitical analysts who are interested in the geopolitics between between countries and domestic affairs, this is an arduos task because the international and domestic affairs intermingle and the main political issues are often obscured with irrelevant headlines. In order to alleviate this problem, a data science and machine learning approach was proposed to lighten the burden through web scraping and summarizing news content. To this end, a large-language model (LLM) is needed to quickly summarize the articles and web scraping will be employed to collect the relevant data. Popular Southeast Asian news outlets such as Channel News Asia will be scraped for news because these news outlets are where most people obtain their news from.

When I designed this project, I wanted the project to have the following constraints, with the following reasons:
  - Very short summaries for each news headline (a few sentences), so that the geopolitical analyst can quickly sift through the information, ignore unnecessary information       and get a gist of the affairs of the country. 
  - Storing the news headlines in a sqlite3 database because the dataset is relatively small and will probably not grow exponentially, since I am not focusing on global news.
  - Lowest run time in the computer because this will be run on my local computer, daily.

With the following constraints in mind, the testing of the Large Language Models (T5/Pegasus/BART) can begin.

## Methodology
The method is to employ the Extract-Transform-Load pipeline in order to extract information from the news outlet's website. The title, date, url, country source, news outlet and country (either ASEAN or Singapore/Indonesia/Myanamr) where the news is concerned. It should also be mentioned, that the author's name was not collected because there are some news outlets which do not contain the author's name for some articles and I wished to be consistent, instead of writing the news outlet twice or having a lot of missing data. The article's content was also scraped using web scraping technologies, though not stored in a database.


<img width="450" alt="Screenshot 2023-08-07 at 1 40 38 PM" src="https://github.com/ChrisDemSas/Machine-Learning-Projects/assets/93426725/fa7939c7-f6ec-4b12-849c-42d570f804b9">

Figure 1: Figure showing the ETL pipeline and the summarization process.

The schema of the database is shown:


<img width="233" alt="Screenshot 2023-08-07 at 1 52 25 PM" src="https://github.com/ChrisDemSas/Machine-Learning-Projects/assets/93426725/9db40df6-ca00-46d0-a57e-f594f6e7b75d">

Figure 2: Figure showing the database schema of the news summarization project.


Then, the article content is summarized using a Large Language Model (BART/Pegasus/T5) to produce the summary and the results put inside a PDF document. Finally, the model is deployed using Prefect and set to run every day.

## Results for Summary Model
The results found that out of the three language models, the BART model performed the best (results can be viewed under 'results' folder under 'test' and 'NewsScraperSummarizer'. This is because the T5 model, while was quite successful, was quite hard to fine-tune for other users if they wanted a longer summary because it simply generated empty spaces, and so was rejected. The BART and Pegasus models, were both quite well done, but BART performed better when it came to time constraints. The results are shown here:

<img width="888" alt="Screenshot 2023-08-07 at 2 26 42 PM" src="https://github.com/ChrisDemSas/Machine-Learning-Projects/assets/93426725/d5f96fd2-7141-47d3-9368-d4eff30b11ba">

Figure 3: Graph showing the time taken for execution with varying token lengths.

<img width="894" alt="Screenshot 2023-08-07 at 2 29 24 PM" src="https://github.com/ChrisDemSas/Machine-Learning-Projects/assets/93426725/56e5f53d-3ced-4ebc-b813-e6391533b5ec">

Figure 4: Graph showing the Rouge Score with varying token lengths.


## Conclusion

In conclusion, with the constraints shown, the BART model seems to be the best one for the purpose of summarization and for this model. This is because in Figure 4, the ROUGE scores seem to be close to the Pegasus model and that the BART model runs significantly faster than the Pegasus model as shown in Figure 3. Thus, the BART model was chosen for the purpose, whereby the final results look like this:
<img width="961" alt="Screenshot 2023-08-07 at 2 34 19 PM" src="https://github.com/ChrisDemSas/Machine-Learning-Projects/assets/93426725/6a0428f2-642f-4d6c-8f9b-7ad5765d3b09">

Figure 6: Sample summary of what the BART model and the pipeline is capable of.

It is my hope that the entire pipeline can be of use for other people. The code itself is very simple to use, although to repurpose it for other countries, one needs to write their own web scraping scripts. 

Further improvements can be made on the way the database is created: i.e scraping the entire website for the available news from the first inception of the news outlet, although this will probably overload the servers.

## Improvements and Changelog

7th August 2023: Added Vietnamese and Thai news outlets (Tuo Tre News and ThaiPBSWorld respectively).









