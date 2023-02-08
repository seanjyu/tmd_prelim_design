"""
TMD Preliminary Design

The following file contains all the functions used to calculate the
preliminary tmd design.
"""

from scipy import optimize
import plotly.graph_objects as go
import numpy as np
import pandas as pd


def undamped_dyn_factor_opt(m):
    return (1 + m) / (0.5 * m) ** .5 - dyn_amp

def curve_func(x, a, b, c, d):
    return a * np.exp(-b * x) + c * x + d

def interpolate_mass_ratio(damp_ratio, dyn_amp):
    # import data from Tsai and Lin (1993)
    xl_file = pd.read_csv('damped_system_opt_mass_ratio.csv')
    x_data = xl_file["m"]

    if damp_ratio in [0.02, 0.05, 0.1]:
        # if damping ratio is in data, use data
        y_data = xl_file[str(damp_ratio)]

    else:
        # if damping ratio not in data need to interpolate
        if damp_ratio > 0 and damp_ratio < 0.02:
            percentage_diff = damp_ratio / 0.02
            y_data = xl_file["0"] - percentage_diff * (
                        xl_file["0"] - xl_file["0.02"])

        elif damp_ratio > 0.02 and damp_ratio < 0.05:
            percentage_diff = (damp_ratio - 0.02) / 0.03
            y_data = xl_file["0.02"] - percentage_diff * (
                        xl_file["0.02"] - xl_file["0.05"])

        elif damp_ratio > 0.05 and damp_ratio < 0.1:
            percentage_diff = (damp_ratio - 0.05) / 0.05
            y_data = xl_file["0.05"] - percentage_diff * (
                        xl_file["0.05"] - xl_file["0.1"])

    # if required dynamic factor larger than largest y value clamp mass
    # ratio to 0.005
    if dyn_amp > y_data[0]:
        mass_ratio = 0.005
    else:
        # run curve fitting function
        popt, pcov = optimize.curve_fit(curve_func, x_data, y_data)

        # run root find to solve for optimum mass ratio
        global opt_a, opt_b, opt_c, opt_d
        opt_a = popt[0]
        opt_b = popt[1]
        opt_c = popt[2]
        opt_d = popt[3] - dyn_amp

        def curve_func_opt(x):
            return opt_a * np.exp(-opt_b * x) + opt_c * x + opt_d

        try:
            sol = optimize.root_scalar(curve_func_opt,
                                             bracket=[0.000000001, 0.1],
                                             method='brentq')
            mass_ratio = sol.root
        except ValueError:
            mass_ratio = "root_find_error"

    return mass_ratio


# function to plot dynamic amplification factor curve
def amplification_vs_f(damping_ratio, mass_ratio, f_ratio_opt,
                       tmd_d_ratio, rho):
    '''

    :param rho:
    :return:
    '''
    if int(damping_ratio) == 0:
        a = (((1 + mass_ratio) * f_ratio_opt ** 2 - rho ** 2) ** 2 +
             (2 * tmd_d_ratio * rho * f_ratio_opt *
              (1 + mass_ratio)) ** 2) ** 0.5

        b = (((1 - rho ** 2) * (
                    f_ratio_opt ** 2 - rho ** 2) - mass_ratio
              * rho ** 2 * f_ratio_opt ** 2) ** 2 +
             (2 * tmd_d_ratio * rho * f_ratio_opt *
              (1 - rho ** 2 * (1 + mass_ratio))) ** 2) ** 0.5

    else:
        a = rho ** 2 * ((f_ratio_opt ** (2) - rho ** (2)) ** (2) + (
                2 * rho * f_ratio_opt * tmd_d_ratio) ** 2) ** 0.5

        b = ((-mass_ratio * (f_ratio_opt ** (2)) * (rho ** 2) +
              (1 - rho ** (2)) * (
                          f_ratio_opt ** (2) - rho ** (2)) - 4 *
              damping_ratio * tmd_d_ratio * f_ratio_opt * rho ** (
                  2)) ** (2)
             + 4 * (damping_ratio * rho * (
                            f_ratio_opt ** (2) - rho ** (2))
                    + tmd_d_ratio * f_ratio_opt * rho * (
                                1 - rho ** (2) *
                                (1 + mass_ratio))) ** (2)) ** 0.5

    return a / b

def no_damper(damping_ratio, rho):
    '''

    :param rho:
    :return:
    '''
    return rho ** 2 / ((1 - rho ** 2) ** 2 +
                       (2 * damping_ratio * rho) ** 2) ** 0.5

def damped_building_factors(mass_ratio, damping_ratio):
    # using curve fit functions from Tsai and Lin (1993) find optimal
    # frequency and damping ratio
    f_ratio_opt = (1 - 0.5 * mass_ratio) ** 0.5 / (1 + mass_ratio) + \
                  (1 - 2 * damping_ratio ** 2) ** 0.5 - 1 - \
                  (2.375 - 1.034 * (mass_ratio) ** 0.5 - 0.426
                   * mass_ratio) * damping_ratio * (mass_ratio) ** (
                      0.5) \
                  - (3.730 - 16.903 * (mass_ratio) ** 0.5 + 20.496 *
                     mass_ratio) * damping_ratio ** 2 * (
                      mass_ratio) ** 0.5

    tmd_d_ratio = (mass_ratio * (3 - (0.5 * mass_ratio)) ** 0.5 /
                   (8 * (1 + mass_ratio) * (1 - mass_ratio))) ** 0.5 \
                  + \
                  (0.151 * damping_ratio - 0.17 * damping_ratio **
                   2) + \
                  (0.163 * damping_ratio + 4.98 * damping_ratio ** 2) \
                  * mass_ratio
    return f_ratio_opt, tmd_d_ratio

def tmd_prelim_design_function(dyn_amp_input, damping_ratio):
    x = np.linspace(0.7, 1.2, 100)

    global dyn_amp
    dyn_amp = dyn_amp_input

    if damping_ratio <= 0:
        try:
            undamped_dyn_factor_opt_sol = optimize.root_scalar(
                undamped_dyn_factor_opt,
                bracket=[0.000000001, 0.1],
                method='brentq')

            mass_ratio = undamped_dyn_factor_opt_sol.root

            # calculate f_opt
            f_ratio_opt = (1 - 0.5 * mass_ratio) ** (0.5) / (1 + mass_ratio)

            # calculate damping ratio
            tmd_d_ratio = (mass_ratio * (3 - (0.5 * mass_ratio) ** 0.5) /
                           (8 * (1 + mass_ratio) * (
                                       1 - 0.5 * mass_ratio))) ** 0.5

        except ValueError:
            return "root_find_error"

    else:

        # if building has damping ratio need to use interpolation
        # to find mass ratio

        mass_ratio = interpolate_mass_ratio(damping_ratio, dyn_amp)

        if mass_ratio == "root_find_error":
            return mass_ratio

        f_ratio_opt, tmd_d_ratio = damped_building_factors(
            mass_ratio,
            damping_ratio)

        max_dyn_factor = max(amplification_vs_f(damping_ratio, mass_ratio,
                                                f_ratio_opt, tmd_d_ratio,
                                                x))

        while max_dyn_factor > dyn_amp:
            mass_ratio = mass_ratio + 0.001
            f_ratio_opt, tmd_d_ratio = damped_building_factors(
                mass_ratio,
                damping_ratio)

            max_dyn_factor = max(
                amplification_vs_f(damping_ratio, mass_ratio,
                                   f_ratio_opt, tmd_d_ratio, x))

        # Apply a limit to mass ratio at 0.8
        if mass_ratio > 0.8:
            mass_ratio = 0.8
            f_ratio_opt, tmd_d_ratio = damped_building_factors(
                mass_ratio,
                damping_ratio)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,
                             y=amplification_vs_f(damping_ratio,
                                                  mass_ratio,
                                                  f_ratio_opt,
                                                  tmd_d_ratio, x),
                             mode='lines',
                             name='TMD'))
    fig.add_trace(go.Scatter(x=x,
                             y=no_damper(damping_ratio, x),
                             marker=dict(
                                 color='MediumPurple',
                                 line=dict(
                                     color='MediumPurple',
                                     width=2
                                     )),
                             mode = 'lines',
                             name = 'No TMD'))
    #fig.update_layout(legend_title="Legend Title")

    fig.update_yaxes(range=[0, dyn_amp + 3])

    return [mass_ratio, f_ratio_opt, tmd_d_ratio, fig]


