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


path = 'https://raw.githubusercontent.com/KennethTrinh/DigitalAg-Hackathon/master/data/'




#------------------------------------------------------ APP ------------------------------------------------------ 

app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div([
        html.H1(children='Methane Emissions'),
        html.Label('Tool for analyzing methane emissions from dairy farms', 
                    style={'color':'rgb(33 36 35)'}), 
        html.Img(src=app.get_asset_url('supply_chain.png'), style={'position': 'relative', 'width': '180%', 'left': '-83px', 'top': '-20px'}),
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
                dcc.Upload(
                    id='upload-data-1',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files'), 
                        " for training"
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
                html.Div(id='output-data-1-upload'),
                dcc.Upload(
                    id='upload-data-2',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files'),
                        " for prediction"
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
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

        ## ML Algorithm Dropdown
        html.Div([
            dcc.Dropdown(
                id='ml-regression-x-dropdown',
                options=["Regression", "Decision Tree", "k-NN"],
                value='Decision Tree',
                clearable=False
            ),
            dcc.Graph(id="ml-regression-x-graph")
        ], className='box'),

        

    ], className='main'),
    
])


#------------------------------------------------------ Callbacks ------------------------------------------------------

models = {'Regression': linear_model.LinearRegression,
          'Decision Tree': tree.DecisionTreeRegressor,
          'k-NN': neighbors.KNeighborsRegressor}
@app.callback(
    Output("ml-regression-x-graph", "figure"), 
    Input('ml-regression-x-dropdown', "value"))
def train_and_display(name):
    df = px.data.tips() # replace with your own data source
    X = df.total_bill.values[:, None]
    X_train, X_test, y_train, y_test = train_test_split(
        X, df.tip, random_state=42)

    model = models[name]()
    model.fit(X_train, y_train)

    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    fig = go.Figure([
        go.Scatter(x=X_train.squeeze(), y=y_train, 
                   name='train', mode='markers'),
        go.Scatter(x=X_test.squeeze(), y=y_test, 
                   name='test', mode='markers'),
        go.Scatter(x=x_range, y=y_range, 
                   name='prediction')
    ])
    return fig


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
            [html.Div("Preview")] +

            # Body
            [html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns[:10]
            ]) for i in range(min(len(df), 3))]
        )
    ])

@app.callback(Output('output-data-1-upload', 'children'),
              Input('upload-data-1', 'contents'),
              State('upload-data-1', 'filename'))
def update_output(contents, filename):
    if contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(contents, filename)]
        return children

@app.callback(Output('output-data-2-upload', 'children'),
              Input('upload-data-2', 'contents'),
              State('upload-data-2', 'filename'))
def update_output(contents, filename):
    if contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(contents, filename)]
        return children

@app.callback(
    Output('output-container', 'children'),
    Input('submit-button', 'n_clicks'),
    State('upload-data-1', 'contents'),
    State('upload-data-1', 'filename')
)
def update_output(n_clicks, list_of_contents, list_of_names):
    if n_clicks > 0:
        val = methane_lin_reg()
        return f'The predicted grams of produced methane:  {val}.'
    
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children


def methane_lin_reg():
    df1 = pd.read_csv('prediction_cow.csv')
    X_new = df1.iloc[:, :].values
    X_new = X_new.reshape(1, -1)


    df = pd.read_csv('output_200cows.csv')
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    reg = linear_model.LinearRegression()
    reg.fit(X, y)
    # X_new = [[...]]  # input data for a new cow, with 17 features
    return float(reg.predict(X_new)[0])




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

def getGeneBar():
    genes = ['Gene A', 'Gene B', 'Gene C', 'Gene D', 'Gene E']
    methane_production = [2.5, 3.2, 1.8, 2.1, 2.9]
    fig = go.Figure([go.Bar(x=genes, y=methane_production)])
    fig.update_layout(title='Contribution of Genes to Methane Production in Cows', xaxis_title='Gene', yaxis_title='Methane Production (kg CO2e/day)')
    return fig

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
    bar = getGeneBar()
    return html.Div([
        dcc.Graph(id='farm-pie-chart', figure=pie),
        dcc.Graph(id='farm-emissions-boxplot', figure=box),
        dcc.Graph(id='gene-bar-chart', figure=bar)
    ], className='box')





if __name__ == '__main__':
    app.run_server(debug=True)