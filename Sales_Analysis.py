from dash import Dash, dcc, html, dash_table as dt
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


sales = pd.read_csv('Sales-Data.csv')
sales['Order Date'] = pd.to_datetime(sales['Order Date'], dayfirst= True)
sales['Year'] = sales['Order Date'].dt.year
sales['Month'] = sales['Order Date'].dt.month_name()
app = Dash(__name__, meta_tags=[{'name': 'viewport', 'content': 'width=device-width'}])
server = app.server
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3('Sales Dashboard', style={'margin-bottom': '0px', 'color': 'white'})

        ], className='one-third column', id='title1'),
        html.Div([
            html.P('year', className='fix_label', style={'color': 'white'}),
            dcc.Slider(id='select_years',
                       included=False,
                       updatemode='drag',
                       tooltip={'always_visible': True},
                       min=2015,
                       max=2018,
                       step=1,
                       value=2018,
                       marks={str(yr): str(yr) for yr in range(2015, 2019)},
                       className='dcc_compon'),

        ], className='one-half column', id='title2'),


        html.Div([
            html.P('Segment', className='fix_label', style={'color': 'white'}),
            dcc.RadioItems(id='radio_items',
                       labelStyle={'display': 'inline-block'},
                       value='Consumer',
                       options=[{'label': i, 'value': i} for i in sales['Segment'].unique()],
                           style={'text-align': 'center', 'color': 'white'},
                       className='dcc_compon'),

        ], className='one-third column', id='title3')

    ], id='header', className='row flex-display', style={'margin-bottom': '25px'}),
    html.Div([
        html.Div([
            dcc.RadioItems(id='radio_items1',
                       labelStyle={'display': 'inline-block'},
                       value='Sub-Category',
                       options=[{'label': 'Sub-Category' , 'value': 'Sub-Category'},
                                {'label': 'Region' , 'value': 'Region'}],
                           style={'text-align': 'center', 'color': 'white'},
                       className='dcc_compon'),
            dcc.Graph(id='bar_chart_1', config={'displayModeBar': 'hover'},
                      style={'height': '350px'})

        ], className='create_container2 three columns', style={'height': '400px'}),

html.Div([

            dcc.Graph(id='donut_chart', config={'displayModeBar': 'hover'},
                      style={'height': '350px'})

        ], className='create_container2 three columns', style={'height': '400px'}),
html.Div([

            dcc.Graph(id='line_chart', config={'displayModeBar': 'hover'},
                      style={'height': '350px'})

        ], className='create_container2 four columns', style={'height': '400px'}),

html.Div([

            html.Div(id='text1'),
            html.Div(id='text2'),
            html.Div(id='text3'),

        ], className='create_container2 two columns')

    ], className='row flex-display'),
    html.Div([
        html.Div([
        dt.DataTable(id='my_datatable',
                     columns=[{'name': i, 'id': i} for i in
                              sales.loc[:, ['Order Date', 'Customer ID', 'Customer Name',
                                            'Segment', 'Country', 'City', 'State',
                                            'Region', 'Category', 'Sub-Category', 'Product Name', 'Sales',
                                            'Year',	'Month']]],
                     virtualization= True,
                     style_cell={'textAlign': 'left',
                                 'min-width': '100px',
                                 'backgroundColor': '#1f2c56',
                                 'color': '#FEFEFE',
                                 'border-bottom': '0.01rem solid #19AAE1'},
                     style_header={'backgroundColor': '#1f2c56',
                                   'fontWeight': 'bold',
                                   'font': 'Lato, sans-serif',
                                   'color': 'orange',
                                   'border': '#1f2c56'},
                     style_as_list_view=True,
                     style_data={'styleOverflow': 'hidden', 'color': 'white'},
                     fixed_rows={'headers': True},
                     sort_action='native',
                     sort_mode='multi')
        ], className='create_container2 three columns'),

        html.Div([
dcc.RadioItems(id='radio_items2',
                       labelStyle={'display': 'inline-block'},
                       value='State',
                       options=[{'label': 'State' , 'value': 'State'},
                                {'label': 'City' , 'value': 'City'}],
                           style={'text-align': 'center', 'color': 'white'},
                       className='dcc_compon'),
            dcc.Graph(id='bar_chart_2', config={'displayModeBar': 'hover'},
                      ),


        ], className='create_container2 three columns'),
html.Div([
            dcc.Graph(id='bubble_chart', config={'displayModeBar': 'hover'})

        ], className='create_container2 six columns'),




    ], className='row flex-display')

], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

@app.callback(Output('bar_chart_1', 'figure'),
              [Input('select_years','value')],
              [Input('radio_items','value')],
              [Input('radio_items1','value')])
def update_graph(select_years, radio_items, radio_items1):
    sales1 = sales.groupby(['Year', 'Sub-Category', 'Segment'])['Sales'].sum().reset_index()
    sales2 = sales1[(sales1['Year'] == select_years) & (sales1['Segment'] == radio_items)].sort_values(by = ['Sales'],
                                        ascending = False).nlargest(5, columns = ['Sales'])
    sales3 = sales.groupby(['Year', 'Region', 'Segment'])['Sales'].sum().reset_index()
    sales4 = sales3[(sales3['Year'] == select_years) & (sales3['Segment'] == radio_items)].sort_values(by=['Sales'],
                                        ascending = False).nlargest(5, columns=['Sales'])

    if radio_items1 == 'Sub-Category':


     return {
        'data': [
            go.Bar(
                x=sales2['Sales'],
                y=sales2['Sub-Category'],
                text = sales2['Sales'],
                texttemplate= '$' + '%{text:,.2s}',
                textposition='auto',
                orientation= 'h',
                marker=dict(color='#19AAE1'),
                hoverinfo='text',
                hovertext=
                '<b>Year</b>: ' + sales2['Year'].astype(str) + '<br>' +
                '<b>Segment</b>: ' + sales2['Segment'].astype(str) + '<br>' +
                '<b>Sub-Category</b>: ' + sales2['Sub-Category'].astype(str) + '<br>' +
                '<b>Sales</b>: $' + [f'{x:,.0f}' for x in sales2['Sales']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Sales by Sub-Category' + ' ' + str((select_years)),
                   'y': 0.99,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 12},
            font=dict(family='sans-serif',
                      color='white',
                      size=15),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#010915',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t = 40, r=0),
            xaxis=dict(title='<b></b>',
                       color = 'orange',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='orange',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='orange',
                           size=12
                       )),
            yaxis=dict(title='<b></b>',
                       color='orange',
                       autorange='reversed',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='orange',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='orange',
                           size=12
                       )
                       )


        )
    }

    elif radio_items1 == 'Region':


     return {
        'data': [
            go.Bar(
                x=sales4['Sales'],
                y=sales4['Region'],
                text = sales4['Sales'],
                texttemplate= '$' + '%{text:,.2s}',
                textposition='auto',
                orientation= 'h',
                marker=dict(color='#19AAE1'),
                hoverinfo='text',
                hovertext=
                '<b>Year</b>: ' + sales4['Year'].astype(str) + '<br>' +
                '<b>Segment</b>: ' + sales4['Segment'].astype(str) + '<br>' +
                '<b>Region</b>: ' + sales4['Region'].astype(str) + '<br>' +
                '<b>Sales</b>: $' + [f'{x:,.0f}' for x in sales4['Sales']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Sales by Region in Year' + ' ' + str((select_years)),
                   'y': 0.99,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 12},
            font=dict(family='sans-serif',
                      color='white',
                      size=15),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#010915',
                    'xanchor': 'center', 'x': 0.4, 'y': -0.7},
            margin=dict(t = 40, r=0),
            xaxis=dict(title='<b></b>',
                       color = 'orange',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='orange',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='orange',
                           size=12
                       )),
            yaxis=dict(title='<b></b>',
                       color='orange',
                       autorange='reversed',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='orange',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='orange',
                           size=12
                       )
                       )


        )
    }

@app.callback(Output('donut_chart', 'figure'),
              [Input('select_years','value')],
              [Input('radio_items','value')])
def update_graph(select_years, radio_items):
    sales5 = sales.groupby(['Year', 'Category', 'Segment'])['Sales'].sum().reset_index()
    sales_furniture = sales5[(sales5['Year'] == select_years) & (sales5['Segment'] == radio_items) & (sales5['Category'] == 'Furniture')]['Sales'].sum()
    sales_Office = sales5[(sales5['Year'] == select_years) & (sales5['Segment'] == radio_items) & (sales5['Category'] == 'Office Supplies')]['Sales'].sum()
    sales_Technology = sales5[(sales5['Year'] == select_years) & (sales5['Segment'] == radio_items) & (sales5['Category'] == 'Technology')]['Sales'].sum()
    colors = ['#30C9C7', '#7A45D1', 'orange']



    return {
            'data': [go.Pie(
                labels=['Furniture', 'Office Supplies', 'Technology'],
                values=[sales_furniture, sales_Office, sales_Technology],
                marker=dict(colors=colors),
                hoverinfo='label+value+percent',
                textinfo='label+value',
                texttemplate='%{label} <br>$%{value:,.2f}',
                textposition='auto',
                textfont=dict(size=13),
                hole=.7,
                rotation=160,
                # insidetextorientation= 'radial'

            )],

            'layout': go.Layout(
                title={'text': 'Sales by Category in year' + ' ' + str((select_years)),
                       'y': 0.93,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                titlefont={'color': 'white',
                           'size': 15},
                font=dict(family='sans-serif',
                          color='white',
                          size=12),
                hovermode='closest',
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                legend={'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'xanchor': 'center', 'x': 0.5, 'y': -0.7}

            )
        }
@app.callback(Output('line_chart', 'figure'),
              [Input('select_years','value')],
              [Input('radio_items','value')])

def update_graph(select_years, radio_items):
    sales6 = sales.groupby(['Year', 'Month', 'Segment'])['Sales'].sum().reset_index()
    sales7 = sales6[(sales6['Year'] == select_years) & (sales6['Segment'] == radio_items)]




    return {
        'data': [
            go.Scatter(
                x=sales7['Month'],
                y=sales7['Sales'],
                text=sales7['Sales'],
                texttemplate='$' + '%{text:,.2s}',
                textposition='bottom left',
                mode='markers+lines+text',
                line=dict(width=3, color = 'orange'),
                marker=dict(color='#19AAE1', size=10, symbol='circle',
                            line=dict(color='#19AAE1', width=2)),
                hoverinfo='text',
                hovertext=
                '<b>Year</b>: ' + sales7['Year'].astype(str) + '<br>' +
                '<b>Month</b>: ' + sales7['Month'].astype(str) + '<br>' +
                '<b>Segment</b>: ' + sales7['Segment'].astype(str) + '<br>' +
                '<b>Sales</b>: $' + [f'{x:,.0f}' for x in sales7['Sales']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Sales Trend in Year' + ' ' + str((select_years)),
                   'y': 0.99,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 12},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#010915',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t = 5, l=0, r=0),
            xaxis=dict(title='<b></b>',
                       color = 'orange',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='orange',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='orange',
                           size=12
                       )),
            yaxis=dict(title='<b></b>',
                       color='orange',
                       showline=False,
                       showgrid=True,
                       showticklabels=False,
                       linecolor='orange',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='orange',
                           size=12
                       )
                       )


        )
    }


@app.callback(Output('text1', 'children'),
              [Input('select_years', 'value')])

def update_graph(select_years):
    sales8 = sales.groupby(['Year'])['Sales'].sum().reset_index()
    current_year = sales8[(sales8['Year'] == select_years)]['Sales'].sum()

    return[
        html.H6(children='Current_Year',
                style={'textAlign': 'center',
                       'color': 'white'}),
        html.P('${0:,.2f}'.format(current_year),
               style={'textAlign': 'center',
                      'color': '#19AAE1',
                      'fontSize': 15,
                      'margin-top': '-10px'}
               )
    ]


@app.callback(Output('text2', 'children'),
              [Input('select_years', 'value')])

def update_graph(select_years):
    sales10 = sales.groupby(['Year'])['Sales'].sum().reset_index()
    sales10['PY'] = sales10['Sales'].shift(1)
    previous_year = sales10[(sales10['Year'] == select_years)]['PY'].sum()

    return[
        html.H6(children='Previous_Year',
                style={'textAlign': 'center',
                       'color': 'white'}),
        html.P('${0:,.2f}'.format(previous_year),
               style={'textAlign': 'center',
                      'color': '#19AAE1',
                      'fontSize': 15,
                      'margin-top': '-10px'}
               )
    ]

@app.callback(Output('text3', 'children'),
              [Input('select_years', 'value')])

def update_graph(select_years):
    sales11 = sales.groupby(['Year'])['Sales'].sum().reset_index()
    sales11['YOY Growth'] = sales11['Sales'].pct_change()
    sales11['YOY Growth'] = sales11['YOY Growth']*100
    growth_year = sales11[(sales11['Year'] == select_years)]['YOY Growth'].sum()

    return[
        html.H6(children='Growth_Year',
                style={'textAlign': 'center',
                       'color': 'white'}),
        html.P('{0:,.2f}%'.format(growth_year),
               style={'textAlign': 'center',
                      'color': '#19AAE1',
                      'fontSize': 15,
                      'margin-top': '-10px'}
               )
    ]
@app.callback(Output('my_datatable', 'data'),
              [Input('select_years','value')],
              [Input('radio_items','value')])

def update_graph(select_years, radio_items):
    data_table = sales[(sales['Year'] == select_years) & (sales['Segment'] == radio_items)]
    return data_table.to_dict('records')



@app.callback(Output('bar_chart_2', 'figure'),
              [Input('select_years','value')],
              [Input('radio_items','value')],
              [Input('radio_items2','value')])
def update_graph(select_years, radio_items, radio_items2):
    sales12 = sales.groupby(['Year', 'State', 'Segment'])['Sales'].sum().reset_index()
    sales13 = sales12[(sales12['Year'] == select_years) & (sales12['Segment'] == radio_items)].sort_values(by = ['Sales'],
                                        ascending = False).nlargest(10, columns = ['Sales'])
    sales14 = sales.groupby(['Year', 'City', 'Segment'])['Sales'].sum().reset_index()
    sales15 = sales14[(sales14['Year'] == select_years) & (sales14['Segment'] == radio_items)].sort_values(by=['Sales'],
                                        ascending = False).nlargest(10, columns=['Sales'])

    if radio_items2 == 'State':


     return {
        'data': [
            go.Bar(
                x=sales13['Sales'],
                y=sales13['State'],
                text = sales13['Sales'],
                texttemplate= '$' + '%{text:,.2s}',
                textposition='auto',
                orientation= 'h',
                marker=dict(color='#19AAE1'),
                hoverinfo='text',
                hovertext=
                '<b>Year</b>: ' + sales13['Year'].astype(str) + '<br>' +
                '<b>Segment</b>: ' + sales13['Segment'].astype(str) + '<br>' +
                '<b>State</b>: ' + sales13['State'].astype(str) + '<br>' +
                '<b>Sales</b>: $' + [f'{x:,.0f}' for x in sales13['Sales']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Sales State in Year' + ' ' + str((select_years)),
                   'y': 0.99,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 12},
            font=dict(family='sans-serif',
                      color='white',
                      size=15),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#010915',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t = 40, r=0),
            xaxis=dict(title='<b></b>',
                       color = 'orange',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='orange',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='orange',
                           size=12
                       )),
            yaxis=dict(title='<b></b>',
                       color='orange',
                       autorange='reversed',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='orange',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='orange',
                           size=12
                       )
                       )


        )
    }

    elif radio_items2 == 'City':


     return {
        'data': [
            go.Bar(
                x=sales15['Sales'],
                y=sales15['City'],
                text = sales15['Sales'],
                texttemplate= '$' + '%{text:,.2s}',
                textposition='auto',
                orientation= 'h',
                marker=dict(color='#19AAE1'),
                hoverinfo='text',
                hovertext=
                '<b>Year</b>: ' + sales15['Year'].astype(str) + '<br>' +
                '<b>Segment</b>: ' + sales15['Segment'].astype(str) + '<br>' +
                '<b>City</b>: ' + sales15['City'].astype(str) + '<br>' +
                '<b>Sales</b>: $' + [f'{x:,.0f}' for x in sales15['Sales']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Sales by City in Year' + ' ' + str((select_years)),
                   'y': 0.99,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 12},
            font=dict(family='sans-serif',
                      color='white',
                      size=15),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#010915',
                    'xanchor': 'center', 'x': 0.4, 'y': -0.7},
            margin=dict(t = 40, r=0),
            xaxis=dict(title='<b></b>',
                       color = 'orange',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='orange',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='orange',
                           size=12
                       )),
            yaxis=dict(title='<b></b>',
                       color='orange',
                       autorange='reversed',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='orange',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='orange',
                           size=12
                       )
                       )


        )
    }

@app.callback(Output('bubble_chart', 'figure'),
                  [Input('select_years', 'value')],
                  [Input('radio_items', 'value')])
def update_graph(select_years, radio_items):
        sales16 = sales.groupby(['Year', 'Month', 'Segment', 'State', 'City'])['Sales'].sum().reset_index()
        sales17 = sales16[(sales16['Year'] == select_years) & (sales16['Segment'] == radio_items)]

        return {
            'data': [
                go.Scatter(
                    x=sales17['Month'],
                    y=sales17['Sales'],
                    text=sales17['Sales'],

                    mode='markers',
                    line=dict(width=3, color='orange'),
                    marker=dict(color=sales17['Sales'], colorscale='HSV',
                                showscale=False,
                                size=sales17['Sales'] / 250, symbol='circle',
                                line=dict(color='MediumPurple', width=2)),
                    hoverinfo='text',
                    hovertext=
                    '<b>Year</b>: ' + sales17['Year'].astype(str) + '<br>' +
                    '<b>Month</b>: ' + sales17['Month'].astype(str) + '<br>' +
                    '<b>Segment</b>: ' + sales17['Segment'].astype(str) + '<br>' +
                    '<b>State</b>: ' + sales17['State'].astype(str) + '<br>' +
                    '<b>City</b>: ' + sales17['City'].astype(str) + '<br>' +
                    '<b>Sales</b>: $' + [f'{x:,.0f}' for x in sales17['Sales']] + '<br>'

                ),

            ],

            'layout': go.Layout(
                title={'text': 'Sales by State and City in Year' + ' ' + str((select_years)),
                       'y': 0.99,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                titlefont={'color': 'white',
                           'size': 12},
                font=dict(family='sans-serif',
                          color='white',
                          size=12),
                hovermode='closest',
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                legend={'orientation': 'h',
                        'bgcolor': '#010915',
                        'xanchor': 'center', 'x': 0.5, 'y': -0.7},
                margin=dict(t=40, l=0, r=0),
                xaxis=dict(title='<b></b>',
                           color='orange',
                           showline=True,
                           showgrid=False,
                           showticklabels=True,
                           linecolor='orange',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Aerial',
                               color='orange',
                               size=12
                           )),
                yaxis=dict(title='<b></b>',
                           color='orange',
                           showline=False,
                           showgrid=True,
                           showticklabels=False,
                           linecolor='orange',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Aerial',
                               color='orange',
                               size=12
                           )
                           )

            )
        }




if __name__ == '__main__':
    app.run_server(debug=True)

