import pandas as pd
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelWithLMHead
from rouge import Rouge
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
import requests

class Summarizer:
    """Implementation of the Summarizer class: An object which summarizes articles.
    
    === Attributes ===
    summarizer: The type of summarizer: Bart, T5 or Pegasus.
    dataset: A pandas dataframe which contains the dataset for today. Must have the exact same headings as the one obtained by NewsScraper class.
    min_length: The minimum length for a single summary of an article.
    max_length: The maximum length for a single summary of an article.
    """
    summarizer: str
    dataset: pd.DataFrame
    min_length: int
    max_length: int
    
    def __init__(self, summarizer: str, dataset: pd.DataFrame, min_length = int, max_length = int) -> None:
        """Initialize the Summarizer class."""
        
        if summarizer == 'bart':
            self.summarizer = AutoModelWithLMHead.from_pretrained('facebook/bart-large-cnn', return_dict = True)
            self.tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-cnn')
        elif summarizer == 't5':
            self.summarizer = AutoModelWithLMHead.from_pretrained('T5-base', return_dict = True)
            self.tokenizer = AutoTokenizer.from_pretrained('T5-base')
        elif summarizer == 'pegasus':
            self.summarizer = AutoModelWithLMHead.from_pretrained('google/pegasus-large', return_dict = True)
            self.tokenizer = AutoTokenizer.from_pretrained('google/pegasus-large')

        self.dataset = dataset
        self.rouge = Rouge()
        self.rouge_results = []
        self.min_length = min_length
        self.max_length = max_length
        self.articles = {'title': [], 'country': [], 'article': []}
        self.summary = {}
        self.messy_summary = {}
    
    def _cleanup(self, text):
        """Take in a summarized text and return it wihtout the '>' or '<'. """

        final_text = ''
        indicator = False

        for i in text:
            if i == '>':
                indicator = False
            elif i == '<':
                indicator = True
            elif indicator:
                continue
            else:
                final_text += i

        return final_text
    
    def _get_article(self, link: str):
        """Get a link and return the entire article."""
        
        request = requests.get(link)
        html = request.content
        soup = BeautifulSoup(html, 'html.parser')
        
        article = ''
        
        for links in soup.find_all('p'):
            curr = links.string
            if curr is None or curr == 'None':
                continue
            else:
                article += curr
        return article
    
    def populate_articles(self):
        """Populate self.articles."""
        
        dataset = self.dataset.to_dict('index')
        for index in dataset:
            country = dataset[index]['country_source']
            url = dataset[index]['url']
            title = dataset[index]['title']
            
            article = self._get_article(url)
            self.articles['title'].append(title)
            self.articles['article'].append(article)
            self.articles['country'].append(country)
 
    def summarize(self) -> None:
        """Go through every title in self.dataset and then summarize them."""
        
        for index, article in enumerate(self.articles['article']):
            country = self.articles['country'][index]
            title = self.articles['title'][index]
            print(title)
            
            inputs = self.tokenizer.encode("sumarize: " + article, return_tensors = 'pt', max_length = 1024, truncation = True)
            output = self.summarizer.generate(inputs, min_length = self.min_length, max_length = self.max_length)
            summary = self.tokenizer.decode(output[0])
            
            if country in self.summary:
                self.summary[country].append((title, self._cleanup(summary)))
            else:
                self.summary[country] = [(title, self._cleanup(summary))] 
        
    def create_pdf(self) -> None:
        """Create the summarized text in pdf format."""
        
        doc = SimpleDocTemplate(
                f"summary {str(datetime.today().date())}.pdf",
                pagesize=letter,
                rightMargin=72, leftMargin=72,
                topMargin=72, bottomMargin=18,
                )
        styles = getSampleStyleSheet()
        flowables = []
        
        for country in self.summary:
            title = Paragraph(country, style = styles['Heading1'])
            flowables.append(title)
            for summaries in self.summary[country]:
                article_title, summary = summaries
                a_title = Paragraph(article_title, style = styles["Heading3"])
                flowables.append(a_title) 
                para = Paragraph(summary, style=styles["Normal"])
                flowables.append(para) 
            flowables.append(PageBreak())

        doc.build(flowables)

"""
if __name__ == '__main__':
    articles = pd.DataFrame(pd.read_csv('Source.csv'))
    print('data read successfully')
    summarizer = Summarizer('bart', articles, 50, 100)
    print('summarizer initialized successfully')
    summarizer.populate_articles()
    print('summarizer populated successfully')
    summarizer.summarize()
    print('summary generation successfully')
    summarizer.create_pdf()
    print('summary pdf generated successfully')
"""
    
