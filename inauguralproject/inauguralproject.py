#Import packages
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt



###Question1
#Defining parameters.
m = 1 #cash-on-hand.
v = 10 #scales the disutility of labor.
eps= 0.3 #elasticity of labor supply
tau0 = 0.4 #standard labor income tax.
tau1 = 0.1 #top bracket labor income tax.
kappa = 0.4 #the cut-off for the top labor income bracket.
w = 0.5 #wage rate set with the initial value 0.5.

#Defining utility as a function of labour supplu and consumption seen in eq(1).
def u_func(c,l,eps,v):
    return np.log(c)-v*(l**(1+1/eps)/(1+1/eps))

#Defining function for consumption, where c*=x because of monoticity seen from eq(2).
def c_func(l,w,m,tau0,tau1,kappa):
    return m+w*l-(tau0*w*l+tau1*np.max(w*l-kappa,0))

#Defining the utility constraint such that c=c_func.
def u_con(l,w,eps,v,tau0,tau1,kappa):
    c = c_func(l,w,m,tau0,tau1,kappa)
    return -u_func(c,l,v,eps)

#Defining a function for the solution of the utility maximization problem. 
def sol(w,eps,v,tau0,tau1,kappa,m):
    l_sol=optimize.minimize_scalar(u_con, method = 'bounded',bounds = (0,1), args = (w,eps,v,tau0,tau1,kappa))
    l_ss = l_sol.x
    c_ss = c_func(m,w,l_ss,tau0,tau1,kappa)
    u_ss = u_func(l_ss,c_ss,eps,v)
    return [l_ss,c_ss,u_ss]





###Question2
#Set number of observations.
N=10000

#Generate vectors for labour supply, consumption and wages.
w_vec = np.linspace(0.5,1.5,N) #this linespace() command return evenly spaced numbers over a specified interval.
l_vec = np.empty(N) #returns a new array of given (same N) shape and type, without initializing entries.
c_vec = np.empty(N) #returns a new array of given (same N) shape and type, without initializing entries.

for i,w in enumerate(w_vec):
    lc_bundle = sol(w,eps,v,tau0,tau1,kappa,m)
    l_vec[i] = lc_bundle[0]
    c_vec[i] = lc_bundle[1]

#Defining the figure's.
fig = plt.figure(figsize=(10,4))

#Left-side plot.
ax_left=fig.add_subplot(1,2,1)
ax_left.plot(w_vec,l_vec,color='yellow')

ax_left.set_title('Labor supply, $l^*$')
ax_left.set_xlabel('$w$')
ax_left.set_ylabel('$l^*$')
ax_left.grid(True)

#Right-side plot.
ax_right = fig.add_subplot(1,2,2)
ax_right.plot(w_vec,c_vec,color='blue')

ax_right.set_title('Consumption, $c^*$')
ax_right.set_xlabel('$w$')
ax_right.set_ylabel('$c^*$')
ax_right.grid(True)

#Ploting figure. 
plt.show()




###Question3
#Defining the uniform distribution of wage rate with random values saved by a seed number. 
N=10000
np.random.seed(100)
w_uni=np.random.uniform(low=0.5,high=1.5,size=N)

#Defining optimal labor supply by creating an empty list and iterating each wage rate. 
l_opt = np.empty(N) #this np.empty-command returns a new array of given (same N) shape and type, without initializing entries.
for i,w in enumerate(w_uni):
    lc_bundle = sol(w,eps,v,tau0,tau1,kappa,m)
    l_opt[i] = lc_bundle[0]

#Defining total tax revenue.  
def tax_rev(l_list): #this function uses a list of every individual labor supplier as parameter.
    #creating empty list to contain every revenue of each individual's paid tax.
    tax_list = np.empty(10000)
    #calculating the individual consumer tax revenue and summing it up.
    for i in range(10000):
        tax_list[i] = tau0*w_uni[i]*l_list[i]+tau1*np.max(w_uni[i]*l_list[i]-kappa,0)
    #returning the total sum of tax revenue. 
    return np.sum(tax_list)

#Print out total revenue. 
print(tax_rev(l_opt))



###Question4
#Defining new epsilion to the value of 0.1 given in the assignment. 
eps_new=0.1

#Redefining optimal labor supply and consumption given the new epsilion value. 
l_opt_new = np.empty(N)
c_opt_new = np.empty(N)
for i,w in enumerate(w_uni):
    lc_bundle=sol(w,eps_new,v,tau0,tau1,kappa,m)
    l_opt_new[i] = lc_bundle[0]
    c_opt_new[i] = lc_bundle[1]

#Print out total tax revenue for this new case. 
print(tax_rev(l_opt_new))



###Question5
#We worn't sure of how to tackle this question. 
