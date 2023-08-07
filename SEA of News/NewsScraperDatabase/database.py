### Class for database collecting

import pandas as pd
import datetime

class EmptyDatasetException(Exception):
    """Raised when trying to do operations with an empty database.
    
    Attributes:
         dataset -- An empty Pandas DataFrame.
         message -- The message when the exception is raised.
    """
    
    dataset: pd.DataFrame
    message: str
    
    def __init__(self, dataset, message = 'DataFrame cannot be empty'):
        """Initialize the EmptyDatasetException class."""
        
        self.dataset = dataset
        self.message = message
        super().__init__(self.message)

    
class TemporaryDatabase:
    """Implementation of the Temporary Database class: A database class to store collected data from a country and then load it into a database.
    
    Note: We are making assuming that the data format is in a Pandas DataFrame.
    
    Attributes:
        dataset -- A dictionary containing the data (in dataframe format) collected from various news sources for one country. Each dataframe must have: title, URL, author, outlet, date, tags, country_source as the columns.
        country -- The country name of where the data was collected.
    """
    
    # Attribute types
    dataset: dict
    country: str
    
    def __init__(self, dataset: dict, country: str) -> None:
        """Initialize the dataset class."""
        
        self.dataset = dataset
        self.country = country
        self.compiled_dataset = pd.DataFrame()
        
    def display(self, news_source = 'all') -> pd.DataFrame:
        """Display the dataset according to the news source."""
        
        if news_source == 'all':
            return self.dataset
        else:
            return self.dataset[news_source]
    
    def add_source(self, news_source: str, data: pd.DataFrame) -> None:
        """Add a source and the data into the dataset."""
        
        if data.empty:
            raise EmptyDatasetException(data)
        else:
            self.dataset[news_source] = data
    
    def _validate_data(self, curr_dataset: pd.DataFrame, today_date = True) -> pd.DataFrame:
        """Validate data helper function."""

        curr_dataset = curr_dataset[curr_dataset.tags.str.contains(f'{self.country}|{self.country.upper()}|{self.country.lower()}|ASEAN|Asean|asean', regex = True)] # Checks for tags
        curr_dataset = curr_dataset.drop_duplicates(subset = ['title', 'url'], keep = 'first') # Checks uniqueness
        if today_date: # Check for data to be today's date.
            curr_dataset[curr_dataset['date'].isin([datetime.today()]) == True]
        return curr_dataset
    
    def validate_data(self, news_source = 'all', today_date = True) -> None:
        """Validate the dataset, by checking for uniqueness in title and URL, seeing if the tag contains country name or ASEAN."""
        
        if news_source == 'all':
            for source in self.dataset:
                curr_dataset = self._validate_data(self.dataset[source], today_date)
                self.dataset[source] = curr_dataset
        else:
            curr_dataset = self._validate_data(self.dataset[news_source])
            self.dataset[source] = curr_dataset               
    
    def compile(self) -> None:
        """Construct the dataset into a large dataset."""
        
        master_dataset = pd.DataFrame()
        
        for source in self.dataset:
            curr_data = self.dataset[source]
            #master_dataset.append(self.dataset[source], ignore_index = True)
            master_dataset = pd.concat([master_dataset, curr_data])
        
        self.compiled_dataset = master_dataset
    
    def fetch_compiled(self) -> pd.DataFrame:
        """Return the compiled dataset or raise an exception if the compiled dataset is empty."""
        
        if self.compiled_dataset.empty:
            raise EmptyDatasetException(self.compiled_dataset)
        else:
            return self.compiled_dataset
    
    def create_csv(self, filepath: str) -> None:
        """Create a csv file from the compiled dataset."""
        
        if self.compiled_dataset.empty:
            raise EmptyDatasetException(self.compiled_dataset)
        else: 
            self.compiled_dataset.to_csv(filepath)