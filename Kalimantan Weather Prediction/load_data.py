# Methods used for data analysis

import numpy
import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset

FILENAME = 'rainfall_data.csv'

def transform(rainfall_data):
    """Take in a rainfall dataset and apply the transformation."""
    
    b = max(rainfall_data)
    a = min(rainfall_data)
    
    transformed = (0.8 * (rainfall_data - a) / (b - a)) + 0.1
    
    return transformed

def transform_back(transformed_data, rainfall_data):
    """Take in a transformed_data and transform it back."""
    
    original_data = pd.read_csv(rainfall_data)['total_rainfall']
    
    b = max(original_data)
    a = min(original_data)
    
    untransformed = a + (((transformed_data - 0.1) * (b-a))/0.8)
    return untransformed


def create_dataset(file_name, input_number):
    """
    Take in a file and return a dataset containing 2 temperatures as the input 
    and an output table containing a single temperature as output.
    
    Pre-condition: Only for rainfall datasets, where the dataset only contains 
    the time and weather data as columns.
    """
    
    data = pd.read_csv(file_name)
    dates, rainfall = data['month'], data['total_rainfall']
    transformed_rainfall = transform(rainfall)
    
    data = transformed_rainfall.tolist() # CHANGE THE TOTAL RAINFALL IF OTHER FILES
    x_input = []
    y_input = []
    
    for item in data:
        x_input.append(item)
        y_input.append(item)
    
    """
    for index, rainfall in enumerate(data):
        if index > input_number - 1: # Account for the 0th index.
            y_input.append(rainfall)
        
        if index + input_number < len(data):
            for i in data[index: index + input_number]:
                x_input.append(i)"""
    
    return dates, rainfall, x_input, y_input


def train_test_split(dates, x_input, y_input, seperation_percentage):
    """Take in an x and y inputs and seperate them according to the seperation 
    percentage. Return the x_training, y_training, x_test and y_test.
    
    """
    
    index = int(len(dates) * seperation_percentage)
    
    
    x_train = x_input[: index]
    y_train = y_input[: index]
    x_test = x_input[index :]
    y_test = y_input[index :]
    
    return x_train, y_train, x_test, y_test


def process_dataset(file_name, input_number, seperation_percentage):
    """Take in a file name and generate the input and output datasets."""
    
    dates, rainfall, x_input, y_input = create_dataset(file_name, input_number)
    x_train, y_train, x_test, y_test = train_test_split(dates, x_input, y_input, seperation_percentage)
    
    x_train = torch.from_numpy(numpy.array(x_train)).float()
    y_train = torch.from_numpy(numpy.array(y_train)).float()
    x_test = torch.from_numpy(numpy.array(x_test)).float()
    y_test = torch.from_numpy(numpy.array(y_test)).float()
    
    train_dataset = TensorDataset(x_train, y_train)
    train_dataloader = DataLoader(train_dataset, batch_size = input_number, shuffle = False)
    test_dataset = TensorDataset(x_test, y_test)
    test_dataloader = DataLoader(test_dataset, batch_size = input_number, shuffle = False)
    
    return dates, train_dataloader, test_dataloader

a = process_dataset(FILENAME, 2, 0.8)
