from .scraper import NewsScraper
import requests
import pandas as pd
from bs4 import BeautifulSoup
from titlecase import titlecase
from datetime import datetime, timedelta
    
class AntaraNews(NewsScraper):
    """Implementation of the News Scraper for Antara News: A implementation of the scraper from Antara News.
    
    Attributes:
        base_url: The base URL for Antara News.
        categories: The list of categories for Antara news.
        dataset: A dictionary containing all data.
    """

    dataset: dict
    base_url: str
    categories: list
    
    def __init__(self) -> None:
        """Initialize the AntaraNews class."""
        NewsScraper.__init__(self)
        self.base_url = 'https://en.antaranews.com/news'
        self.tracker = []
    
    def _check_tag(self, tag: str) -> str:
        """Take in a tag and return either ASEAN or Indonesia depending on the contents of the tag."""
        
        foreign_country = ['myanmar', 'thailand', 'vietnam', 'cambodia', 'laos', 'asean', 'burma',
                           'brunei', 'malaysia', 'singapore', 'timor leste', 'philippines']
    
        asean_checker = False
        for country in foreign_country:
            if asean_checker:
                continue
            if country in tag.lower():
                asean_checker = True 

        if asean_checker:
            return 'ASEAN'
        else:
            return 'Indonesia'
    
    def _check_date(self, date: str) -> datetime:
        """Take in the date in string format and return a datetime."""
        
        if 'ago' in date:
            if 'hours' in date:
                hours = timedelta(int(date[:1]))
                return datetime.today() - hours
            elif 'minutes' in date:
                minutes = timedelta(minutes = int(date[:1]))
                return datetime.today() - minutes
            elif 'seconds' in date:
                seconds = timedelta(seconds = int(date[:1]))
                return datetime.today() - seconds
            else:
                return datetime.today()
        else:
            new_date = ''
            if 'th' in date:
                date = date.split('th')
            elif 'st' in date:
                date = date.split('st')
            elif 'rd' in date:
                date = date.split('rd')
            elif 'nd' in date:
                date = date.split('nd')
            for item in date:
                new_date += item
            
            return datetime.strptime(new_date, '%d %B %Y')
                

    def collect_data(self) -> None:
        """Fetch the data from Antara News and populate the dataset."""
        
        request = requests.get(self.base_url)
        html = request.content
        soup = BeautifulSoup(html, 'html.parser')
        
        for link in soup.find_all('a'):
            url = link.get('href')
            if '/news/' in url:
                if not (url in self.tracker):
                    self.tracker.append(url)
                else:
                    continue
            else:
                continue
            
            # URL News Request 
            print(url)
            news_request = requests.get(url)
            news_html = news_request.content
            news_soup = BeautifulSoup(news_html, 'html.parser')
            
            # Title News Request
            title = news_soup.find('title')
            title = title.text.strip('- ANTARA News')
            
            # Get the Date
            date = news_soup.find('span', {'class': 'article-date'})
            date = date.text.strip()
            if not (date == datetime.today()):
                continue
            
            # Get the country
            country = self._check_tag(title)
            
            # Get the tags: No tags here...
            
            # Append everything
            self.dataset['url'].append(url)
            self.dataset['title'].append(title)
            self.dataset['date'].append(date)
            self.dataset['tags'].append(None)
            self.dataset['country'].append(country)
            self.dataset['country_source'].append('Indonesia')
            self.dataset['outlet'].append('Antara News')

"""
if __name__ == '__main__':
    data = AntaraNews()
    data.collect_data()
    print(data.length())
"""