from .scraper import *
import requests
import pandas as pd
from bs4 import BeautifulSoup
from titlecase import titlecase
from datetime import datetime

class ThaiPBS(NewsScraper):
    """Implementation of the News Scraper for ThaiPBSWorld: A implementation of the scraper from ThaiPBSWorld.
    
    Attributes:
        base_url: The base URL for ThaiPBSWorld.
        categories: The list of categories for ThaiPBSWorld.
        dataset: A dictionary containing all data.
    """
    
    dataset: dict
    base_url: str
    categories: list
    
    def __init__(self) -> None:
        """Initialize the ThaiPBSScraper class."""
        NewsScraper.__init__(self)
        self.base_url = 'https://www.thaipbsworld.com/category/news'
        self.categories = ['general', 'politics', 'asean', 'business', 'technology', 'environment', 'south-watch']
    
    def collect_data(self) -> pd.DataFrame:
        """Fetch the data from ThaiPBSWorld and populate the dataset."""
        
        for category in self.categories:
            new_url = self.base_url + f'/{category}/'
            request = requests.get(new_url)
            html = request.content
            soup = BeautifulSoup(html, 'html.parser')
            
            divs = soup.find_all('div', {'class': 'post-title'})
            
            for div in divs:
                link = div.find('a')['href']
                print(link)
                counter = 0
                
                self.dataset['url'].append(link)
                
                for li in div.find_all('li'):
                    if counter == 0:
                        date = li.text
                        self.dataset['date'].append(datetime.strptime(date, '%B %d, %Y'))
                    elif counter == 1:
                        author = li.text[3:].split(' ')
                        full_name = ''
                        
                        if '(World)' in author:
                            author.remove('(World)')
                        
                        for names in author: 
                            full_name += f'{names} '
                            
                        self.dataset['author'].append(full_name)             
                        
                    elif counter == 2:
                        title = titlecase(li.text[17:])
                        self.dataset['title'].append(title)
                    counter += 1
                
                current_url = requests.get(link)
                html = current_url.content
                soup = BeautifulSoup(html, 'html.parser')
                divs = soup.find_all('ul', {'class': 'tags-box'})
        
                final_tag = category
                for elements in divs:
                    for tag in elements.find_all('a', {'rel': 'tag'}):
                        final_tag += f';{tag.text}'
                
                self.dataset['tags'].append(final_tag)

                if 'ASEAN' in final_tag or 'asean' in final_tag:
                    self.dataset['country'].append('ASEAN')
                else:
                    self.dataset['country'].append('Thailand')

                self.dataset['country_source'].append('Thailand')
                self.dataset['outlet'].append('ThaiPBSWorld') 