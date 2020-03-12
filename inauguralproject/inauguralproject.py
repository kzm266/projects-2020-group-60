#God ide ved fejl: klik f8

#Import packages
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import itertools

#Question 1. 
def c_ss(m=1, tau0 = 0.4, tau1 = 0.1, kappa = 0.4, w = 1, v = 10, eps = 0.3):
    """ solve for the steady state level of capital
    Args:
        s (float): saving rate
        g (float): technological growth rate
        n (float): population growth rate
        alpha (float): cobb-douglas parameter
        delta (float): capital depreciation rate 

    Returns:
        result (RootResults): the solution represented as a RootResults object
    """ 
    
    # a. define objective function
    l=range(0,1)
    x = m+w*l-(tau0*w*l+tau1*np.max(w*l-kappa,0))
    c=range(0,x)
    cstar = np.argmax(np.log(c))-v*((l**(1+1/eps))/(1+1/eps))

    #. b. call root finder
    cstar = optimize.root_scalar(cstar,method='bisect')
    
    return cstar
print(c_ss)


def l_ss(m=1, tau0 = 0.4, tau1 = 0.1, kappa = 0.4, w = 1, v = 10, eps = 0.3):
    """ solve for the steady state level of capital

    Args:
        s (float): saving rate
        g (float): technological growth rate
        n (float): population growth rate
        alpha (float): cobb-douglas parameter
        delta (float): capital depreciation rate 

    Returns:
        result (RootResults): the solution represented as a RootResults object
    """ 
    
    # a. define objective function
    l=range(0,1)
    x = m+w*l-(tau0*w*l+tau1*np.max(w*l-kappa,0))
    lstar = np.argmax(np.log(l))-v*((l**(1+1/eps))/(1+1/eps))

    #. b. call root finder
    lstar = optimize.root_scalar(lstar,method='bisect')
    
    return lstar
print(l_ss)