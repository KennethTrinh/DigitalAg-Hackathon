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


path = 'https://raw.githubusercontent.com/KennethTrinh/DigitalAg-Hackathon/master/data/'


n_points = 12 # one year of monthly data
x = pd.date_range('2022-01-01', periods=n_points, freq='M')
y = np.cumsum(np.random.randn(n_points)*10)
df = pd.DataFrame({'Date': x, 'Value': y})


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
            ## Dropdown
            html.Div([
                dcc.Dropdown(
                    id='ml-regression-x-dropdown',
                    options=["Regression", "Decision Tree", "k-NN"],
                    value='Decision Tree',
                    clearable=False
                ),
                dcc.Graph(id="ml-regression-x-graph")
            ], className='box'),

            ## Line Chart
            html.Div([
                dcc.Graph(
                    id='month-by-month-line-chart',
                    figure=px.line(df, x='Date', y='Value', title='Month by Month Line Chart')
                )
            ], className='box'),

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

        ], className='main'),
    ]),
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









if __name__ == '__main__':
    app.run_server(debug=True)