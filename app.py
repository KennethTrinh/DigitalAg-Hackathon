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

emissions = pd.read_csv(path + "emissions_with_origin.csv")
productions = pd.read_csv(path + "productions.csv")
water = pd.read_csv(path + "water_use.csv")
global_emissions = pd.read_csv(path + "Global_Emissions.csv")

top10 = emissions.sort_values("Total_emissions")[-10:]
top10_vegetal = emissions[emissions.Origin=='Vegetal'].sort_values("Total_emissions")[-10:]
top8_animal = emissions[emissions.Origin=='Animal'].sort_values("Total_emissions")



radio_ani_veg = dbc.RadioItems(
        id='ani_veg', 
        className='radio',
        options=[dict(label='Animal', value=0), dict(label='Vegetal', value=1), dict(label='Total', value=2)],
        value=2, 
        inline=True
    )

dict_ = {'Apples':'Apples', 'Bananas':'Bananas', 'Barley':'Barley', 'Beet Sugar':'Sugar beet', 'Berries & Grapes':'Berries & Grapes', 'Brassicas':'Brassicas', 
        'Cane Sugar':'Sugar cane', 'Cassava':'Cassava', 'Citrus Fruit':'Citrus', 'Coffee':'Coffee beans', 'Groundnuts':'Groundnuts','Maize':'Maize', 'Nuts':'Nuts', 
        'Oatmeal':'Oats', 'Olive Oil':'Olives', 'Onions & Leeks':'Onions & Leeks','Palm Oil':'Oil palm fruit', 'Peas':'Peas', 'Potatoes':'Potatoes', 'Rapeseed Oil':'Rapeseed',
        'Rice':'Rice', 'Root Vegetables':'Roots and tubers', 'Soymilk':'Soybeans', 'Sunflower Oil':'Sunflower seed', 'Tofu':'Soybeans','Tomatoes':'Tomatoes', 
        'Wheat & Rye':'Wheat & Rye', 'Dark Chocolate':'Cocoa, beans', 'Milk': 'Milk', 'Eggs': 'Eggs','Poultry Meat': 'Poultry Meat', 'Pig Meat': 'Pig Meat', 
        'Seafood (farmed)': 'Seafood (farmed)', 'Cheese': 'Cheese', 'Lamb & Mutton': 'Lamb & Mutton', 'Beef (beef herd)': 'Beef (beef herd)'}

options_veg = [dict(label=key, value=dict_[key]) for key in top10_vegetal['Food product'].tolist()[::-1] if key in dict_.keys()]
options_an = [dict(label=val, value=val) for val in top8_animal["Food product"].tolist()[::-1]]
options_total = [dict(label=key, value=dict_[key]) for key in top10['Food product'].tolist()[::-1] if key in dict_.keys()]

bar_colors = ['#ebb36a','#6dbf9c']
bar_options = [top8_animal, top10_vegetal, top10]

drop_map = dcc.Dropdown(
        id = 'drop_map',
        clearable=False,
        searchable=False, 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
    )

drop_continent = dcc.Dropdown(
        id = 'drop_continent',
        clearable=False, 
        searchable=False, 
        options=[{'label': 'World', 'value': 'world'},
                {'label': 'Europe', 'value': 'europe'},
                {'label': 'Asia', 'value': 'asia'},
                {'label': 'Africa', 'value': 'africa'},
                {'label': 'North america', 'value': 'north america'},
                {'label': 'South america', 'value': 'south america'}],
        value='world', 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}
    )

slider_map = daq.Slider(
        id = 'slider_map',
        handleLabel={"showCurrentValue": True,"label": "Year"},
        marks = {str(i):str(i) for i in [1990,1995,2000,2005,2010,2015]},
        min = 1990,
        size=450, 
        color='#4B9072'
    )

fig_water = px.sunburst(water, path=['Origin', 'Category', 'Product'], values='Water Used', color='Category', 
                        color_discrete_sequence = px.colors.sequential.haline_r).update_traces(hovertemplate = '%{label}<br>' + 'Water Used: %{value} L')

fig_water = fig_water.update_layout({'margin' : dict(t=0, l=0, r=0, b=10),
                        'paper_bgcolor': '#F9F9F8',
                        'font_color':'#363535'
                    })

fig_gemissions = px.sunburst(global_emissions, path = ['Emissions', 'Group','Subgroup'], values = 'Percentage of food emissions', 
                    color = 'Group', color_discrete_sequence = px.colors.sequential.Peach_r).update_traces(hovertemplate = '%{label}<br>' + 'Global Emissions: %{value}%', textinfo = "label + percent entry") 

fig_gemissions = fig_gemissions.update_layout({'margin' : dict(t=0, l=0, r=0, b=10),
                        'paper_bgcolor': '#F9F9F8',
                        'font_color':'#363535'})

#------------------------------------------------------ APP ------------------------------------------------------ 

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([
        html.H1(children='FOOD FOOTPRINT'),
        html.Label('We are interested in investigating the food products that have the biggest impact on environment. Here you can understand which are the products whose productions emit more greenhouse gases and associate this with each supply chain step, their worldwide productions, and the water use.', 
                    style={'color':'rgb(33 36 35)'}), 
        html.Img(src=app.get_asset_url('supply_chain.png'), style={'position': 'relative', 'width': '180%', 'left': '-83px', 'top': '-20px'}),
    ], className='side_bar'),

    html.Div([
        html.Div([

            html.Div([
                dcc.Dropdown(
                    id='ml-regression-x-dropdown',
                    options=["Regression", "Decision Tree", "k-NN"],
                    value='Decision Tree',
                    clearable=False
                )
            ], className='box'),
            dcc.Graph(id="ml-regression-x-graph"),
        

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










if __name__ == '__main__':
    app.run_server(debug=True)
