# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 22:42:46 2022

@author: asfard1
"""

import dash
from dash import ctx
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import dash_table as dt
import pandas as pd

from funcs_extra import df_lultilayer, resin_uniq_name, update_table_ref_lw

# parameters
float_round=2
style_as_list_view=False
style_table={'height': '300px', 'overflowY': 'visible', }
style_table_lw={'height': 'auto', 'overflowY': 'visible', 'width':'60%', 'marginLeft': 'auto', 'marginRight': 'auto' }
style_header={'backgroundColor': 'white','fontWeight':'bold', 'border': '1px solid pink', 'height': 'auto'}
style_data={'backgroundColor': 'white', 'color': 'blue', 'border': '1px solid blue', 'height': 'auto', 'whiteSpace': 'normal'}
style_cell={'textAlign': 'center', 'whiteSpace': 'normal','height': 'auto',}
style_cell_conditional=[ {'if': {'column_id': 'overall composition'}, 'textAlign': 'left' } ]
fill_width=False

#################################################################################################################################
pe_mat= pd.read_csv('Copy of ProspectorExport PE copolymer.csv', encoding = "ISO-8859-1")
price_whole= pd.read_csv('price.csv', encoding = "ISO-8859-1")
price_whole.drop(price_whole.columns[price_whole.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

currency= pd.read_csv('currency.csv', encoding = "ISO-8859-1")

resin_uniq_name=list(resin_uniq_name(price_whole))

resin_uniq_name.sort()

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
                                                                          
                                     html.Div(id = 'table1_ly_w', children=[html.Div('Reference Structure', style={'color':'black', "font-weight": "bold"}),
                                                                             dt.DataTable(id='table_ref_ly_w', data=[], columns=[],
                                                                                          style_as_list_view=style_as_list_view, 
                                                                                          style_table=style_table_lw,
                                                                                          style_header=style_header,
                                                                                          style_data=style_data,
                                                                                          style_cell=style_cell,
                                                                                          style_cell_conditional=style_cell_conditional, 
                                                                                          fill_width=fill_width
                                                                                          )
                                                                            ],
                                              className = 'tableDiv', style={'color':'black', 'width':'50%'}),
                                     html.Div(
                                         id = 'table1',
                                         children = [dt.DataTable( id = 'ref_table', 
                                                         style_as_list_view=style_as_list_view, style_table=style_table,
                                                         style_header=style_header,
                                                         style_data=style_data,
                                                         style_cell=style_cell,
                                                         style_cell_conditional=style_cell_conditional,
                                                         columns=[], data=[], fill_width=fill_width, editable=True, row_deletable=True, 
                                                         dropdown_conditional=[{
                                                             'if': {
                                                                 'column_id': 'overall composition',
                                                                 'filter_query': '{id} > 1'
                                                                   },
                                                             'options': [
                                                                 {'label': i, 'value': i}
                                                                 for i in resin_uniq_name
                                                             ]
                                                         },
                                                            # {
                                                            #     'if': {
                                                            #         'column_id': '0',
                                                            #         'filter_query': '{id} = 0'
                                                            #           },
                                                            #     'options': [{'label':"input layer ratio's", 'value':'arash'}]
                                                             #}
                                                             ]
                                                    )    
                                          ],
                                         className = 'tableDiv', style={'color':'black', 'width':'45%'}),
        
                                    ],
                                style={'textAlign':'center', 'color':'red', 'backgroundColor':'lightgreen'} 
                     )

  # callback to update the ref
@app.callback(  [ Output('ref_table', 'data'),    Output('ref_table', 'columns')],
                [ Input( 'num_layer', 'value'),
                  Input( 'num_mat',  'value'),
                  #Input('ref_table', 'data_timestamp'),
                  #State('ref_table', 'data')
                  ] )

           
def update_table_ref(num_layer, num_resin):#, data):
      
    
      df= df_lultilayer(num_layer, num_resin)
      
      if 'id' not in df.columns:
          #df['overall weights'] = 0
          df['id'] = df.index
          mycolumns = [{'name': i, 'id': i, 'type': 'numeric'} for i in df.columns[0:-1]]
          mycolumns[0]= {'name': 'overall composition', 'id': 'overall composition', 'presentation': 'dropdown'}
          mycolumns[len(mycolumns)-1]= {'name': 'overall weights', 'id': 'overall weights', 'editable': False}
          
          #df=update_table_ref_lw(df)
         
      return df.to_dict("rows"), mycolumns

#def update_table_ref_overall( data, data_w):
      
#      df= pd.DataFrame(data)
#      df_w= pd.DataFrame(data_w)
#      
#      cols_layers   = [c for c in df.columns if 'Layer' in c] # columns name with layer composition
#      cols_layers_w = [c for c in df_w.columns ]
#
#      out = (df[cols_layers] * df_w[cols_layers_w].values).sum(axis=1)
      
#      df['overall weights']= out 
#      return df.to_dict("rows")

# callback to update table Refrence




   

            
if __name__=='__main__':
    app.run_server(debug=True, use_reloader=False)
