#God ide ved fejl: klik f8



#Import packages
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
plt.style.use("seaborn")




###Question1
m = 1 #m
v = 10 #v
eps= 0.3 #epsilon
tau0 = 0.4 #tax_0
tau1 = 0.1 #tax_1
kappa = 0.4 #kappa
w = 0.5 #w set with the initial value 1

#Defining utility as a function of labour supplu and consumption
def u_func(c,l,eps=eps,v=v):
    return np.argmax(np.log(c))-v*(l**(1+1/eps)/(1+1/eps))

#Defining function for consumption, where c*=x because of monoticity seen from eq(2)
def c_func(l,w,m=m,tau0=tau0,tau1=tau1,kappa=kappa):
    return m+w*l-(tau0*w*l+tau1*np.max(w*l-kappa,0))

#Defining the utility constraint such that c=c_func
def u_con(l,w,eps=eps,v=v,tau0=tau0,tau1=tau1,kappa=kappa):
    c = c_func(l,w,m=m,tau0=tau0,tau1=tau1,kappa=kappa)
    return u_func(c,l,v,eps)

#Creat an optimizing function for labour supply. 
def sol(w,v=v,eps=eps,tau0=tau0,tau1=tau1,kappa=kappa):
    guess=0.5 #Give the function a good guess for the value of l_ss
    l_ss = optimize.minimize(lambda l: -u_con(l,w,eps=eps,v=v,tau0=tau0,tau1=tau1,kappa=kappa), guess, method = 'SLSQP', bounds=[(0,1)])
    return l_ss
    print(l_ss.message)

#Checking if the sol function is optimizing correctly. 
print(sol(1)) #Test optimizer for w = 1
print(sol(1,eps=0.1)) #Test epsilon for eps=0.1






###Question2
#Set number of observations.
N=10000

#Generate vectors of optimal labour supply, consumption and wages.
w_vec = np.linspace(0.5,1.5,N) # Return evenly spaced numbers over a specified interval
l_vec = np.empty(N) # Return a new array of given (same N) shape and type, without initializing entries
c_vec = np.empty(N)

#I. optimal l's => loop through w and adding solutions for l to l_vec
for i,w in enumerate(w_vec):
    l_vec[i] = sol(w).x[0]
    
print(w_vec) # check elements
print(l_vec) # check elements

# II. optimal c's
for i,w in enumerate(w_vec):
    l = sol(w).x[0]
    c_vec[i] = c_func(l,w)

print(c_vec) # check elements

fig = plt.figure(figsize = (10,4))

# left plot
ax_left = fig.add_subplot(1,2,1)
ax_left.plot(w_vec,l_vec,lw=2,color='forestgreen')

ax_left.set_title('labor supply, $\ell^*$')
ax_left.set_xlabel('$w$')
ax_left.set_ylabel('$\ell^*$')
ax_left.grid(True)

# right plot
ax_right = fig.add_subplot(1,2,2)
ax_right.plot(w_vec,c_vec,lw=2,color='cornflowerblue')

ax_right.set_title('consumption, $c^*$')
ax_right.set_xlabel('$w$')
ax_right.set_ylabel('$c^*$')
ax_right.grid(True)





###Question3
seed=123
N=10000
mu_low=0.5
mu_high=1.5

np.random.seed(seed)
w_ran_vec=np.random.uniform(low=mu_low,high=mu_high,size=N)
print(w)

l_ss_vec=np.empty(N) # Return a new array of given (same N) shape and type, without initializing entries
c_ss_vec=np.empty(N)
# optimal l
for i,w in enumerate(w_ran_vec):
    l_ss_vec[i]=sol(w).x[0]
    
#optimal c
for i,w in enumerate(w_ran_vec):
    l=sol(w).x[0]
    c_ss_vec[i] = c_func(l,w)
    
print(l_ss_vec)
print(c_ss_vec)
    
def tax_rev(w_ran_vec,l_ss_vec, tau0=tau0,tau1=tau1,kappa=kappa):
    sum = 0
    for i in range(N):
        w=w_ran_vec[i]
        l=l_ss_vec[i]
        sum+=tau0*w*l+tau1*np.max(w*l-kappa,0)
    return sum
print(tax_rev(l_ss_vec,w_ran_vec))





###Question4
l_ss_vec_new=np.empty(N) # Return a new array of given (same N) shape and type, without initializing entries
c_ss_vec_new=np.empty(N)
# optimal l
for i,w in enumerate(w_ran_vec):
    l_ss_vec_new[i]=sol(w,eps=eps_new).x[0]
    
#optimal c
for i,w in enumerate(w_ran_vec):
    l=sol(w,eps=eps_new).x[0]
    c_ss_vec_new[i] = c_func(l,w)

print(c_ss_vec_new)

def tax_rev(w_ran_vec,l_SS_vec_new, tau0=tau0,tau1=tau1,kappa=kappa):
    sum = 0
    for i in range(N):
        w = w_ran_vec[i]
        l = l_SS_vec_new[i]
        sum += tau0*w*l+tau1*np.max(w*l-kappa,0)
    return sum
print(tax_rev(l_SS_vec_new,w_ran_vec))




###Question5
#Call on old functions from each question and see which gives the highest utility. (Suggest that one and report the tax rev in that case). 