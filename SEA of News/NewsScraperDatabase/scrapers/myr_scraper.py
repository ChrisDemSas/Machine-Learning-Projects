from .scraper import NewsScraper
import requests
import pandas as pd
from bs4 import BeautifulSoup
from titlecase import titlecase
from datetime import datetime
    
class TheIrrawaddy(NewsScraper):
    """Implementation of the News Scraper for The Irrawady: A implementation of the scraper from The Irrawaddy.
    
    Attributes:
        base_url: The base URL for The Irrawaddy.
        categories: The list of categories for The Irrawaddy.
        dataset: A dictionary containing all data.
    """

    dataset: dict
    base_url: str
    categories: list
    
    def __init__(self) -> None:
        """Initialize the TheIrrawaddy class."""
        NewsScraper.__init__(self)
        self.base_url = 'https://www.irrawaddy.com/category/news'
        self.categories = []
    
    def _check_tag(self, tag: str) -> str:
        """Take in a tag and return either ASEAN or Myanmar depending on the contents of the tag."""
        
        foreign_country = ['singapore', 'thailand', 'vietnam', 'cambodia', 'laos', 'asean',
                           'brunei', 'malaysia', 'indonesia', 'timor leste', 'philippines']
    
        asean_checker = False
        for country in foreign_country:
            if asean_checker:
                continue
            if country in tag.lower():
                asean_checker = True 

        if asean_checker:
            return 'ASEAN'
        else:
            return 'Myanmar'

    def collect_data(self) -> None:
        """Fetch the data from TheIrrawaddy and populate the dataset."""
        
        request = requests.get(self.base_url)
        html = request.content
        soup = BeautifulSoup(html, 'html.parser')
        
        divs = soup.find_all('h3', {'class': 'jeg_post_title'}) 
        
        for div in divs:
            url = div.find('a')['href'] # Get the URL
            self.dataset['url'].append(url)
            print(url)
            
            for h3 in div.find_all('a'): # Get the Title
                title = h3.text
                if len(title) > 0:
                    self.dataset['title'].append(title)

            news_div = requests.get(url)
            news_html = news_div.content
            news_soup = BeautifulSoup(news_html, 'html.parser')
            
            # Construct Date
            date = news_soup.find_all('div', {'class': 'jeg_nav_item jeg_top_date'})
            date = div.text.strip()
            date = datetime.strptime(date, '%A, %B %d, %Y').date()
            if date == datetime.today():
                self.dataset['date'].append(date)
            else:
                continue
            
            # Construct Tags
            tag = ''
            for tags in news_soup.find_all('div', {'class': 'jeg_post_tags'}):
                for curr_tag in tags.find_all('a'):
                    tag += str(curr_tag.text) + ';'
            self.dataset['tags'].append(tag)
            
            # Check for other ASEAN countries
            country = self._check_tag(tag)
            self.dataset['country'].append(country)
            
            # Append the other details
            self.dataset['country_source'].append('Myanmar')
            self.dataset['outlet'].append('The Irrawaddy')


class MyanmarNow(NewsScraper):
    """Implementation of the News Scraper for Myanmar Now: A implementation of the scraper from Myanmar Now.
    
    Attributes:
        base_url: The base URL for Myanmar Now.
        categories: The list of categories for Myanmar Now.
        dataset: A dictionary containing all data.
    """

    dataset: dict
    base_url: str
    categories: list
    
    def __init__(self) -> None:
        """Initialize the MyanmarNow class."""
        NewsScraper.__init__(self)
        self.base_url = 'https://myanmar-now.org/en/'
        self.categories = ['business', 'national', 'local-news', 'announcement']
        self.tracker = []
    
    def _check_tag(self, tag: str) -> str:
        """Take in a tag and return either ASEAN or Myanmar depending on the contents of the tag or title."""
        
        foreign_country = ['singapore', 'thailand', 'vietnam', 'cambodia', 'laos', 'asean',
                           'brunei', 'malaysia', 'indonesia', 'timor leste', 'philippines']
    
        asean_checker = False
        for country in foreign_country:
            if asean_checker:
                continue
            if country in tag.lower():
                asean_checker = True 

        if asean_checker:
            return 'ASEAN'
        else:
            return 'Myanmar'
    
    def collect_data(self) -> None:
        """Fetch the data from Myanmar Now and populate the dataset."""
        
        request = requests.get(self.base_url)
        html = request.content
        soup = BeautifulSoup(html, 'html.parser')
        
        for link in soup.find_all('h2', {'class': 'post-title'}):
            
            # Get the title and URL
            for title in link:
                url = title.get('href')
                title = title.text
                if not (url in self.tracker):
                    self.tracker.append(url)
                    print(url)
                else:
                    continue
            
                news_request = requests.get(url)
                news_html = news_request.content
                news_soup = BeautifulSoup(news_html, 'html.parser')
                
                # Construct the Tags
                tag = ''
                for tags in news_soup.find_all('span', {'class': 'tagcloud'}):
                    if not (tags.text is None):
                        tag += f"{tags.text};"
                
                for tags in news_soup.find_all('span', {'class': 'post-cat-wrap'}):
                    if not (tags is None):
                        tag += f'{tags.text};'
                
                # Find the Date
                date = news_soup.find('span', {'class': 'date meta-item tie-icon'})
                date = date.text
                date = datetime.strptime(date, '%B %d, %Y').date()
                if date == datetime.today().date():
                    self.dataset['date'].append(date)
                    print(url)
                else:
                    continue                
                
                # Check Country
                country = self._check_tag(title)
                
                self.dataset['country'].append(country)
                self.dataset['title'].append(title)
                self.dataset['url'].append(url)
                self.dataset['tags'].append(tag)
                self.dataset['country_source'].append('Myanmar')
                self.dataset['outlet'].append('Myanmar Now')


if __name__ == '__main__':
    data = TheIrrawaddy()
    data.collect_data()
    print(data.length())