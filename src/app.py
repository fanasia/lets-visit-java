# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from tkinter.ttk import Style
from turtle import width
from dash import Dash, html, dcc, Input, Output, State, callback
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# styling
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)

mapbox_access_token = 'pk.eyJ1IjoiZmFuYXNpYSIsImEiOiJjbDJwcHc5NXQxdGVuM2Nwa2dienZ1bWQwIn0.axUG1Bsn2DIoPmTYDt8lgQ'

# read data
data = pd.read_csv("ready_data.csv")
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

ratingMinValue = data['Rating'].min()
ratingMaxValue = data['Rating'].max()

priceMinValue = data['Price'].min()
priceMaxValue = data['Price'].max()

# lat long
city_coordinates = {
    'Jakarta' : [-6.2000, 106.8166],
    'Yogyakarta' : [-7.7970, 110.3705],
    'Bandung' : [-6.9147, 107.6098],
    'Semarang' : [-6.9666, 110.4166],
    'Surabaya' : [-7.2504, 112.7688],
    'Java' : [-7.6145, 110.4244]
}

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# index page
layout_index = dbc.Container(
    [
        # title
        dbc.Row(
            dbc.Col(
                html.H1("Where to go in Java, Indonesia? ✈️🇮🇩"),
                width={"size": 6, "offset": 3},
            )
        ),
        html.Br(),

        # description
        dbc.Row(
            dbc.Col(
                html.Div("Java, also spelled Djawa or Jawa, island of Indonesia lying southeast of Malaysia and Sumatra, south of Borneo (Kalimantan), and west of Bali. Java is home to roughly half of Indonesia’s population and dominates the country politically and economically. The capital of Java and of the country is Jakarta (formerly Batavia), which is also Indonesia’s largest city. Java has many tourist places ranging from breathtaking nature to spectacular cityscape"),
                width={"size": 6, "offset": 3},
            )
        ),
        html.Br(),

        # slider of images
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Carousel(
                    items=[
                        {"key": "1", "src": "/assets/jakarta.png"},
                        {"key": "2", "src": "/assets/bandung.png"},
                        {"key": "3", "src": "/assets/yogyakarta.png"},
                        {"key": "4", "src": "/assets/semarang.png"},
                        {"key": "6", "src": "/assets/surabaya.png"}
                    ],
                    controls=False,
                    indicators=True,
                    interval=2000,
                    ride="carousel"
                )
            )
        ),

        # button
        html.Br(),
        dbc.Row(
            dbc.Col(
                dcc.Link(dbc.Button("Find out now!", size="lg", color="primary"), href='/page-1'),
                width={"size": 6, "offset": 5},
            )
        )
    ], 
style={"margin-top": "100px", "margin-bottom": "100px"})

# page 1
category_checklist_1 = dbc.Container(
    [
        dbc.Label("Category"),
        dbc.Checklist(
            options=[
                {'label': 'Culture', 'value': 'Budaya'},
                {'label': 'Amusement Parks', 'value': 'Taman Hiburan'},
                {'label': 'Nature', 'value': 'Cagar Alam'},
                {'label': 'Nautical', 'value': 'Bahari'},
                {'label': 'Shopping Center', 'value': 'Pusat Perbelanjaan'},
                {'label': 'Worship Place', 'value': 'Tempat Ibadah'}
            ],
            value=['Budaya','Taman Hiburan','Cagar Alam','Bahari','Pusat Perbelanjaan','Tempat Ibadah'],
            id='category_checkbox_1',
            inline=True
        )
    ]
)

rating_slider_1 = html.Div(
    [
        dbc.Label("Rating"),
        dcc.RangeSlider(
            id='rating_slider_1',
            min=3,
            max=5,
            value=[ratingMinValue, ratingMaxValue],
            marks= {i: str(i) for i in range(3, 5, 1)},
            allowCross=False
        )
    ]
)

price_slider_1 = html.Div(
    [
        dbc.Label("Price"),
        dcc.RangeSlider(
            id='price_slider_1',
            min=priceMinValue,
            max=priceMaxValue,
            value=[priceMinValue, priceMaxValue],
            marks= {i: str(i) for i in range(priceMinValue, priceMaxValue, 100000)},
            allowCross=False
        )
    ]
)

filter_1 = html.Div(
    [
        dbc.Row(dbc.Col(category_checklist_1)),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(rating_slider_1),
                dbc.Col(price_slider_1)
            ]
        ),
    ]
)

layout_page_1 = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dcc.Link(dbc.Button("Back to home", outline="True", size="sm", color="primary"), href='/'),
            )
        ),

        # title
        dbc.Row(
            dbc.Col(
                html.H1("Know the cities! 🏙️"),
                width={"size": 6, "offset": 4},
            )
        ),
        html.Br(),

        # filter
        filter_1,

        # graph
        dcc.Graph(
            id='bar_chart_num_of_attractions_per_city'
        ),

        # options
        dbc.Row(
            dbc.Col(
                html.H5("Already know which city you want to go? Choose below")
            )
        ),

        dbc.Row(
            dbc.Col(
                dcc.Dropdown(['Jakarta', 'Yogyakarta', 'Bandung', 'Semarang', 'Surabaya'], '', id='demo-dropdown')
            )
        ),

        # next button
        dbc.Row(
            dbc.Col(
                dcc.Link(dbc.Button("Let's plan!", size="md", color="primary"), href='/page-2', id='nav_link')
            ),
            style={"margin-top": "10px"}
        )
    ],
style={"margin-top": "50px"})

# page 2
layout_page_2 = dbc.Container(
    [
        dcc.Input(id='input_city', value='', type='hidden'),

        # title and filter
        html.Div(id='filter', style={'padding': 10, 'flex': 1}),
        dcc.Graph(
            id='map_attraction'
        ),

        # next button
        dbc.Row(
            dbc.Col(
                dcc.Link(dbc.Button("Back to previous page", outline="True", size="md", color="primary"), href='/page-1'),
            ),
            style={"margin-top": "10px"}
        )
    ],
style={"margin-top": "30px", "margin-bottom": "30px"})

# index layout
app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    layout_index,
    layout_page_1,
    layout_page_2
])

# Index callbacks
@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/page-1":
        return layout_page_1
    elif pathname.startswith("/page-2"):
        return layout_page_2
    else:
        return layout_index

# Page 1 callbacks
@app.callback(
    Output('bar_chart_num_of_attractions_per_city','figure'),
    Input('category_checkbox_1', 'value'),
    Input('rating_slider_1', 'value'),
    Input('price_slider_1', 'value')
)
def update_graph(category_values, rating_values, price_values):
    # filter
    dff = data[data['Category'].isin(category_values)]
    dff = dff[dff['Rating'].between(rating_values[0], rating_values[1], 'both')]
    dff = dff[dff['Price'].between(price_values[0], price_values[1], 'both')]

    # bar chart
    dfg = dff.groupby('City').count().reset_index()

    fig = px.bar(dfg,
             x='City',
             y='Place_Id',
             title='Number of Tourist Attractions in a City',
             barmode='stack')

    # how to make the scale stay? update_layout?

    return fig

@callback(
    Output('nav_link', 'href'),
    Input('demo-dropdown','value'))
def update_nav_link(dropdown_value):
    return '/page-2/' + dropdown_value

# Page 2 callbacks
@callback(
    Output('input_city', 'value'),
    Input('url', 'pathname'))
def select_city(pathname_value):
    city = pathname_value.split('/page-2/')
    if len(city) > 1 and len(city[1]) > 0:
        return city[1]

    return ''

@callback(
    Output('filter', 'children'),
    Input('input_city', 'value'))
def update_filter(city_value):
    if city_value:
        dff = data[data['City'] == city_value]
    else:
        dff = data

    ratingMinValue = dff['Rating'].min()
    ratingMaxValue = dff['Rating'].max()

    priceMinValue = dff['Price'].min()
    priceMaxValue = dff['Price'].max()

    timeSpentMinValue = dff['Time_Minutes'].min()
    timeSpentMaxValue = dff['Time_Minutes'].max()

    timeSpentMinValue_int = int(timeSpentMinValue)
    timeSpentMaxValue_int = int(timeSpentMaxValue)

    category_checklist_2 = dbc.Container(
        [
            dbc.Label("Category"),
            dbc.Checklist(
                options=[
                    {'label': 'Culture', 'value': 'Budaya'},
                    {'label': 'Amusement Parks', 'value': 'Taman Hiburan'},
                    {'label': 'Nature', 'value': 'Cagar Alam'},
                    {'label': 'Nautical', 'value': 'Bahari'},
                    {'label': 'Shopping Center', 'value': 'Pusat Perbelanjaan'},
                    {'label': 'Worship Place', 'value': 'Tempat Ibadah'}
                ],
                value=['Budaya','Taman Hiburan','Cagar Alam','Bahari','Pusat Perbelanjaan','Tempat Ibadah'],
                id='category_checkbox_2',
                inline=True
            )
        ]
    )

    rating_slider_2 = dbc.Container(
        [
            dbc.Label("Rating"),
            dcc.RangeSlider(
                id='rating_slider_2',
                min=3,
                max=5,
                value=[ratingMinValue, ratingMaxValue],
                marks= {i: str(i) for i in range(3, 5, 1)},
                allowCross=False
            )
        ]
    )

    price_slider_2 = dbc.Container(
        [
            dbc.Label("Price"),
            dcc.RangeSlider(
                id='price_slider_2',
                min=priceMinValue,
                max=priceMaxValue,
                value=[priceMinValue, priceMaxValue],
                marks= {i: str(i) for i in range(priceMinValue, priceMaxValue, 100000)},
                allowCross=False
            )
        ]
    )

    time_slider_2 = dbc.Container(
        [
            dbc.Label("Time Spent (minutes)"),
            dcc.RangeSlider(
                id='time_spent_slider_2',
                min=timeSpentMinValue,
                max=timeSpentMaxValue,
                value=[timeSpentMinValue, timeSpentMaxValue],
                marks= {i: str(i) for i in range(timeSpentMinValue_int, timeSpentMaxValue_int, 50)},
                allowCross=False
            )
        ]
    )

    text_title = "Now let's plan the trip to {}! 🧳".format(city_value)

    div = [
        dcc.Input(id='update_map', value=city_value, type='hidden'),
        dbc.Row(
            dbc.Col(
                html.H1(text_title),
                width={"size": 6, "offset": 3},
            )
        ),

        html.Br(),
        dbc.Row(dbc.Col(category_checklist_2)),

        html.Br(),
        dbc.Row(
            [
                dbc.Col(rating_slider_2),
                dbc.Col(price_slider_2)
            ]
        ),

        html.Br(),
        dbc.Row(dbc.Col(time_slider_2))
    ]

    return div

@app.callback(
    Output('map_attraction','figure'),
    Input('update_map', 'value'),
    Input('category_checkbox_2', 'value'),
    Input('rating_slider_2', 'value'),
    Input('price_slider_2', 'value'),
    Input('time_spent_slider_2', 'value')
)
def update_graph(update_map, category_values, rating_values, price_values, time_spent_values):
    selected_city = ''
    zoom = 0

    # main filter
    if update_map:
        dff = data[data['City'] == update_map]
        selected_city = update_map
        zoom = 10
    else:
        dff = data
        selected_city = 'Java'
        zoom = 7

    # additional filter
    dff = dff[dff['Category'].isin(category_values)]
    dff = dff[dff['Rating'].between(rating_values[0], rating_values[1], 'both')]
    dff = dff[dff['Price'].between(price_values[0], price_values[1], 'both')]
    dff = dff[dff['Time_Minutes'].between(time_spent_values[0], time_spent_values[1], 'both')]

    # maps chart
    fig = go.Figure(go.Scattermapbox(
        lat=dff['Lat'],
        lon=dff['Long'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=dff['Label'],
    ))

    # zoom maps based on city chosen only
    coordinates = city_coordinates.get(selected_city)
    
    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=coordinates[0],
                lon=coordinates[1]
            ),  
            pitch=0,
            zoom=zoom
        ),
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)