from NewsScraperDatabase.database import *
from NewsScraperDatabase.scrapers.sg_scraper import *
from NewsScraperDatabase.scrapers.indo_scraper import *
from NewsScraperDatabase.scrapers.myr_scraper import *
from NewsScraperSummarizer.summarizer import *
import pandas as pd
from prefect import flow, task
from prefect.deployments import Deployment
import csv
from prefect import flow, get_run_logger
import os
import sqlite3

RETRY_DELAY = 1800 # 30 MIN (REPORTED IN SECONDS)
RETRIES = 5

@task
def extract_forward(Outlet) -> pd.DataFrame:
    """Do one forward iteration of the extract process. Note: Outlet is a class name.
    Returns a dataframe containing a populated database.
    """
    
    outlet = Outlet()
    outlet.collect_data()
    dataset = outlet.return_dataset()
    
    return dataset
    
@flow(name = "extract", retries = RETRIES, retry_delay_seconds = RETRY_DELAY)
def extract() -> pd.DataFrame:
    """Perform the extraction process and return a dataframe for SEA."""
    
    # Singapore Data
    dataset = TemporaryDatabase({}, 'SEA')
    sg_news = extract_forward(ChannelNewsAsia)
    if not sg_news.empty:
        dataset.add_source('Channel News Asia', sg_news)
    # dataset.validate_data(today_date = True)
    
    myn_news = extract_forward(MyanmarNow)
    if not myn_news.empty:
        dataset.add_source('Myanmar Now', myn_news)
        
    indo_news = extract_forward(AntaraNews)
    if not indo_news.empty:
        dataset.add_source('Antara News', indo_news)
    
    dataset.compile()
    return dataset.fetch_compiled()

@task(name = "transform")
def transform(dataset) -> pd.DataFrame:
    """Take in a Pandas dataset and perform the transformation process and return two dataframes."""
    
    news_dataset = dataset.drop(columns = ['outlet', 'country_source', 'url'])
    source_dataset = dataset.drop(columns = ['date', 'tags', 'country'])

    return {'news': news_dataset, 'source': source_dataset}
    
@task(name = "load")
def load(dataset: dict) -> None:
    """Load the dataset into a csv (Add database later!). 
    
    Note, that the dataset here is the format is like the one in transform method."""
    
    conn = sqlite3.connect('') # Need to write sqlite3 connection
    c = conn.cursor()
    c.execute(''' CREATE TABLE IF NOT EXISTS news(title PRIMARY KEY, date DATE, tags TEXT, country TEXT)''')
    c.execute(''' CREATE TABLE IF NOT EXISTS source(title PRIMARY KEY, outlet TEXT, country_source TEXT, URL TEXT)''')
    
    for item in dataset:
        curr = dataset[item]
        curr.to_sql(item, con = conn, if_exists = 'append', index = False)
    conn.commit()

    return dataset

@task(name = 'summarize')
def summarize(dataset: dict) -> None:
    """Take in a article dataset and then summarize them."""
    
    sources = dataset['source']
    sources.reset_index(inplace = True)
    summarizer = Summarizer('bart', sources, 50, 100)
    summarizer.populate_articles()
    summarizer.summarize()
    summarizer.create_pdf()

@flow(log_prints = True)
def complete_pipeline():
    """The complete ETL and summarization pipeline."""
    
    dataset = extract()
    dataset = transform(dataset)
    dataset = load(dataset)
    summarize(dataset)

if __name__ == "__main__":
    flow = complete_pipeline()
    flow.run()