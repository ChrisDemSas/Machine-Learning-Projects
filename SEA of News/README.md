# SEA of News: Data Scraping News Headlines and Summarization of South East Asian News

## Quick Summary
SEA of News aims to quickly gather from popular news outlets in Singapore, Myanmar and Indonesia in order to expedite the research process for those who want to monitor the geopolitics of these countries. Initially, the aim was to simply summarize the current day's news in order to give a brief overview of the daily events occuring in these countries, but eventually, I decided to store the headlines and other key information (dates, country source etc.) in an sqlite database and let it grow over time. The method used was to use Extract-Transform-Load for the database part, using the web scraping to scrape headlines from the outlets and then using the pipeline to load the data into a sqlite database. Then, the url was then used again to scrape the article content of the headlines, while carefully ignoring the articles not written on the current day. Finally, the entire project was deployed using Prefect and then automatically run daily so that a news summary can be generated daily. This entire project managed to expedite the research of geopolitical developments by at least 10% and greatly reduced the burden of going to individual news outlets and sifting through irrelavant news.

## Problem Statement and Introduction
The geopolitical landscape during the year 2023, has seen tremendous developments and keeping up with current events is difficult due to numerous sources providing different versions of events. For geopolitical analysts who are interested in the geopolitics between between countries and domestic affairs, this is an arduos task because the international and domestic affairs intermingle and the main political issues are often obscured with irrelevant headlines. In order to alleviate this problem, a data science and machine learning approach was proposed to lighten the burden through web scraping and summarizing news content. To this end, a large-language model (LLM) is needed to quickly summarize the articles and web scraping will be employed to collect the relevant data. Popular Southeast Asian news outlets such as Channel News Asia will be scraped for news because these news outlets are where most people obtain their news from.

## Methodology
The method is to employ the Extract-Transform-Load pipeline in order to extract information from the news outlet's website. The title, date, url, country source, news outlet and country (either ASEAN or Singapore/Indonesia/Myanamr) where the news is concerned. It should also be mentioned, that the author's name was not collected because there are some news outlets which do not contain the author's name for some articles and I wished to be consistent, instead of writing the news outlet twice or having a lot of missing data. The article's content was also scraped using web scraping technologies, though not stored in a database.


<img width="450" alt="Screenshot 2023-08-07 at 1 40 38 PM" src="https://github.com/ChrisDemSas/Machine-Learning-Projects/assets/93426725/fa7939c7-f6ec-4b12-849c-42d570f804b9">

Figure 1: Figure showing the ETL pipeline and the summarization process.

The schema of the database is shown:


<img width="233" alt="Screenshot 2023-08-07 at 1 52 25 PM" src="https://github.com/ChrisDemSas/Machine-Learning-Projects/assets/93426725/9db40df6-ca00-46d0-a57e-f594f6e7b75d">

Figure 2: Figure showing the database schema of the news summarization project.


Then, 


## Results

## Conclusion
