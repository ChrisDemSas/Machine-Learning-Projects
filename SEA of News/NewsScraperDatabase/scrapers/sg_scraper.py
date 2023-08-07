from .scraper import NewsScraper
import requests
import pandas as pd
from bs4 import BeautifulSoup
from titlecase import titlecase
from datetime import datetime
    
class ChannelNewsAsia(NewsScraper):
    """Implementation of the News Scraper for Channel News Asia: A implementation of the scraper from Channel News Asia.
    
    Attributes:
        base_url: The base URL for Channel News Asia.
        categories: The list of categories for Channel News Asia.
        dataset: A dictionary containing all data.
    """

    dataset: dict
    base_url: str
    categories: list
    
    def __init__(self) -> None:
        """Initialize the ChannelNewsAsia class."""
        NewsScraper.__init__(self)
        self.base_url = 'https://www.channelnewsasia.com/singapore'
    
    def _check_tag(self, tag: str) -> str:
        """Take in a tag and return either ASEAN or Myanmar depending on the contents of the tag."""
        
        foreign_country = ['myanmar', 'thailand', 'vietnam', 'cambodia', 'laos', 'asean', 'burma',
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
            return 'Singapore'

    def collect_data(self) -> None:
        """Fetch the data from Channel News Asia and populate the dataset."""
        
        request = requests.get(self.base_url)
        html = request.content
        soup = BeautifulSoup(html, 'html.parser')
        trunc_url = 'https://www.channelnewsasia.com'
        
        for item in soup.find_all('div', {'class': 'card-object__figure'}):
            for link in item.find_all('a', {'class': 'link'}):
                link = link.get('href')
                if 'singapore' in link:
                    link = trunc_url + link
                else:
                    continue
                
                news_request = requests.get(link)
                news_html = news_request.content
                news_soup = BeautifulSoup(news_html, 'html.parser')
                
                # Get the title
                title = news_soup.find('h1', {'class': 'h1 h1--page-title'})
                title = title.text.strip()
                
                # Get the Date
                date = news_soup.find('div', {'class': 'article-publish article-publish--'})
                
                if date is None:
                    date_backup = news_soup.find('div', {'class': 'article-publish article-publish-- block block-mc-content-share-bookmark block-content-share-bookmark clearfix'})
                    date_backup = date_backup.text.strip()[:11]
                    date = date_backup
                else:
                    date = date.text.strip()[:11]
    
                date = datetime.strptime(date, '%d %b %Y').date()
                if not (date == datetime.today().date()):
                    continue
                else:
                    print(link)
                
                # Get the tags
                meta = news_soup.find_all("meta", {'name': 'cXenseParse:mdc-keywords'})
                category = news_soup.find('meta', {'name': 'cXenseParse:mdc-context'})
                category = category['content']
                tags = f'{category};'
                
                if len(meta) > 0:
                    for item in meta:
                        tag = item['content']
                        tags += f'{tag};'
                
                # Get the country
                country = self._check_tag(title)
                self.dataset['country'].append(country)
                self.dataset['tags'].append(tags)
                self.dataset['title'].append(title)
                self.dataset['url'].append(link)
                self.dataset['date'].append(date)
                self.dataset['country_source'].append('Singapore')
                self.dataset['outlet'].append('Channel News Asia')
                

if __name__ == '__main__':
    data = ChannelNewsAsia()
    data.collect_data()
    print(data.length())
