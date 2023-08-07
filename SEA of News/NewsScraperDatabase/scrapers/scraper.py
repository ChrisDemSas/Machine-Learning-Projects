import requests
import pandas as pd
from bs4 import BeautifulSoup
from titlecase import titlecase
from datetime import datetime

class NewsScraper:
    """Implementation of the NewsScraper class: A news scraping class which extracts the information from a base URL, whereby the URL must contain categories and news in it.
    
    Attributes:
        dataset -- The entire dataset that is to be populated. Has the fields, title, author, date, country_source, tags, outlet, url.
        base_url -- The Base URL.
        categories -- A list of categories.
    """
    
    dataset: dict
    base_url: str
    categories: list
    
    def __init__(self) -> None:
        """Initialize the NewsScraper class."""
        
        self.dataset = {'title': [],
                        'date': [],
                        'tags': [],
                        'outlet': [],
                        'country': [],
                        'country_source': [],
                        'url': []}
        self.header = {'User-agent': 'Mozilla/5.0'}

    
    def collect_data(self) -> None:
        """Fetch the dataset from the base URL and populate the dataset."""
        
        raise NotImplementedError
    
    def return_dataset(self) -> dict:
        """Return the dataset as a Pandas DataFrame.."""
        
        return pd.DataFrame(self.dataset)
    
    def is_empty(self) -> bool:
        """Return True if dataset is empty."""
        
        empty_data  = {'title': [],
                        'date': [],
                        'tags': [],
                        'outlet': [],
                        'country': [],
                        'country_source': [],
                        'url': []}
        
        return self.dataset == empty_data
    
    def create_csv(self, filepath: str) -> None:
        """Create a csv file from self.dataset."""
        
        pd.DataFrame(self.dataset).to_csv(filepath)
    
    def check_url(self) -> str:
        """Return the base url."""
        
        return self.base_url
    
    def length(self) -> dict:
        """Return a dictionary containing length of each table."""
        
        dataset = {'title': len(self.dataset['title']),
                        'date': len(self.dataset['date']),
                        'tags': len(self.dataset['tags']),
                        'outlet': len(self.dataset['outlet']),
                        'country': len(self.dataset['country']),
                        'country_source': len(self.dataset['country_source']),
                        'url': len(self.dataset['url'])}  

        return dataset
