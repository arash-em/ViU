# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 22:42:46 2022

@author: asfard1
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash_table as dt
import pandas as pd

from funcs_extra import df_lultilayer, resin_uniq_name



pe_mat= pd.read_csv('Copy of ProspectorExport PE copolymer.csv', encoding = "ISO-8859-1")
price_whole= pd.read_csv('price.csv', encoding = "ISO-8859-1")
price_whole.drop(price_whole.columns[price_whole.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

currency= pd.read_csv('currency.csv', encoding = "ISO-8859-1")

df= df_lultilayer(7, 5)
df['id'] = df.index
      
mycolumns = [{'name': i, 'id': i} for i in df.columns[0:-1]]
mycolumns[0]= {'name': 'overall composition', 'id': '0', 'presentation': 'dropdown'}


resin_uniq_name=list(resin_uniq_name(price_whole))

print(mycolumns)
app= dash.Dash()
app.layout = html.Div(children= [
                                     html.H1('ViU Polyethylene flexible Film'),
                                     html.Br(),
                                     html.Div( [html.Div('Select number of layers', style={'width':'20%'}),
                                                dcc.Dropdown([3,5,7], value=5, id='num_layer', style={'width':'40%'}),
                                                html.Div('Select Currency', style={'width':'20%'}),
                                                dcc.Dropdown(['US Dollar','Euro','Yuan', "Rupee"], placeholder='Select currency', id='currency', style={'width':'40%'}),
                                                html.Div('Select max number of materials', style={'width':'20%'}),
                                                dcc.Dropdown([5,10,15,20], value=5, id='num_mat', style={'width':'40%'}),
                                                html.Div('Select weight unit', style={'width':'20%'}),
                                                dcc.Dropdown(['KG','TON','LB'], placeholder='Select weight unit', id='w_unit', style={'width':'40%'}),
                                                ], style={'textAlign':'center',  'color':'blue', 'display':'flex', 'backgroundColor': 'yellow'}),
                                     html.Br(),
            
                                              
                                     html.Div(
                                         id = 'table1',
                                         children = 
                                         [ html.Div('Reference Structure', style={'color':'black', "font-weight": "bold"}), 
                                                     dt.DataTable( id = 'ref_table', 
                                                         style_as_list_view=False, style_table={'height': '300px', 'overflowY': 'auto'},
                                                         style_header={'backgroundColor': 'white','fontWeight':'bold', 'border': '1px solid pink', 'height': 'auto'},
                                                         style_data={'backgroundColor': 'white', 'color': 'blue', 'border': '1px solid blue', 'height': 'auto', 'whiteSpace': 'normal'},
                                                         style_cell={'textAlign': 'center', 'whiteSpace': 'normal','height': 'auto',},
                                                         style_cell_conditional=[ {
                                                                         'if': {'column_id': 'overall composition'}, 'textAlign': 'left' } ],
                                                         columns=mycolumns, data=df.to_dict("rows"), fill_width=False, editable=True, row_deletable=True, 
                                                         dropdown_conditional=[{
                                                             'if': {
                                                                 'column_id': '0',
                                                                 'filter_query': '{id} > 0'
                                                                   },
                                                             'options': [
                                                                 {'label': i, 'value': i}
                                                                 for i in resin_uniq_name
                                                             ]
                                                         }]
                                                    )    
                                          ],
                                         className = 'tableDiv', style={'color':'black', 'width':'45%'}),
                                    ],
                                style={'textAlign':'center', 'color':'red', 'backgroundColor':'lightgreen'}
                     )

            
if __name__=='__main__':
    app.run_server(debug=True, use_reloader=False)
