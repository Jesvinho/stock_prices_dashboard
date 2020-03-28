import dash
from datetime import datetime as dt
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from dash.dependencies import Input,Output,State
import pandas_datareader.data as web
import os

os.environ["IEX_API_KEY"]="pk_0c37f645c7a84d5b9a9d86a4bbdbf867"

np.random.seed(43)
y_data=np.random.random(100)*300
x_data=np.arange(100).tolist()

companies=pd.read_csv('companies_new.csv',index_col='Unnamed: 0')
companies.set_index('symbol',inplace=True)

grid=[]
for tic in companies.index:
    my_dict={}
    my_dict['label']=str(companies.loc[tic]['name'])+''+str(tic)
    my_dict['value']=tic
    grid.append(my_dict)
print(grid)


graph_data=go.Scatter(x=x_data,y=y_data, mode='lines+markers',text=y_data)
graph_layout= go.Layout(title='TSLA  Closing prices',
                xaxis={'title':'date'},
                yaxis={'title':'stockprices'},
                hovermode='closest')

app=dash.Dash()

app.layout=html.Div([
                    html.Div(children=html.H1('Stock Ticker Dashboard')),

                    html.Div([html.Div([
    dcc.Dropdown(
        id='section_2-1_input',
        options=grid,
        value='F',
        multi=False
    ),
    html.Div(id='section_2-1_output')
],style={'width':'30%','display':'inline-block'}),
                    html.Div([
    dcc.DatePickerRange(
        id='section_2-2_input',
        min_date_allowed=dt(1995, 8, 5),
        max_date_allowed=dt.today(),
        initial_visible_month=dt.today(),
        end_date=dt.today().date()
    ),
    html.Div(id='section_2-2_output')
],style={'width':'30%','display':'inline-block'}),
html.Div([html.Button('Submit', id='section_2-3')]),

                    html.Div([dcc.Graph(id='stock-graph',
                                        figure={'data':[graph_data],
                                                'layout':graph_layout},
                                        style= {'width':'80%',
                                                'height':'425px'})
                            ])
                            ])

                    ])





@app.callback(
    dash.dependencies.Output('section_2-1_output', 'children'),
    [dash.dependencies.Input('section_2-1_input', 'value')])
def update_dropdown(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    dash.dependencies.Output('section_2-2_output', 'children'),
    [dash.dependencies.Input('section_2-2_input', 'start_date'),
     dash.dependencies.Input('section_2-2_input', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(start_date.split('T')[0], '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(end_date.split('T')[0], '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix



@app.callback(Output('stock-graph','figure'),
                [Input('section_2-3','n_clicks')],
                [State('section_2-2_input','start_date'),
                State('section_2-2_input','end_date'),
                State('section_2-1_input','value')])
def graph_update(n_clicks,start_date,end_date,value):
    start=start_date
    end=end_date
    #df=pd.read_pickle('ford_feb_to_march28.pkl')
    df=web.DataReader(value,'iex',start,end)
    graph_data=go.Scatter(x=df.index,y=df['close'], mode='lines+markers',text=y_data)
    graph_layout= go.Layout(title='TSLA  Closing prices',
                    xaxis={'title':'date'},
                    yaxis={'title':'stockprices'},
                    hovermode='closest')
    return {'data':[graph_data],
            'layout':graph_layout}






if __name__=='__main__':
    app.run_server()
