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


n_points = 12 # one year of monthly data
x = pd.date_range('2022-01-01', periods=n_points, freq='M')
y = np.cumsum(np.random.randn(n_points)*10)
df = pd.DataFrame({'Date': x, 'Value': y})

layout = go.Layout(
    title='Methane Emissions Comparison for Dairy Companies',
    xaxis=dict(title='Month'),
    yaxis=dict(title='Methane Emissions (tonnes)')
)

# # Define the initial data for the chart
# initial_data = [
#     go.Bar(x=list(range(1, 13)), y=dairy_data['Dairy Farmers of America'], name='Dairy Farmers of America')
# ]
# fig_compare = go.Figure(data=initial_data, layout=layout)

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

        html.Div(id='dairy-company-output', className='box'),

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




@app.callback(
    Output('dairy-company-output', 'children'),
    Input('dairy-company-dropdown', 'value')
)
def update_output(selected_company):
    if selected_company == 'None selected':
        return html.Div()
    selected_data = dairy_data[selected_company]
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
    bar = go.Figure(data=data, layout=layout)
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
        
    return html.Div([
        dcc.Graph(id='dairy-emissions-chart', figure=bar),
        dcc.Graph(
            id='month-by-month-line-chart',
            figure=px.line(df, x='Date', y='Value', title='Month by Month Line Chart')
        ),
        dcc.Graph(
            id='gauge-chart',
            figure=gauge_chart
        )
    ])






if __name__ == '__main__':
    app.run_server(debug=True)
