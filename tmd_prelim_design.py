"""
Multi-Tiered Pendulum TMD Preliminary Design

Based on chapter 4 of textbook 'Intro to Structural Motion Control'

UI run using streamlit

User inputs
- dyn_max - Dynamic amplification factor constraint for building
- Maximum tmd mass ratio

Outputs
- Damper mass as a ratio of
- Damper Frequency
- Optimum height

Packages
-
"""
import streamlit as st

global dyn_amp, f_ratio_opt, damping_ratio, tmd_d_ratio, H2_opt_mass

# functions
def H2_opt_to_mass(m):
    return (1 + m) / (0.5 * m) ** .5 - dyn_amp

def H4_opt_to_mass(m):
    rho_sq = 1 / (1 + m)
    f_sq = (1 - 0.5 * m) / (1 + m)**2
    damp_coeff_sq = m * (3 - (0.5 * m)** 0.5) / (8 * (1 + m) *
                                                 (1 - 0.5 * m))
    return 1 / (((1 - rho_sq) * (f_sq - rho_sq) - m * rho_sq * f_sq)**2 +
                4 * damp_coeff_sq * rho_sq * f_sq * (1 - rho_sq * (1 - m))
                ** 2) ** 0.5 - dyn_amp

def curve_func(x, a, b, c, d):
    return a * np.exp(-b * x) + c * x + d

def interpolate_mass_ratio(damp_ratio, dyn_amp):

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

        sol = optimize.root_scalar(curve_func_opt,
                                         bracket=[0.000000001, 0.1],
                                         method='brentq')
        mass_ratio = sol.root
    return mass_ratio

# main loop
# inputs
dyn_amp = 15
damping_ratio = 0.09

if damping_ratio == 0:
    H2_opt_mass_sol = optimize.root_scalar(H2_opt_to_mass,
                                           bracket = [0.000000001, 0.1],
                                           method='brentq')

    mass_ratio = H2_opt_mass_sol.root
    print('hi')

    # calculate f_opt
    f_ratio_opt = (1 - 0.5 * mass_ratio) ** (0.5) / (1 + mass_ratio)

    # calculate damping ratio
    tmd_d_ratio = (mass_ratio * (3 - (0.5 * mass_ratio) ** 0.5 ) /
                   (8 * (1 + mass_ratio) * (1 - 0.5 * mass_ratio))) ** 0.5

else:

    # if building has damping ratio need to use interpolation
    # to find mass ratio
    print('hey')
    # import data from Tsai and Lin (1993)
    xl_file = pd.read_csv('damped_system_opt_mass_ratio.csv')
    x_data = xl_file["m"]

    mass_ratio = interpolate_mass_ratio(damping_ratio, dyn_amp) + 0.004

    # using curve fit functions from Tsai and Lin (1993) find optimal
    # frequency and damping ratio
    f_ratio_opt = (1 - 0.5 * mass_ratio) ** 0.5 / (1 + mass_ratio) +\
                  (1 - 2 * damping_ratio ** 2) ** 0.5 - 1 - \
                  (2.375 - 1.034 * (mass_ratio) ** 0.5 - 0.426
                   * mass_ratio) * damping_ratio * (mass_ratio) ** (0.5) \
                  - (3.730 - 16.903 * (mass_ratio) ** 0.5 + 20.496 *
                  mass_ratio) * damping_ratio ** 2 * (mass_ratio) ** 0.5

    tmd_d_ratio = (mass_ratio * (3 - (0.5 * mass_ratio)) ** 0.5 /
                  (8 * (1 + mass_ratio) * (1 - mass_ratio))) ** 0.5 + \
                  (0.151 * damping_ratio - 0.17 * damping_ratio ** 2) + \
                  (0.163 * damping_ratio + 4.98 * damping_ratio ** 2) \
                  * mass_ratio
    # print(mass_ratio)
print(f_ratio_opt, tmd_d_ratio)



# for plotting
# plot dynamic amplification factor curve
def amplification_vs_f(rho):
    '''

    :param rho:
    :return:
    '''
    if int(damping_ratio) == 0:
        a = (((1 + mass_ratio) * f_ratio_opt ** 2 - rho ** 2) ** 2 + (2 * tmd_d_ratio * rho * f_ratio_opt * (1 + mass_ratio)) ** 2) ** 0.5
        b = (((1 - rho ** 2) * (f_ratio_opt ** 2 - rho ** 2) - mass_ratio * rho ** 2 * f_ratio_opt ** 2) ** 2 + (2 * tmd_d_ratio * rho * f_ratio_opt * (1 - rho ** 2 * (1 + mass_ratio))) ** 2) ** 0.5
    else:
        a = rho ** 2 * ((f_ratio_opt ** (2) - rho ** (2)) ** (2) + (
                 2 * rho * f_ratio_opt * tmd_d_ratio) ** 2) ** 0.5

        b = ((-mass_ratio * (f_ratio_opt ** (2)) * (rho ** 2) +
            (1 - rho ** (2)) * (f_ratio_opt ** (2) - rho ** (2)) - 4 *
            damping_ratio * tmd_d_ratio * f_ratio_opt * rho ** (2)) ** (2) +
            4 * (damping_ratio * rho * (f_ratio_opt ** (2) - rho ** (2)) +
            tmd_d_ratio * f_ratio_opt * rho * (1 - rho ** (2) *
            (1 + mass_ratio))) ** (2) ) ** 0.5
    return a/b

def no_damper(rho):
    return rho ** 2 / ((1 - rho ** 2) ** 2 + (2 * damping_ratio * rho) ** 2) ** 0.5
#mass_ratio = mass_ratio * 1.1
# f_ratio_opt = 0.965
# damping_ratio = 0.02
# tmd_d_ratio = 0.105
x = np.linspace(0.8, 1.2, 100)
plt.plot(x, amplification_vs_f(x))
# tmd_d_ratio = 0.001
# plt.plot(x, no_damper(x))
print(max(amplification_vs_f(x)))

# H2_opt_input = 0
# H4_opt_input = 0
# m = np.linspace(0.000001, 0.1, 200)
# fig = px.line(x = m, y = H2_opt_to_mass(m))
# fig.update_layout(yaxis_range=[0, 25])
# fig.show()
#
# fig_1 = px.line(x = m, y = H4_opt_to_mass(m))
# fig_1.update_layout(yaxis_range=[0, 300])
# fig_1.show()


# streamlit UI
#
# # Main text
# st.title('TMD Preliminary Design')
# st.markdown('This webapp ')
#
# # Sidebar - inputs
# st.sidebar.title("Inputs")
# dyn_amp = st.sidebar.number_input("Required Dynamic Amplification Factor",
#                                   min_value=0.0, format='%f', step=1.0)
# damping_ratio = st.sidebar.number_input("Building Damping Ratio",
#                                         min_value=0.0, max_value=0.1,
#                                         format='%f',
#                                         step=0.01)
# st.sidebar.markdown('To assume building is undamped set damping ratio '
#                     'to 0.')

# When submit button is pressed check for illegal inputs and if there
# are errors output error message. If no errors put sidebar values
# into functions then plot optimal design.
#if st.sidebar.button("Submit"):




