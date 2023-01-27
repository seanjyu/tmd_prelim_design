import pandas as pd
import scipy.optimize
import matplotlib.pyplot as plt
import numpy as np
import math

'''
File for testing curve fitting on optimal mass ratio vs amplification factor
Data is from the paper: 

Tsai, H.-C., and Lin, G.-C. (1993). 
“Optimum tuned-mass dampers for minimizing steady-state response of 
support-excited and damped systems.” 
Earthquake Engineering & Structural Dynamics, 22(11), 957–973. 
'''

# import data from Tsai and Lin (1993)
xl_file = pd.read_csv('damped_system_opt_mass_ratio.csv')

damp_ratio = 0.01
dyn_factor = 5

# Use exponential + linear function for fitting
def curve_func (x, a, b, c, d):
    return a * np.exp(-b *x) + c * x + d

x_data = xl_file["m"]

if damp_ratio in [0.02, 0.05, 0.1]:
    # if damping ratio is in data, use data
    y_data = xl_file[str(damp_ratio)]

else:
    # if damping ratio not in data need to interpolate
    if  damp_ratio > 0 and damp_ratio < 0.02:
        percentage_diff = damp_ratio / 0.02
        # print(percentage_diff * (xl_file["0"] - xl_file["0.02"]), percentage_diff * (xl_file["0"] - xl_file["0.02"]))
        y_data = xl_file["0"] - percentage_diff * (xl_file["0"] - xl_file["0.02"])
        print(type(y_data))

    elif damp_ratio > 0.02 and damp_ratio < 0.05:
        percentage_diff = (damp_ratio - 0.02) / 0.03
        y_data = xl_file["0.02"] - percentage_diff * (xl_file["0.02"] - xl_file["0.05"])

    elif damp_ratio > 0.05 and damp_ratio < 0.1:
        percentage_diff = (damp_ratio - 0.05) / 0.05
        y_data = xl_file["0.05"] - percentage_diff * (xl_file["0.05"] - xl_file["0.1"])


# if required dynamic factor larger than largest y value clamp mass ratio to 0.005
if dyn_factor > y_data[0]:
    mass_ratio = 0.005
else:
    # run curve fitting function
    popt, pcov = scipy.optimize.curve_fit(curve_func, x_data, y_data)

    # run root find to solve for optimum mass ratio
    global opt_a, opt_b, opt_c, opt_d
    opt_a = popt[0]
    opt_b = popt[1]
    opt_c = popt[2]
    opt_d = popt[3] - dyn_factor

    def curve_func_opt(x):
        return opt_a * np.exp(-opt_b * x) + opt_c * x + opt_d

    sol = scipy.optimize.root_scalar(curve_func_opt, bracket=[0.000000001, 0.1], method='brentq')
    mass_ratio = sol.root

# plot for study
# run curve fitting function
popt, pcov = scipy.optimize.curve_fit(curve_func, x_data, y_data)
plt.plot(xl_file["m"], curve_func(xl_file["m"], *popt), '--')
plt.plot(xl_file["m"], xl_file["0.02"], label = "0.02")
plt.plot(xl_file["m"], xl_file["0.1"], label = "0.1")
plt.plot(xl_file["m"], xl_file["0.05"], label = "0.05")
plt.plot(xl_file["m"], xl_file["0"], label = "0")
# plt.loglog(xl_file["m"], curve_func(xl_file["m"], *popt), '--')
# plt.loglog(xl_file["m"], xl_file["0.02"], label = "0.02")
# plt.loglog(xl_file["m"], xl_file["0.1"], label = "0.1")
# plt.loglog(xl_file["m"], xl_file["0.05"], label = "0.05")
# plt.loglog(xl_file["m"], xl_file["0"], label = "0")