#%%
from types import SimpleNamespace
import time
import numpy as np
from scipy import optimize

class OLGModelClass():

    def __init__(self,do_print=True):
        """ create the model """

        self.par = SimpleNamespace()
        self.sim = SimpleNamespace()
        self.setup()
        self.allocate()
    
    def setup(self):
        """ baseline parameters """

        par = self.par

        # a. household
        par.sigma = 1 # CRRA coefficient
        par.beta = 0.22 # discount factor

        # b. firms
        par.production_function = 'cobb-douglas'
        par.alpha = 0.33 # capital weight
        par.theta = 0 # substitution parameter
        par.delta = 0 # depreciation rate
        par.A = 10 # TFP

        # c. government
        par.tau_w = 0 # labor income tax
        par.tau_r = 0 # capital income tax

        # d. misc
        par.K_lag_ini = 0 # initial capital stock
        par.B_lag_ini = 0 # initial government debt
        par.simT = 50 # length of simulation

    def allocate(self):
        """ allocate arrays for simulation """
        
        par = self.par
        sim = self.sim

        # a. list of variables
        household = ['C1','C2']
        firm = ['K','Y','K_lag']
        prices = ['w','rk','rb','r','rt']
        government = ['G','T','B','balanced_budget','B_lag']

        # b. allocate
        allvarnames = household + firm + prices + government
        for varname in allvarnames:
            sim.__dict__[varname] = np.nan*np.ones(par.simT)

    def simulate(self,do_print=True):
        """ simulate model """

        t0 = time.time()

        par = self.par
        sim = self.sim
        
        # a. initial values
        sim.K_lag[0] = par.K_lag_ini
        sim.B_lag[0] = par.B_lag_ini

        # b. iterate
        for t in range(par.simT):
            
            # i. simulate before s
            simulate_before_s(par,sim,t)

            if t == par.simT-1: continue          

            # i. find bracket to search
            s_min,s_max = find_s_bracket(par,sim,t)

            # ii. find optimal s
            obj = lambda s: calc_euler_error(s,par,sim,t=t)
            result = optimize.root_scalar(obj,bracket=(s_min,s_max),method='bisect')
            s = result.root

            # iii. simulate after s
            simulate_after_s(par,sim,t,s)


def find_s_bracket(par,sim,t,maxiter=1000,do_print=False):
    """ find bracket for s to search in """

    # a. maximum bracket
    s_min = 0.0 + 1e-9 # save almost nothing
    s_max = 1.0 - 1e-9 # save almost everything

    # b. saving a lot is always possible 
    value = calc_euler_error(s_max,par,sim,t)
    sign_max = np.sign(value)

    # c. find bracket      
    lower = s_min
    upper = s_max

    it = 0
    while it < maxiter:
                
        # i. midpoint and value
        s = (lower+upper)/2 # midpoint
        value = calc_euler_error(s,par,sim,t)

        # ii. check conditions
        valid = not np.isnan(value)
        correct_sign = np.sign(value)*sign_max < 0
        
        # iii. next step
        if valid and correct_sign: # found!
            s_min = lower
            s_max = upper
            return s_min,s_max
        elif not valid: # too low s -> increase lower bound
            lower = s
        else: # too high s -> increase upper bound
            upper = s

        # iv. increment
        it += 1

    raise Exception('cannot find bracket for s')

def calc_euler_error(s,par,sim,t):
    """ target function for finding s with bisection """

    # a. simulate forward
    simulate_after_s(par,sim,t,s)
    simulate_before_s(par,sim,t+1) # next period

    # c. Euler equation
    LHS = sim.C2[t+1]**(par.sigma)
    RHS = (1+sim.rt[t+1])*par.beta * sim.C1[t]**(par.sigma)
    return LHS-RHS

def simulate_before_s(par,sim,t):
    """ simulate forward """

    if t > 0:
        sim.K_lag[t] = sim.K[t-1]
        sim.B_lag[t] = sim.B[t-1]

    # a. production and factor prices
    if par.production_function == 'cobb-douglas':

        # i. production
        sim.Y[t] = par.A*sim.K_lag[t]**par.alpha

        # ii. factor prices
        sim.rk[t] = par.A * par.alpha * sim.K_lag[t]**(par.alpha-1)
        sim.w[t] = (1-par.alpha) * sim.K_lag[t]**(par.alpha)


    # b. no-arbitrage and after-tax return
    sim.r[t] = sim.rk[t]-par.delta # after-depreciation return
    sim.rb[t] = sim.r[t] # same return on bonds
    sim.rt[t] = (1-par.tau_r)*sim.r[t] # after-tax return

    # c. consumption
    sim.C2[t] = (1+sim.rt[t])*(sim.K_lag[t]+sim.B_lag[t])

    # d. government
    sim.T[t] = par.tau_r*sim.r[t]*(sim.K_lag[t]+sim.B_lag[t]) + par.tau_w*sim.w[t]

    if sim.balanced_budget[t]:
        sim.G[t] = sim.T[t] - sim.r[t]*sim.B_lag[t]

    sim.B[t] = (1+sim.r[t])*sim.B_lag[t] - sim.T[t] + sim.G[t]

def simulate_after_s(par,sim,t,s):
    """ simulate forward """

    # a. consumption of young
    sim.C1[t] = (1-par.tau_w)*sim.w[t]-s
    # b. end-of-period stocks
    I = sim.Y[t] - sim.C1[t] - sim.C2[t] - sim.G[t]
    sim.K[t] = (1-par.delta)*sim.K_lag[t] + I
    print(sim.K[t])
#%%
model = OLGModelClass()
model.simulate()



