# # --- import libraries ---
# import dash
# import dash_table
# import dash_core_components as dcc
# import dash_html_components as html
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from dash.dependencies import Output, Input
#
# # --- load data ---
# df_h = pd.read_csv('df_h.csv')
# df_h['Date'] = pd.to_datetime(df_h['Date'])
#
# df_t = pd.read_csv('dash_table.csv')
# # geo_df = pd.read_csv('geo_df.csv')
# df_arima = pd.read_csv('df_arima.csv')
# df_arima['Date'] = pd.to_datetime(df_arima['Date'])
# df_arima['Date'] = df_arima['Date'].dt.strftime('%Y-%m')
#
# options = []
# for column in df_h.columns:
#     options.append({'label': '{}'.format(column, column), 'value': column})
# options = options[1:]
#
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
# # --- initialize the app ---
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server
#
# # --- layout the dashboard ---
# app.layout = html.Div([
#     html.Div([
#         html.Div([
#             html.H1('Analysis of US Home Prices and Median Income',
#                     style={'textAlign': 'center',
#                            'color': '#FFFFFF',
#                            'fontSize': '36px',
#                            'padding-top': '0px'},
#                     ),
#
#             html.P('By Martin Palkovic', style={'textAlign': 'center',
#                                                 'color': '#FFFFFF',
#                                                 'fontSize': '24px'},
#                    ),
#             html.P('''An interactive dashboard displaying data for income,
#                        population and housing prices in the United States ''',
#                    style={'textAlign': 'center',
#                           'color': '#FFFFFF',
#                           'fontSize': '16px'},
#                    ),
#         ],
#             style={'backgroundColor': '#1f3b4d',
#                    'height': '200px',
#                    'display': 'flex',
#                    'flexDirection': 'column',
#                    'justifyContent': 'center'},
#         ),
#         html.Div([
#             html.Div([
#                 html.Label('Select a city to see home price data'),
#                 dcc.Dropdown(
#                     id='city-dropdown',
#                     options=options,
#                     value='Denver, CO',
#                     multi=False,
#                     clearable=True,
#                     searchable=True,
#                     placeholder='Choose a City...',
#                 ),
#             ],
#                 style={'width': '25%',
#                        'display': 'inline-block',
#                        'padding-left': '150px',
#                        'padding-top': '20px'}
#             ),
#             html.Div(
#                 dcc.Graph(id='forecast-container',
#                           style={'padding': '25px'}),
#             )
#         ]),
#         html.Div([
#             html.Div(
#                 dcc.Graph(id='graph-container',
#                           style={'padding': '25px'}),
#             ),
#             html.Div(
#                 dcc.Graph(id='map-container',
#                           style={'padding': '50px'})
#             ),
#             html.Label('''Filter data in the first row of the table to see
#                        changes on the map and graph! Example: > 100000 Population,
#                        < 300000 Median Home price, etc.''',
#                        style={'padding-left': '5px'}),
#             dash_table.DataTable(
#                 id='datatable',
#                 columns=[{'name': i, 'id': i,
#                           'deletable': True, 'selectable': True,
#                           'hideable': True} for i in df_t.columns],
#                 data=df_t.to_dict('records'), editable=False,
#                 filter_action='native', sort_action='native',
#                 sort_mode='multi', column_selectable='multi',
#                 row_selectable='multi', row_deletable=True,
#                 selected_columns=[], selected_rows=[],
#                 page_action='native', page_current=0,
#                 page_size=100, fill_width=False,
#                 style_table={'padding': '50px',
#                              'height': '300px',
#                              'overflowY': 'auto'},
#                 style_cell_conditional=[
#                     {'if': {'column_id': c},
#                      'textAlign': 'center'}
#                     for c in ['Population', 'Median Household Income ($USD)',
#                               'Median Home Price ($USD, January 2021)']
#                 ],
#                 style_data={
#                     'whiteSpace': 'normal',
#                     'height': 'auto',
#                 }
#             ),
#             html.Label('References:',
#                        style={'padding': '10px'}
#                        ),
#             html.Label('[1] Zillow, 2021, Zillow Home Value Index Data (ZHVI), All Homes, Time Series, Raw Mid Tier:',
#                        style={'padding-left': '25px'}),
#             html.A('https://www.zillow.com/research/data/',
#                    style={'padding-left': '25px'}),
#             html.Label('[2] Golden Oak Research Group, 2017, US Household Income Statistics:',
#                        style={'padding-left': '25px'}),
#             html.A('https://www.kaggle.com/goldenoakresearch/us-household-income-stats-geo-locations',
#                    style={'padding-left': '25px'}),
#             html.Label('[3] GeoNames API (Geocoders):',
#                        style={'padding-left': '25px'}),
#             html.A('https://geocoder.readthedocs.io/providers/GeoNames.html',
#                    style={'padding-left': '25px',
#                           'padding-bottom': '25px'}),
#         ],
#         ),
#     ],
#     ),
# ],
# )
#
#
# # --- dropdown callback ---
# @app.callback(
#     Output('forecast-container', 'figure'),
#     Input('city-dropdown', 'value'))
# def update_figure(selected_city):
#     dff = df_h[['Date', selected_city]]
#     # dff[selected_city] = dff[selected_city].round(0)
#     dfa = df_arima[df_arima['City'] == selected_city]
#
#     fig = px.line(dff, x='Date', y=selected_city,
#                   hover_data={selected_city: ':$,f'}).update_traces(
#         line=dict(color='#1f3b4d', width=2))
#
#     fig.add_scatter(x=dfa.Date, y=dfa.Mean,
#                     line_color='orange', name='Forecast Mean',
#                     hovertemplate='Forecast Mean: %{y:$,f}<extra></extra>')
#
#     fig.add_scatter(x=dfa.Date, y=dfa.Lower_ci,
#                     fill='tonexty', fillcolor='rgba(225,225,225, 0.3)',
#                     marker={'color': 'rgba(225,225,225, 0.9)'},
#                     name='Lower 95% Confidence Interval',
#                     hovertemplate='Lower 95% Confidence Interval: %{y:$,f}<extra></extra>')
#
#     fig.add_scatter(x=dfa.Date, y=dfa.Upper_ci,
#                     fill='tonexty', fillcolor='rgba(225,225,225, 0.3)',
#                     marker={'color': 'rgba(225,225,225, 0.9)'},
#                     name='Upper 95% Confidence Interval',
#                     hovertemplate='Upper 95% Confidence Interval: %{y:$,f}<extra></extra>')
#
#     fig.update_layout(template='xgridoff',
#                       yaxis={'title': 'Median Home Price ($USD)'},
#                       xaxis={'title': 'Year'},
#                       title={'text': 'Median Home Price vs. Year for {}'.format(selected_city),
#                              'font': {'size': 24}, 'x': 0.5, 'xanchor': 'center'}
#                       )
#
#     return fig
#
#
# # --- graph callback ---
# @app.callback(
#     Output('graph-container', 'figure'),
#     Input('datatable', 'derived_virtual_data'))
# def update_scatter(all_rows_data):
#     dff = pd.DataFrame(all_rows_data)
#
#     fig = px.scatter(dff, x='Median Home Price ($USD, January 2021)',
#                      y='Median Household Income ($USD)', size='Population',
#                      size_max=25, color='Median Home Price ($USD, January 2021)',
#                      color_continuous_scale='jet', hover_name='City',
#                      hover_data={'Latitude': False, 'Longitude': False,
#                                  'Population': ':,2f', 'Median Household Income ($USD)': ':$,2f',
#                                  'Median Home Price ($USD, January 2021)': ':$,2f'})
#
#     fig.update_layout(title_text='Median Household Income vs. Median Home Price ($USD) in the United States',
#                       title_font_size=24,
#                       title_xref='container',
#                       title_y=0.95,
#                       title_x=0.5,
#                       showlegend=False,
#                       hovermode='closest',
#                       template='xgridoff')
#
#     return fig
#
#
# # --- map callback ---
# @app.callback(
#     Output('map-container', 'figure'),
#     Input('datatable', 'derived_virtual_data'))
# def update_map(all_rows_data):
#     dff = pd.DataFrame(all_rows_data)
#
#     fig = px.scatter_geo(dff, lat='Latitude', lon='Longitude', size='Population',
#                          size_max=25, color='Median Home Price ($USD, January 2021)',
#                          color_continuous_scale='jet', hover_name='City',
#                          hover_data={'Latitude': False,
#                                      'Longitude': False,
#                                      'Population': ':,2f',
#                                      'Median Household Income ($USD)': ':$,2f',
#                                      'Median Home Price ($USD, January 2021)': ':$,2f'})
#
#     fig.update_layout(
#         title_text='Median Home Price (Dec 2020), Income (2017) and City Populations (2019) for the United States',
#         title_font_size=24,
#         title_xref='container',
#         title_y=0.99,
#         title_x=0.5,
#         showlegend=True,
#         geo=dict(scope='usa', landcolor='rgba(225, 225, 225, 0.75)'),
#         width=1200, height=700, legend_title_text='City size, ranked by population')
#
#     return fig
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)