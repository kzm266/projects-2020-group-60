#God ide ved fejl: klik f8
pip3 install numpy
pip3 install scipy  
pip3 install itertools

#Import packages
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import itertools



##Question 1. 
m = 1 #m
v = 10 #v
eps= 0.3 #epsilon
tau0 = 0.4 #tax_0
tau1 = 0.1 #tax_1
kappa = 0.4 #kappa
w = 0.5 #w set with the initial value 1

#Defining utility as a function of labour supplu and consumption
def utility(c,l,eps,v):
    u = np.argmax(np.log(c))-v*((l**(1+1/eps))/(1+1/eps))
    return u

#Defining the budget constraint
def constraint(money,w,l,tax0,tax1,kappa):
    x = m+w*l-(tau0*w*l+tau1*np.max(w*l-kappa,0))
    return x

from scipy import optimize

#Objective function which returns negative values to minimize
def target(l,w,eps,v,tax0,tax1,kappa):
    c = constraint(m,w,l,tau0,tau1,kappa)
    return -utility(c,l,eps,v)

#Call the solver using the functions: constraint and target.
def optimiser(l,w,eps,v,tax0,tax1,kappa,m):
    solution = optimize.minimize_scalar(target, method = 'bounded',bounds=(0,1), args = (w,eps,v,tau0,tau1,kappa))
    
#Unpack optimal labour supply, consumption and individual utility
    lss = solution
    css = constraint(m,w,lss,tau0,tau1,kappa)
    uss = utility(lss,css,eps,v)
    return [lss,css,uss]



##Question2
import matplotlib.pyplot as plt
plt.style.use("seaborn")

#Set number of observations.
N=10000

#Generate vectors of optimal labour supply and consumption given wages.
w_vec=np.linspace(0.5,1.5,N)
l_vec=np.empty(N)
c_vec=np.empty(N)
for i,w in enumerate(w_vec):
    lc_bundle=optimiser(w,eps,v,tau0,tau1,kappa,m)
    #2.2.2. As the optimiser function returns a list of optimal labour supply and feasible consumption,
            #extract the relevant results. Copy them to the list of labour supply and consupmtion.
    l_vec[i]=lc_bundle[0]
    c_vec[i]=lc_bundle[1]

#Create figure
fig = plt.figure(figsize=(10,4))

#Left side plot: Labour supply.
ax_left = fig.add_subplot(1,2,1)
ax_left.plot(w_vec,l_vec)

ax_left.set_title('Optimal labour supply, wages between 0.5-1.5')
ax_left.set_xlabel('$w$')
ax_left.set_ylabel('$l^\star$')
ax_left.grid(True)

#Right side plot: Consumption.
ax_right = fig.add_subplot(1,2,2)
ax_right.plot(w_vec,c_vec)

ax_left.set_title('Optimal consumption, wages between 0.5-1.5')
ax_right.set_xlabel('$w$')
ax_right.set_ylabel('$c^\star$')
ax_right.grid(True)

##Question3
def taxrev(c,l,eps,v):
    T = sum(tau0*w_vec*lss_vec+tau1)
    return T 