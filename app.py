# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

COLORS = [
	"#ffe3bd","#99613f","#82b0d0","#c9182a",
	"#FB9F99","#cad3f7","#f6a604","#036987",
	"#165254","#85a189","#ffc383","#d58399",
	"#ee7f7a","#7999af","#d2449a","#f07d60"
	]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
	html.Div(id="test"),
	html.H1(
		"Colors and Shapes",
		style={
			"textAlign":"center"
		}
	),
	dcc.Graph(id="random-shapes"),
	html.Div([
		html.Button(
			"Circles", id="circle", n_clicks=0,
			style={
				"margin-right":"265px"
			}
		),
		html.Button(
			"Rectangles", id="rect", n_clicks=0
		)
	], style={"textAlign":"center"}),
	html.Br(),
	html.H3("Size", style={"textAlign":"center"}),
	dcc.Slider(
		id="size-slider",
		min=1,
		max=5,
		value=3,
		marks={str(val): str(val) for val in range(1,6)}
	),
	html.Br(),
	html.H3("Number", style={"textAlign":"center"}),
	dcc.Slider(
		id="num-shapes",
		min=1,
		max=30,
		value=6,
		marks={str(val): str(val) for val in range(1,31,3)}
	),
	html.Br(),
	html.Div(id="curr-shape", style={"display":"none"})
], style={"margin":"auto","width":"30%"})


@app.callback(
	Output("curr-shape","children"),
	[Input("circle","n_clicks"),
	Input("rect","n_clicks")]
)
def update_curr_shape(n_circle, n_rect):
	shape = [p['prop_id'].split('.')[0] for p in dash.callback_context.triggered][0]
	return shape


@app.callback(
	Output("random-shapes","figure"),
	[Input("circle","n_clicks"),
	Input("rect","n_clicks"),
	Input("size-slider","value"),
	Input("num-shapes","value"),
	Input("curr-shape","children")]
)
def randomize_shapes(n_circle, n_rect, min_size, num_shapes, curr_shape):
	# the y1 ensures that circle shapes
	# use the same value for height and 
	# width so they aren't ellipses. If
	# ellipses are desired, then just use
	# options = {
	# 	'shape': shape,
	# 	'y1': 1
	# }
	options = {
		'shape': curr_shape,
		'y1': 1
	}

	if curr_shape == 'circle':
		options = {
			'shape': 'circle',
			'y1': 0
		}

	fig = go.Figure()

	fig.update_layout(height=600, width=600) #, plot_bgcolor="White")
	# axes
	fig.update_xaxes(range=[0,10], visible=False)
	fig.update_yaxes(range=[0,10], visible=False)

	# can't use floating point numbers in slider
	min_size /= 10

	true_num = min(num_shapes, len(COLORS))
	choices = np.random.permutation(COLORS)[:true_num]
	# choices = np.random.choice(COLORS, num_shapes)
	for c in choices:
		origin = np.random.choice(np.linspace(0,.8,20), 2)

		min_ = min_size; max_ = min_size + 0.3
		size = np.random.choice(np.linspace(min_,max_,20), 2)

		fig.add_shape(type=options['shape'],
			xref="paper", yref="paper",
			x0=origin[0], y0=origin[1],
			x1=(origin[0]+size[0]), y1=(origin[1]+size[options['y1']]),
			line_color=c,
			fillcolor=c
		)

	return fig

if __name__ == "__main__":
	app.run_server(debug=True)



