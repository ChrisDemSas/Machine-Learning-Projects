# Main training program

import pandas as pd
import torch
from torch.optim import Optimizer
import numpy as np
from autograd import grad
import torch.nn as nn
from BPNN import *
from LevenbergMarquardt import *
from load_data import *
import seaborn as sns
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt

# Arguments
FILENAME = 'rainfall_data.csv'
TRAIN_TEST_PERCENT = 0.8
EPOCH = 26 # CHANGE LATER
INPUT = 2
OUTPUT = 1
torch.manual_seed(0) # Set the seed

# SGD Optimizer Arguments
SGD_LEARNING_RATE = 0.1


# ADAM Optimizer Arguments
ADAM_LEARNING_RATE = 0.1

# Levenberg-Marquardt Optimizer Arguments
LAMBDA = 100

dates, train_dataloader, test_dataloader = process_dataset(FILENAME, INPUT, TRAIN_TEST_PERCENT)
print("Data has been generated!")

loss_data = []
epochs = [n for n in range(1, EPOCH + 1)]
loss_function = nn.MSELoss()
model = BackpropagationNN(INPUT, OUTPUT)

def optimizer(optimizer_name):
    """Take in an optimizer name and return an initialized optimizer."""
    
    if optimizer_name == 'Adam':
        optimizer = torch.optim.Adam(model.parameters(), ADAM_LEARNING_RATE)
    elif optimizer_name == 'Levenberg-Marquardt':
        optimizer = LevenbergMarquardt(model.parameters(), LAMBDA)
    elif optimizer_name == 'SGD':
        optimizer = torch.optim.SGD(model.parameters(), SGD_LEARNING_RATE)
    
    return optimizer
    
optimizer = optimizer('SGD')

def train(dataloader, epoch, lam):
    """Take in a training data and epoch number and return losses. """
    
    intialize = True
    current_loss = 0
    current_lambda = lam
    
    for i in range(0, epoch):
        current_lambda = lam
        avg_loss = 0
        counter = 0
        current_loss = 0
        
        for id_batch, (x_batch, y_batch) in enumerate(dataloader):
            #optimizer = LevenbergMarquardt(model.parameters(), current_lambda)
            output = model(x_batch)
            loss = loss_function(output, y_batch)
            avg_loss += float(loss)
        
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            counter += 1
        print(f"Epoch: {i + 1}, Average Loss: {loss}")
            
        loss_data.append(float(loss) / counter)


train(train_dataloader, EPOCH, LAMBDA)
#sns.lineplot(epochs, loss_data)

print(f"Minimum: {min(loss_data)} at epoch {loss_data.index(min(loss_data)) + 1}")

# Testing

def test(dataloader):
    """Tests the model."""
    
    avg_loss = 0
    predictions = []
    count = 0
    
    for id_batch, (x_batch, y_batch) in enumerate(dataloader):
        if x_batch.size()[0] == 1:
            continue
        test = model(x_batch)
        loss = loss_function(test, y_batch)
        print(f"Batch Loss at {id_batch}: {loss}")
        
        avg_loss += loss
        predictions.append(float(test))
        count += 1
    
    avg_loss = avg_loss / count
    
    return pd.DataFrame(predictions), avg_loss

predictions, avg_loss = test(test_dataloader)
print(f"Average Loss: {avg_loss}")

returned_predictions = (abs(transform_back(predictions, FILENAME))[0]) # Cheat hack 

date = dates.tolist()

y_values = pd.read_csv(FILENAME)['total_rainfall'][-46:]

sns.lineplot(date[-len(returned_predictions):], returned_predictions)
sns.lineplot(date[-len(returned_predictions):], y_values)

plt.show()