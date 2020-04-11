# run in commandline using: bokeh serve --show covid_sg_transform.py
import bokeh
from bokeh.io import curdoc
from bokeh.layouts import layout, column, row
from bokeh.plotting import figure, ColumnDataSource, show, output_file, show
from bokeh.core.properties import field
from bokeh.models import HoverTool, SingleIntervalTicker, Slider, Button, Label, CategoricalColorMapper
import numpy as np
import pandas as pd

df = pd.read_excel('covid_sg_transform.xlsx')
days = df['Days Since 22 Jan 2020'].tolist()
type = df["Infection Source"].unique().tolist()
data = {}
for day in days:
    df_day = df[df['Days Since 22 Jan 2020'] == day]
    data[day] = df_day.reset_index().to_dict('series')

source = ColumnDataSource(data=data[days[0]])

plot = figure(title='Covid-19 SG Trajectories', plot_width=800, plot_height=800, x_range=(1, 2000), y_range=(1, 2000), x_axis_type="log", y_axis_type="log")
plot.xaxis.axis_label = "Cumulative Cases"
plot.yaxis.axis_label = "New Cases in Past Week"

df[df['Infection Source'] == "Imported case"]["Cumulative Cases"]
df[df['Infection Source'] == "Imported case"]["New Confirmed Cases (Past Week)"]

plot.multi_line([ df[df['Infection Source'] == "Imported case"]["Cumulative Cases"], df[df['Infection Source'] == "Local transmission"]["Cumulative Cases"], df[df['Infection Source'] == "Total"]["Cumulative Cases"], df[df['Infection Source'] == "New Confirmed Cases = Cumulative Cases"]["Cumulative Cases"], df[df['Infection Source'] == "Foreign Worker Dormitories"]["Cumulative Cases"] ],
                [ df[df['Infection Source'] == "Imported case"]["New Confirmed Cases (Past Week)"], df[df['Infection Source'] == "Local transmission"]["New Confirmed Cases (Past Week)"], df[df['Infection Source'] == "Total"]["New Confirmed Cases (Past Week)"], df[df['Infection Source'] == "New Confirmed Cases = Cumulative Cases"]["New Confirmed Cases (Past Week)"], df[df['Infection Source'] == "Foreign Worker Dormitories"]["New Confirmed Cases (Past Week)"] ],
                color=['#440154', '#404387', '#29788E', '#22A784', '#79D151', '#FDE724'],
                alpha=[0.3, 0.3, 0.3, 0.3, 0.3],
                line_width=4)

label = Label(x=80, y=1, text="Day " + str(days[0]), text_font_size='93px', text_color='#eeeeee')
plot.add_layout(label)

color_mapper = CategoricalColorMapper(palette=bokeh.palettes.viridis(6), factors=type)
plot.circle(
    x='Cumulative Cases',
    y='New Confirmed Cases (Past Week)',
    size=36,
    source=source,
    fill_color={'field': 'Infection Source', 'transform': color_mapper},
    fill_alpha=1.0,
    line_color='#7c7e71',
    line_width=0.5,
    line_alpha=0.5,
    legend=field('Infection Source'),
)
plot.legend.location = "top_left"
plot.title.text_font_size = "25px"
plot.add_tools(HoverTool(tooltips=[ ("Infection Source", "@{Infection Source}"),
                                    ("Cum Cases", "@{Cumulative Cases}"),
                                    ("New Cases", "@{New Confirmed Cases (Past Week)}")],
                                    show_arrow=False, point_policy='follow_mouse'))


def animate_update():
    day = slider.value + 1
    if day > days[-1]:
        day = days[0]
    slider.value = day


def slider_update(attrname, old, new):
    day = slider.value
    label.text = str(day)
    source.data = data[day]

slider = Slider(start=days[0], end=days[-1], value=days[0], step=1, title="Days Since 22 Jan 2020")
slider.on_change('value', slider_update)

callback_id = None

def animate():
    global callback_id
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        callback_id = curdoc().add_periodic_callback(animate_update, 100)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)

button = Button(label='► Play', width=60)
button.on_click(animate)

layout = row(column(plot, slider, button))

curdoc().title = "Covid-19 SG Trajectories"
curdoc().add_root(layout)
#show(layout)
