"""
TMD Preliminary Design

Based on chapter 5 of textbook 'Structural Motion Engineering'
by Connor, J. and Laflamme, S. (2014)

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
from tmd_preliminary_design_functions import *

# main loop
# inputs
#dyn_amp = 15
#damping_ratio = 0.0
# a = tmd_prelim_design_function(dyn_amp, damping_ratio)
#print(a)
#a[3].show()

# streamlit UI

# Main text
st.title('TMD Preliminary Design')
st.markdown('The following webapp provides preliminary design variables '
            'for a tuned mass damper. These design variables are:')
st.markdown("Mass Ratio $$\Big(\\frac{m_{damper}}{m_{building}}" \
            "\Big)$$, Frequency Ratio $\Big(\\frac{f_{damper}}" \
            "{f_{building}}\Big)$, Damping Ratio (of damper) "
            "$(\\xi_{damper})$")
st.markdown('These variables were found under the assumption that the '
            'building acts like an SDOF system with a tuned mass damper'
            'attached to the top. Sometimes, if the input dynamic response'
            ' factor is too low an error will occur. An explanation on how'
            ' this app works can be found here: '
            'https://seanjyu.github.io/tmd_preliminary_design/')

# Sidebar - inputs
st.sidebar.title("Inputs")
dyn_amp = st.sidebar.number_input("Required Dynamic Amplification Factor",
                                  min_value=0.0, format='%f', step=0.5)
damping_ratio = st.sidebar.number_input("Building Damping Ratio",
                                        min_value=0.0, max_value=0.1,
                                        format='%f',
                                        step=0.01)
st.sidebar.markdown('To assume building is undamped set damping ratio '
                    'to 0.')

# When submit button is pressed check for illegal inputs and if there
# are errors output error message. If no errors put sidebar values
# into functions then plot optimal design.
if st.sidebar.button("Submit"):
    sol = tmd_prelim_design_function(dyn_amp, damping_ratio)
    if sol == "root_find_error":
        st.error("Error with root finding, please increase minimum "
                    "required dynamic amplification factor.")
    else:
        st.plotly_chart(sol[3])
        mass_result_str = "Mass Ratio $\Big(\\frac{m_{damper}}{m_{building}}" \
                          "\Big)$ = " + "{0:.3f} \n".format(sol[0])
        f_result_str = "Frequency Ratio $\Big(\\frac{f_{damper}}" \
                       "{f_{building}}\Big)$ = " + "{0:.3f} \n".format(sol[1])
        damping_result_str = "Damping Ratio (of damper) $(\\xi_{damper})$ = "\
                             + "{0:.3f} \n".format(sol[2])
        st.markdown(mass_result_str)
        st.markdown(f_result_str)
        st.markdown(damping_result_str)






