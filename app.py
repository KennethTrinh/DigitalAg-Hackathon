import base64
import io
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from sklearn.model_selection import train_test_split
from sklearn import linear_model, tree, neighbors
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from consts import *
import regression


path = 'https://raw.githubusercontent.com/KennethTrinh/DigitalAg-Hackathon/master/data/'




#------------------------------------------------------ APP ------------------------------------------------------ 

app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div([
        html.H1(children='Methane Emissions'),
        html.Label('Tool for analyzing methane emissions from dairy farms', 
                    style={'color':'rgb(33 36 35)'}), 
        html.Img(src=app.get_asset_url('supply_chain.png'), style={'position': 'relative', 'width': '80%', 'left': '0px', 'top': '10px'}),
    ], className='side_bar'),

    
    html.Div([
        
        html.Div([
            html.H2(children='Dairy Companies'),
            dcc.Dropdown(
                id='dairy-company-dropdown',
                options=DAIRY_COMPANY_OPTIONS,
                value='None selected',
                clearable=False
            ),
        ], className='box'),

        html.Div(id='dairy-company-output'),

        html.Div([
            html.H2(children='Farms'),
            dcc.Dropdown(
                id='farm-company-dropdown',
                options=FARM_OPTIONS,
                value='None selected',
                clearable=False
            ),
        ], className='box'),

        html.Div(id='farm-company-output'),

        html.Div([
                dcc.Upload(
                    id='upload-data-2',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files'),
                        " for prediction"
                    ]),
                    style=RACHELS_STYLE,
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
                html.Div(id='output-data-2-upload'),
                html.Button(
                    id='submit-button',
                    n_clicks=0,
                    children='Submit'
                ),
                html.Div(id='output-container')
        ], className='box'),


        

    ], className='main'),
    
])


#------------------------------------------------------ Callbacks ------------------------------------------------------



def getCompanyBar():
    data = []
    for company, emissions in dairy_data.items():
        trace = go.Bar(
            x=list(range(1, 13)),
            y=emissions,
            name=company
        )
        data.append(trace)

    layout = go.Layout(
        title='Comparison of Methane Emissions for Dairy Companies',
        xaxis=dict(title='Month'),
        yaxis=dict(title='Methane Emissions (tonnes)'),
        barmode='group' # or 'stack'
    )
    return go.Figure(data=data, layout=layout)

def getLine():
    n_points = 12 # one year of monthly data
    x = pd.date_range('2022-01-01', periods=n_points, freq='M')
    y = np.cumsum(np.random.randint(0, 50, n_points))
    df = pd.DataFrame({'Month': x, 'Methane Emissions': y})
    layout = go.Layout(
        title='Methane Emissions Comparison for Dairy Companies',
        xaxis=dict(title='Month'),
        yaxis=dict(title='Methane Emissions (tonnes)')
    )
    return px.line(df, x='Month', y='Methane Emissions', title='Monthly Methane Emissions')
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume the user uploaded a CSV file
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    return html.Div([
        html.H5(f'File name: {filename}'),
        html.Table(
            # Header
            [html.Div("Preview of cow features")] +

            # Body
            [html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), 3))]
        )
    ])


@app.callback(Output('output-data-2-upload', 'children'),
              Input('upload-data-2', 'contents'),
              State('upload-data-2', 'filename'))
def update_output(contents, filename):
    if contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(contents, filename)]
        return children

def create_recommendation_list():
    df1 = pd.read_csv('output_200cows.csv')
    cow = df1.iloc[1].to_numpy()[0:17]
    archaea_props=cow[0:4]
    bacteria_props=cow[4:17]
    recs = regression.generate_recommendations(archaea_props, bacteria_props)
    return html.Ul(id='recs', children=[html.Li(i) for i in recs])

@app.callback(
    Output('output-container', 'children'),
    Input('submit-button', 'n_clicks'),
    State('upload-data-2', 'contents'),
    State('upload-data-2', 'filename')
)
def update_output(n_clicks, list_of_contents, list_of_names):
    if n_clicks > 0:
        if list_of_contents is not None:
            c1 = float(429.33333)
            c2 = float(415.6483)
            return html.Div([html.H2("Cow 1: 429.333"), html.H2("Cow 1: 379.333"), html.H5('Recommendations:'),
                         create_recommendation_list()])
        

    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children




def getGauge():
    gauge_val = np.random.uniform(0, 100)
    gauge_chart = go.Figure(
        go.Indicator(
            mode = "gauge+number",
            value = gauge_val,
            domain=dict(x=[0, 1], y=[0, 1]),
            gauge = dict(
                axis=dict(range=[0, 100]),
                bar=dict(color="black"),
                steps=[
                    dict(range=[0, 50], color="green"),
                    dict(range=[50, 80], color="yellow"),
                    dict(range=[80, 100], color="red")
                ]
            )
        )
    )
    gauge_chart.update_layout(
        title=dict(
            text=f"Environmental Regulations Compliance Risk: {gauge_val:.2f}%",
            x=0.5,
            y=0.9,
            font=dict(size=24)
        ),
        margin=dict(l=20, r=20, t=80, b=20)
    )
    return gauge_chart

@app.callback(
    Output('dairy-company-output', 'children'),
    Input('dairy-company-dropdown', 'value')
)
def update_dairy_company(selected_company):
    if selected_company == 'None selected':
        return html.Div()
    selected_data = dairy_data[selected_company]

    bar = getCompanyBar()
    line = getLine()
    gauge_chart = getGauge()
        
    return html.Div([
        dcc.Graph(id='dairy-emissions-chart', figure=bar),
        dcc.Graph(
            id='month-by-month-line-chart',
            figure=line
        ),
        dcc.Graph(
            id='gauge-chart',
            figure=gauge_chart
        )
    ], className='box')

def getPie(selected_data, selected_farm):
    return px.pie(
        values=list(selected_data.values()),
        names=list(selected_data.keys()),
        title=f"Microbial Composition for {selected_farm}",
        hole=0.5
    )

def getBox(farm_emissions, selected_farm):
    box_data = [
        go.Box(
            y=farm_emissions,
            name=selected_farm,
            boxpoints='outliers',
            jitter=0.3,
            pointpos=-1.8
        ),
        go.Box(
            y=benchmark_data,
            name='Average Benchmark Farm',
            boxpoints='outliers',
            jitter=0.3,
            pointpos=-1.8
        )
    ]
    box_layout = go.Layout(
        title='Methane Emissions for {} vs. Average Benchmark Farm'.format(selected_farm),
        yaxis=dict(title='Methane Emissions (tonnes)')
    )
    return go.Figure(data=box_data, layout=box_layout)

@app.callback(
    Output('farm-company-output', 'children'),
    Input('farm-company-dropdown', 'value')
)
def update_farm_company(selected_farm):
    if selected_farm == 'None selected':
        return html.Div()
    selected_data = farm_data[selected_farm]
    pie = getPie(selected_data, selected_farm)

    farm_emissions = box_plot_farm_data[ selected_farm]
    box = getBox(farm_emissions, selected_farm)
    return html.Div([
        dcc.Graph(id='farm-pie-chart', figure=pie),
        dcc.Graph(id='farm-emissions-boxplot', figure=box),
        html.Div([
            html.H2(children='Recommendations'),
            html.Label('Based on the data you have provided, we recommend the following:'),
            #bullet list
            html.Ul([
                html.Li('Increase Starch'),
                html.Li('Add seaweed, Decrease NDF'),
                html.Li('Add Tannins, Remove 3-NOP'),
            ])

        ])
    ], className='box')





if __name__ == '__main__':
    app.run_server(debug=True)