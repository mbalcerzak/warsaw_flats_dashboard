# --- import libraries ---
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Output, Input
import urllib.request as request
import json
from collections import Counter


def get_json():
    link = "https://raw.githubusercontent.com/mbalcerzak/warsaw_flats_api/main/json_dir/flats.json"

    with request.urlopen(link) as url:
        data = json.loads(url.read().decode())

    return data


def get_data():
    return pd.read_csv("dataset.csv")


def get_options():
    data = get_json()

    options = []
    for key in data["flats_per_location"].keys():
        options.append({'label': key, 'value': key})

    return options[1:]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# --- initialize the app ---
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# --- layout the dashboard ---
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('Analysis of Warsaw Flat Prices in 2021',
                    style={'textAlign': 'center',
                           'color': '#FFFFFF',
                           'fontSize': '36px',
                           'padding-top': '0px'},
                    ),

            html.P('By MAB', style={'textAlign': 'center',
                                    'color': '#FFFFFF',
                                    'fontSize': '24px'},
                   ),
            html.P('''An interactive dashboard displaying housing prices in the districts of Warsaw ''',
                   style={'textAlign': 'center',
                          'color': '#FFFFFF',
                          'fontSize': '16px'},
                   ),
        ],
            style={'backgroundColor': '#1f3b4d',
                   'height': '200px',
                   'display': 'flex',
                   'flexDirection': 'column',
                   'justifyContent': 'center'},
        ),
        html.Div([
            html.Div([
                html.Label('Select a city to see home price data'),
                dcc.Dropdown(
                    id='city-dropdown',
                    options=get_options(),
                    value='Bielany, Warszawa',
                    multi=False,
                    clearable=True,
                    searchable=True,
                    placeholder='Choose a City...',
                ),
            ],
                style={'width': '25%',
                       'display': 'inline-block',
                       'padding-left': '150px',
                       'padding-top': '20px'}
            ),
            # html.Div(
            #     dcc.Graph(id='all-districts',
            #               style={'padding': '25px'}),
            # ),
            # pie charts two in a row
            html.Div([
                html.Div([
                    html.H3('Number of flats / district'),
                    dcc.Graph(id='pie_flats_per_location',
                              style={'padding': '25px'}),
                ], className="six columns"),
                html.Div([
                    html.H3('Size of flats'),
                    dcc.Graph(id='pie_flats_per_area_cat',
                              style={'padding': '25px'}),
                ], className="six columns"),
            ], className="row"),
            # end of pie charts row
            html.Div(
                dcc.Graph(id='scraped-per-day',
                          style={'padding': '25px'}),
            ),
        ]),
        html.Div([
            html.Label('References:',
                       style={'padding': '10px'}
                       ),
            html.Label('[1] Zillow, 2021, Zillow Home Value Index Data (ZHVI), All Homes, Time Series, Raw Mid Tier:',
                       style={'padding-left': '25px'}),
            html.A('https://www.zillow.com/research/data/',
                   style={'padding-left': '25px'}),
        ],
        ),
    ],
    ),
],
)


@app.callback(
    Output('all-districts', 'figure'),
    Input('city-dropdown', 'value'))
def update_figure(selected_city):
    data = get_json()
    dff = data["scraped_per_day"]

    dff = pd.DataFrame(dff.items(), columns=['Date', 'Value'])
    dff = dff.sort_values(by=['Date'])

    fig = px.scatter(dff,
                     x='Median Home Price ($USD, January 2021)',
                     y='Median Household Income ($USD)',
                     size='Population',
                     size_max=25,
                     color='Median Home Price ($USD, January 2021)',
                     color_continuous_scale='jet',
                     hover_name='City',
                     hover_data={'Latitude': False, 'Longitude': False,
                                 'Population': ':,2f', 'Median Household Income ($USD)': ':$,2f',
                                 'Median Home Price ($USD, January 2021)': ':$,2f'})

    fig.update_layout(title_text='Median Household Income vs. Median Home Price ($USD) in the United States',
                      title_font_size=24,
                      title_xref='container',
                      title_y=0.95,
                      title_x=0.5,
                      showlegend=False,
                      hovermode='closest',
                      template='xgridoff')

    return fig


# --- dropdown callback ---
@app.callback(
    Output('scraped-per-day', 'figure'),
    Input('city-dropdown', 'value'))
def update_figure(selected_city):
    data = get_json()
    dff = data["scraped_per_day"]
    date_first = data["date_first"]
    date_last = data["date_last"]

    dff = pd.DataFrame(dff.items(), columns=['Date', 'Value'])
    dff = dff.sort_values(by=['Date'])

    fig = px.line(dff, x='Date', y='Value')

    fig.update_layout(template='xgridoff',
                      yaxis={'title': 'Number of ads scraped'},
                      xaxis={'title': 'Date'},
                      title={'text': f'Ads scraped between {date_first} and {date_last}',
                             'font': {'size': 24}, 'x': 0.5, 'xanchor': 'center'}
                      )

    return fig


@app.callback(
    Output('pie_flats_per_location', 'figure'),
    Input('city-dropdown', 'value'))
def update_figure(selected_city):
    data = get_json()
    dff = data["flats_per_location"]
    dff = pd.DataFrame(dff.items(), columns=['Location', 'Value'])

    fig = px.pie(dff, values='Value', names='Location')

    return fig


@app.callback(
    Output('pie_flats_per_area_cat', 'figure'),
    Input('city-dropdown', 'value'))
def update_figure(selected_city):
    data = get_json()
    dff = data["flats_per_area_cat"]
    dff = pd.DataFrame(dff.items(), columns=['Area', 'Value'])

    fig = px.pie(dff, values='Value', names='Area')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)