# SEA of News: Data Scraping News Headlines and Summarization of South East Asian News

## Quick Summary
SEA of News aims to quickly gather from popular news outlets in Singapore, Myanmar and Indonesia in order to expedite the research process for those who want to monitor the geopolitics of these countries. Initially, the aim was to simply summarize the current day's news in order to give a brief overview of the daily events occuring in these countries, but eventually, I decided to store the headlines and other key information (dates, country source etc.) in an sqlite database and let it grow over time. The method used was to use Extract-Transform-Load for the database part, using the package BeautifulSoup to scrape headlines from the outlets and then using the pipeline to load the data into a sqlite database. Then, the url was then used again to scrape the article content of the headlines, while carefully ignoring the articles not written on the current day. Finally, the entire project was deployed using Prefect and then run daily so that a news summary can be generated daily. This entire project managed to expedite the research of geopolitical developments by at least 10% and greatly reduced the burden of going to individual news outlets and sifting through irrelavant news.

## Problem Statement and Introduction


## Methodology

## Results

## Conclusion
