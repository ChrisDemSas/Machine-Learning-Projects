from .scraper import NewsScraper
import requests
import pandas as pd
from bs4 import BeautifulSoup
from titlecase import titlecase
from datetime import datetime
    
class TuoTreNews(NewsScraper):
    """Implementation of the News Scraper for Tuo Tre News: A implementation of the scraper from Tuo Tre News.
    
    Attributes:
        base_url: The base URL for Tuo Tre News.
        categories: The list of categories for Tuo Tre News.
        dataset: A dictionary containing all data.
    """

    dataset: dict
    base_url: str
    categories: list
    
    def __init__(self) -> None:
        """Initialize the TuoTreNews class."""
        NewsScraper.__init__(self)
        self.base_url = 'https://tuoitrenews.vn'
        self.categories = ['politics', 'society', 'business', 'lifestyle']
        self.tracker = []
    
    def _process_url(self, component: list) -> str:
        """Take in the components of a url and return the full URL, date and category."""
        
        final = self.base_url
        date = ''
        
        if len(component) > 3:
            if component[2] in self.categories:
                for item in component[1:]:
                    final += f'/{item}'
                    if item.isnumeric():
                        date = datetime.strptime(item, '%Y%m%d')
                    
            if final != self.base_url:
                return final, date, component[2]
            else:
                return False, False, False
        else:
            return False, False, False

    def collect_data(self) -> pd.DataFrame:
        """Fetch the data from ThaiPBSWorld and populate the dataset."""
        
        request = requests.get(self.base_url)
        html = request.content
        soup = BeautifulSoup(html, 'html.parser')
        foreign_country = ['singapore', 'thailand', 'cambodia', 'laos', 'burma', 'myanmar',
                           'brunei', 'malaysia', 'indonesia', 'timor leste', 'philippines', 'asean']        
        
        divs = soup.find_all('a')
        for div in divs:
            curr_url = None
            if not (div is None):
                curr = div['href'].split('/')
                curr, date, tag = self._process_url(curr)
                if (not curr) or (curr in self.tracker):
                    continue
                else:
                    self.tracker.append(curr)
                    curr_url = curr
            print(curr_url)

            news_request = requests.get(curr_url)
            news_html = request.content
            news_soup = BeautifulSoup(news_html, 'html.parser')
            
            title = news_soup.find_all('h1') # Get title
            
            for item in title:
                title = item.text.strip()
                if len(title) == 0:
                    continue

                if not (item is None) and item != " ":
                    #title = item.text.strip()
                    self.dataset['title'].append(titlecase(title))
                    
                    asean_checker = False
                    for country in foreign_country:
                        if country in title.lower():
                            asean_checker = True
                    
                    if asean_checker:
                        self.dataset['country'].append('ASEAN')
                    else:
                        self.dataset['country'].append('Vietnam')
                            

            self.dataset['url'].append(curr_url)
            self.dataset['date'].append(date)
            self.dataset['country_source'].append('Vietnam')
            self.dataset['outlet'].append('Tuo Tre News')
            self.dataset['tags'].append(tag)

"""
if __name__ == '__main__':
    data = TuoTreNews()
    data.collect_data()
    print(data.length())
"""