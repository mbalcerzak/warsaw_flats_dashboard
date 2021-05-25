import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Output, Input
import urllib.request as request
import json


def get_json():
    link = "https://raw.githubusercontent.com/mbalcerzak/warsaw_flats_api/main/json_dir/flats.json"
    with request.urlopen(link) as url:
        data = json.loads(url.read().decode())

    return data


def get_data():
    return pd.read_csv("dataset.csv")


def get_list(label: str) -> dict:
    data = get_json()
    sorted_list = sorted(data[label].keys())
    options = []
    for key in sorted_list:
        options.append({'label': key, 'value': key})

    return options


districts = get_list("flats_per_location")
flat_sizes = get_list("flats_per_area_cat")


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
            html.H1('Overall statistics',
                    style={'textAlign': 'center',
                           'color': '#1f3b4d',
                           'fontSize': '30px',
                           'padding-top': '15px'},
                    ),
            # pie charts two in a row
            html.Div([
                html.Div([
                    html.H4('Number of flats / district', style={'textAlign': 'center'}),
                    dcc.Graph(id='pie_flats_per_location',
                              style={'padding': '25px'}),
                ], className="six columns"),
                html.Div([
                    html.H4('Size of flats', style={'textAlign': 'center'}),
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
            html.H1('Select a district and area to see average prices per square metre for each month',
                    style={'textAlign': 'center',
                           'color': '#1f3b4d',
                           'fontSize': '30px',
                           'padding-top': '15px'},
                    ),
            html.Div([
                html.Label('Select a district'),
                dcc.Dropdown(
                    id='district-dropdown',
                    options=districts,
                    value='Mokotów, Warszawa',
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
            html.Div([
                html.Label('Select a flat size'),
                dcc.Dropdown(
                    id='area-dropdown',
                    options=flat_sizes,
                    value='40_50',
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
            html.Div(
                dcc.Graph(id='district-area-price',
                          style={'padding': '25px'}),
            ),
        ]),
        html.Div([
            html.Label('Useful links:',
                       style={'padding': '10px'}
                       ),
            html.Label(' - JSON data',
                       style={'padding-left': '25px'}),
            html.A('https://raw.githubusercontent.com/mbalcerzak/warsaw_flats_api/main/json_dir/flats.json',
                   style={'padding-left': '25px'}),
            html.Label('- code for this thing',
                       style={'padding-left': '25px'}),
            html.A('https://github.com/mbalcerzak/warsaw_flats_dashboard',
                   style={'padding-left': '25px'}),
        ],
        ),
    ],
    ),
],
)


@app.callback(
    Output('district-area-price', 'figure'),
    [Input('district-dropdown', "value"),
     Input('area-dropdown', "value")])
def update_figure(location, area):
    data = get_json()
    dff = data["price_m_loc_area_cat"]
    dff = pd.DataFrame.from_dict(dff)

    dff = dff.sort_values(by=['month'])
    dff = dff[dff['location'] == location]
    dff = dff[dff['area_category'] == area]
    num_flats = sum(dff['num_flats'])

    fig = px.line(dff, x='month', y='avg_price_per_m')

    fig.update_layout(template='xgridoff',
                      yaxis={'title': 'Price per m2'},
                      xaxis={'title': 'Month'},
                      title={'text': f'Prices in {location} for flats of size {area} ({num_flats} flats)',
                             'font': {'size': 24}, 'x': 0.5, 'xanchor': 'center'},
                      )
    fig.update_traces(mode="markers+lines")

    return fig


# --- dropdown callback ---
@app.callback(
    Output('scraped-per-day', 'figure'),
    Input('area-dropdown', 'value'))
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
    Input('area-dropdown', 'value'))
def update_figure(selected_city):
    data = get_json()
    dff = data["flats_per_location"]
    dff = pd.DataFrame(dff.items(), columns=['Location', 'Value'])

    fig = px.pie(dff, values='Value', names='Location')

    return fig


@app.callback(
    Output('pie_flats_per_area_cat', 'figure'),
    Input('area-dropdown', 'value'))
def update_figure(selected_city):
    data = get_json()
    dff = data["flats_per_area_cat"]
    dff = pd.DataFrame(dff.items(), columns=['Area', 'Value'])

    fig = px.pie(dff, values='Value', names='Area')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
