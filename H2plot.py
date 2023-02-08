from tmd_preliminary_design_functions import amplification_vs_f
import numpy as np
import plotly.graph_objects as go
x = np.linspace(0.8, 1.2, 100)

mass_ratio = 0.01
f_ratio_opt = 1
fig = go.Figure()
fig.add_trace(go.Scatter(x=x,
                         y=amplification_vs_f(0, mass_ratio, f_ratio_opt, 1, x),
                         mode='lines',
                         name='1'))
fig.add_trace(go.Scatter(x=x,
                         y=amplification_vs_f(0, mass_ratio, f_ratio_opt, 0.0, x),
                         mode='lines',
                         name='0'))
fig.add_trace(go.Scatter(x=x,
                         y=amplification_vs_f(0, mass_ratio, f_ratio_opt, 0.1, x),
                         mode='lines',
                         name='0.1'))

fig.add_trace(go.Scatter(x=x,
                         y=amplification_vs_f(0, mass_ratio, f_ratio_opt, 0.05, x),
                         mode='lines',
                         name='0.05'))

fig.add_trace(go.Scatter(x=x,
                         y=amplification_vs_f(0, mass_ratio, f_ratio_opt, 0.03, x),
                         mode='lines',
                         name='0.03'))

fig.update_yaxes(range=[0, 25])
fig.update_layout(legend_title_text='TMD Damping Ratio')
html = fig.to_html()

with open("h2plot.html", "w", encoding="utf-8") as f:
    f.write(html)