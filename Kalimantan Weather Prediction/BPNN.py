# This is the implentation of the East Kalimantan Rainfall prediction neural network.

import torch 
import numpy as np

class BackpropagationNN(torch.nn.Module):
    """Implementation of the class BackpropagationNeuralNetwork."""
    
    def __init__(self, in_features, out_features):
        """Initialize the BackpropagationNN class."""
        
        super().__init__()
        
        self.tansig = torch.nn.Tanh() 
        self.logsig = torch.nn.Sigmoid()
        self.purelin = torch.nn.Linear(in_features, 50)
        self.hidden = torch.nn.Linear(50, 20)
        self.final_layer = torch.nn.Linear(20, out_features)
        
    
    def forward(self, x):
        """Return a transformed x after backpropagation."""
        
        x = self.tansig(x)
        x = self.logsig(x)
        x = self.purelin(x)
        x = self.hidden(x)
        x = self.final_layer(x)
        
        return x
        
        