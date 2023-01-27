from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

global rho, m, f, eta_b, eta_d, amp_const
#rho = 0.1
m = 0.07
#f = 1
eta_b = 0.05
eta_d = 0.2

def amp_vs_rho(x):
    rho = x[0]
    m = x[0]
    #f = x[1]
    f = (1 - 0.5 * m) ** 0.5 / (1 + m) + (1 - 2 * eta_b** 2) ** 0.5 - 1
    eta_d = (m * (3 - (0.5 * m)) ** 0.5 / (8 * (1 + m) * (1 - m))) ** 0.5
    a = rho ** 2 * ((f ** 2 * ( 1 - m) - rho ** 2) ** 2 + (2 * rho *
        f * eta_d * (1 + m)) ** 2 ) ** 0.5
    b = (- (f * rho) ** 2 * m + (1 - rho ** 2) * (f ** 2 - rho ** 2) - 4 *
        eta_b * eta_d * f * (rho ** 2)) ** 2 + 4 * (eta_b * rho *
        (f ** 2 - rho ** 2) + eta_d * f * rho *
        (1 - rho ** 2 * (1 + m)) ** 2)
    return a/b

x_0 = [0.05, 0.9]
# larger than 0 constraint if needed
# constraints={'type': 'ineq', 'fun':amp_factor}
sol = optimize.minimize(amp_factor, x_0, method="Nelder-Mead", bounds=[(0.001, 0.15), (0.7,1.1)],options= {'xatol': 1e-8, 'disp':True, 'return_all': True})
print(sol)
