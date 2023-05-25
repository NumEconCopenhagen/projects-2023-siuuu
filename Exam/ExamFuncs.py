#%%
import pandas as pd
from scipy.optimize import minimize
import numpy as np
import numpy as np

def utility_maximization_func(alpha, nu, kappa, w, tau):

    # Define L_star
    tilde_w = (1 - tau) * w
    L_star = (-kappa + np.sqrt(kappa**2 + 4 * alpha / nu * tilde_w**2)) / (2 * tilde_w)

    # Calculate G using L_star
    G = tau * w * L_star

    # Define utility
    C = kappa + (1 - tau) * w * L_star
    U = np.log(C**alpha * G**(1 - alpha)) - nu * L_star**2 / 2

    return L_star, G, U
