# H4_opt_mass_sol = optimize.root_scalar(H4_opt_to_mass, bracket = [0.000000001, 0.1], method='brentq')

# choose smaller m ratio
# m_ratio = min(H2_opt_mass_sol.root, H4_opt_mass_sol.root)


def amplification_vs_f(rho):
    # a = (rho ** 2) * ((f_ratio_opt ** (2) * (1 + mass_ratio) - rho ** (2)) ** (2) + (
    #             2 * rho * f_ratio_opt * tmd_d_ratio * (1 + mass_ratio)) ** 2) ** 0.5
    # b = (- (f_ratio_opt * rho) ** 2 * mass_ratio + (1 - rho ** 2) * (
    #             f_ratio_opt ** 2 - rho ** 2) - 4 * damping_ratio * tmd_d_ratio * f_ratio_opt * (
    #                  rho ** 2)) ** 2 + 4 * (
    #                 damping_ratio * rho * (f_ratio_opt ** 2 - rho ** 2) + tmd_d_ratio * f_ratio_opt * rho * (
    #                     1 - rho ** 2 * (1 + mass_ratio)) ** 2)
    # b = ((- mass_ratio * (f_ratio_opt ** (2)) * (rho ** 2) + (rho ** (2) -
    # 1) * (rho ** (2) - f_ratio_opt ** (2)) - 4 * damping_ratio *
    # tmd_d_ratio * f_ratio_opt * rho ** (2)) ** (2) + 4 * damping_ratio **
    # (2) * rho ** (2) * (tmd_d_ratio * f_ratio_opt * (rho ** (2) +
    # mass_ratio * rho ** (2) - 1) + damping_ratio * (rho ** (2) -
    # f_ratio_opt ** (2)) ** (2))) ** 0.5
