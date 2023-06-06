# Implementation of the Levenberg-Marquardt Optimizer.

import torch
from torch.optim import Optimizer
import numpy as np
from autograd import grad
import torch.nn as nn

class LevenbergMarquardt(Optimizer):
    """Implementation of the Levenberg-Marquardt optimizer."""
    
    def __init__(self, params, default_lambda: int):
        """Initialize the Levenberg-Marquardt Algroithm."""
        self.default_lambda = default_lambda
        
        defaults = {"lambda": default_lambda
                    }
        
        super(LevenbergMarquardt, self).__init__(params, defaults)
        
    
    def step(self, closure = None):
        """Calculates a step on the Levenberg-Marquardt Algorithm."""
        
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        
        parameters = [] 
        derivatives = []
        
        for group in self.param_groups:
            
            for p in group['params']:
                if p.grad is not None:
                    parameters.append(p)
                    derivatives.append(p.grad.data)

            self.lm(parameters,
               derivatives,
               self.default_lambda)           
        
        return loss
    

    def lm(self, param_list: list, derivative_list: list, damping_parameter: int):
        """Implementation of the LevenbergMarquardt Step."""
        
        for i, params in enumerate(param_list):
            jacobian = derivative_list[i]
            transposed_jacobian = torch.t(jacobian)
            
            hessian = jacobian @ transposed_jacobian # J^T J = H - Square Matrix
            
            try:
                size = hessian.size()[0]
                identity = torch.eye(size)
            except IndexError: # Only one size.
                identity = 1
            
            equation = hessian - (damping_parameter * identity)
            
            if len(equation.size()) > 1:
                equation = torch.inverse(equation)
                equation = equation @ jacobian
            else:
                equation = float(equation) ** -1
                equation = equation * jacobian
            
            param_list[i].data = params.data - equation # Need to access the datas!!!!
            
            
            
# Source for hessian: https://en.wikipedia.org/wiki/Gauss%E2%80%93Newton_algorithm#Derivation_from_Newton.27s_method

"""
w1 = torch.randn(2, 50)
w1.requires_grad = True
print(w1)
w2 = torch.randn(2, 50)
loss = nn.MSELoss()
output = loss(w1, w2)
output.backward()

o = LevenbergMarquardt([w1], 1)
o.step()
print(w1)
"""