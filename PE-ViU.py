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
import numpy as np

from funcs_extra import df_lultilayer, resin_uniq_name, density, cost_calculation

# parameters
float_round=2
style_as_list_view=False
font_family='EMprint'
##################################################################################################
# Input Box Style
style_input_box0={'font-family':font_family , 'textAlign': 'left',  'height':'auto','width':'auto', 'font-size': '12px',"color": "blue", 'fontWeight':'bold', 'marginRight':'0px', 'marginTop':'3px'}
style_input_box00={'font-family':font_family,'textAlign': 'center', 'height':'5px', 'width':'100px', 'font-size': '12px',"color": "blue", 'marginRight':'50px', 'marginTop':'3px'}
style_input_box=     {'font-family':font_family,'textAlign': 'center', 'marginRight':'20px', 'marginTop':'8px', 'height':'10px','width':'8%', 'font-size': '10px'}
style_input_box_long={'font-family':font_family,'textAlign': 'center', 'marginRight':'20px', 'marginTop':'8px', 'height':'10px', 'width':'12%', 'font-size': '10px'}
style_input_box_header={'font-family':font_family, 'textAlign': 'left',"color": "blue", 'fontWeight':'bold', 'font-size': '10px', 'marginRight':'0px', 'marginTop':'3px'}
style_input_box_display={'font-family':font_family, 'textAlign': 'left',"color": "blue", 'fontWeight':'bold', 'font-size': '10px', 'marginLeft':'3px', 'marginTop':'3px', 'marginRight':'50px'}

style_ref_emc= {'font-family':font_family, 'color':'black', "font-weight": "bold", 'font-size': '15px'}
style_ref_emc_thick=style={'font-family':font_family, 'display':'inline-block', 'font-size': '12px', 'textAlign': 'center'}

# results Style
style_result_head= {'font-family':font_family, 'color':'red', "font-weight": "bold", 'font-size': '13px', 'textAlign': 'center'}

##################################################################################################
style_table={'overflowY': 'visible', 'fontSize':10}
style_table_mw={ 'overflowY': 'visible','padding-top': '30px' }
style_table_lw_ref={'height': 'auto', 'overflowY': 'visible', 'padding-left': '95px' }
style_table_lw_emc={'height': 'auto', 'overflowY': 'visible', 'padding-left': '142px' }

style_header={'backgroundColor': 'white','fontWeight':'bold', 'border': '1px solid pink', 'fontSize':10}
style_data={'backgroundColor': 'white', 'color': 'blue', 'border': '1px solid blue',  'whiteSpace': 'normal'}

style_cell={   'textAlign': 'center', 'whiteSpace': 'normal', 'height': '20px', 'width':'10px', 'fontSize':10}
style_cell_mw={'textAlign': 'center', 'whiteSpace': 'normal', 'width':'30px' , 'height': '35.3px', 'fontSize':10}
style_cell_lw={'textAlign': 'center', 'whiteSpace': 'normal', 'fontSize':10, 'height': '20px', 'width':'66px' }

style_cell_conditional=[ {'if': {'column_id': 'overall composition'}, 'textAlign': 'left' } ]
fill_width=False

#################################################################################################################################
pe_mat= pd.read_csv('Copy of ProspectorExport PE copolymer.csv', encoding = "ISO-8859-1")
price_whole= pd.read_csv('price.csv', encoding = "ISO-8859-1")
price_whole.drop(price_whole.columns[price_whole.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

currency= pd.read_csv('currency.csv', encoding = "ISO-8859-1")

resin_uniq_name,pe_price=resin_uniq_name(price_whole)
resin_uniq_name=list(resin_uniq_name)
resin_uniq_name.sort()
density=density (resin_uniq_name)

print(pe_price['ENABLE 2005CB'])

app= dash.Dash()
app.layout = html.Div(children= [    html.Div([html.Img(src=r'assets/Exxon_logo.png',  style={'height':'10%', 'width':'10%'}),
                                               html.H1('ViU Polyethylene flexible Film', style={'font-family':font_family, 'color':'black', 'marginLeft':'350px'})],
                                               style={'display':'flex', 'backgroundColor': 'white'}),
                                     html.Br(),
                                     html.Div( [html.Div('Select number of layers; reference', style=style_input_box0),
                                                dcc.Dropdown([3,5,7], value=5, id='num_layer', style=style_input_box00),
                                                html.Div('Select number of layers; EMC', style=style_input_box0),
                                                dcc.Dropdown([3,5,7], value=5, id='num_layer_emc', style=style_input_box00),
                                                html.Div('Select Currency', style=style_input_box0),
                                                dcc.Dropdown(['USD','Euro','Yuan', "Rupee"], value='USD', id='currency', style=style_input_box00),
                                                html.Div('Select max number of materials', style=style_input_box0),
                                                dcc.Dropdown([5,10,15,20], value=5, id='num_mat', style=style_input_box00),
                                                html.Div('Select weight unit', style=style_input_box0),
                                                dcc.Dropdown(['KG','TON','LB'], value='TON', id='w_unit', style=style_input_box00),
                                                html.Div('Select mixing', style=style_input_box0),
                                                dcc.Dropdown(['Mix by Weight','Mix by Volume'], value='Mix by Weight', id='mix_unit', style=style_input_box00),
                                                html.Div('Select Value Unit', style=style_input_box0),
                                                dcc.Dropdown(['MICRON', 'MM', 'MIL', 'IN', 'sq MICRON', 'sq MM', 'sq MIL', 'sq IN', 'LITER', 'GAL'], 
                                                             value='MICRON', id='dimen', style=style_input_box00)
                                                ], style={'textAlign':'center',  'display':'flex', 'backgroundColor': '#98FF11'}),
                                     html.Br(),
                                                                          
                                     html.Div([
                                        html.Div(id = 'table1_ly_w', children=[html.Div('Reference Structure', style=style_ref_emc),
                                                                               html.Div([
                                                                                   html.Div('Reference Thickness',style=style_ref_emc_thick), 
                                                                                   dcc.Input(id='ref_thick', type='number', value=100, 
                                                                                            style=style_input_box, step=5)]),
                                                                               dt.DataTable(id='table_ref_ly_w', data=[], columns=[],
                                                                                          style_as_list_view=style_as_list_view, 
                                                                                          style_table=style_table_lw_ref,
                                                                                          style_header=style_header,
                                                                                          style_data=style_data,
                                                                                          style_cell=style_cell_lw,
                                                                                          fill_width=fill_width
                                                                                          )
                                                                            ],
                                              className = 'tableDiv', style={'color':'black', 'width':'50%'}),
                                     
                                         html.Div(id = 'table2_ly_w', children=[html.Div('EMC Structure', style=style_ref_emc),
                                                                                html.Div([
                                                                                    html.Div('EMC Thickness',style=style_ref_emc_thick), 
                                                                                    dcc.Input(id='emc_thick', type='number', value=80, 
                                                                                             style=style_input_box, step=5)]),
                                                                                 dt.DataTable(id='table_emc_ly_w', data=[], columns=[],
                                                                                              style_as_list_view=style_as_list_view, 
                                                                                              style_table=style_table_lw_emc,
                                                                                              style_header=style_header,
                                                                                              style_data=style_data,
                                                                                              style_cell=style_cell_lw,
                                                                                              fill_width=fill_width
                                                                                              )
                                                                                ],
                                                  className = 'tableDiv', style={'color':'black', 'width':'40%'}), 
                                         ], style={'display':'flex'} ),
                                     
                                     html.Div([
                                         html.Div(
                                             id = 'table1',
                                             children = [html.Div([dt.DataTable( id = 'ref_table', 
                                                             style_as_list_view=style_as_list_view, 
                                                             style_header=style_header,
                                                             style_data=style_data,
                                                             style_cell=style_cell,
                                                             style_cell_conditional=style_cell_conditional,
                                                             columns=[], data=[], fill_width=fill_width, editable=True, row_deletable=True, 
                                                             dropdown_conditional=[{
                                                                 'if': {
                                                                     'column_id': 'overall composition',
                                                                     'filter_query': '{id} > 0'
                                                                       },
                                                                 'options': [
                                                                     {'label': i, 'value': i}
                                                                     for i in resin_uniq_name
                                                                 ]
                                                             },
                                                                 ]
                                                        )]),
                                                        html.Div([dt.DataTable( id = 'ref_table_w', 
                                                                         style_table=style_table_mw,
                                                                         style_as_list_view=style_as_list_view, 
                                                                         style_data=style_data,
                                                                         style_header=style_header,                                                
                                                                         style_cell=style_cell_mw,
                                                                         columns=[{'name': 'Overal Weight %', 'id': 'Overal Weight %'},
                                                                                  { 'name': 'Density', 'id': 'Density'},
                                                                                  { 'name': 'Price', 'id': 'Price',}], 
                                                                         data=[], fill_width=fill_width,
                                                                         
                                                                    )], ),
                                                         
                                              ],
                                              style={'color':'black',  'display': 'flex', 'width':'40%'} ),
                                         
                                         html.Div(
                                             id = 'table2',
                                             children = [html.Div([dt.DataTable( id = 'emc_table', 
                                                             style_as_list_view=style_as_list_view, 
                                                             style_header=style_header,
                                                             style_data=style_data,
                                                             style_cell=style_cell,
                                                             style_cell_conditional=style_cell_conditional,
                                                             columns=[], data=[], fill_width=fill_width, editable=True, row_deletable=True, 
                                                             dropdown_conditional=[{
                                                                 'if': {
                                                                     'column_id': 'overall composition',
                                                                     'filter_query': '{id} > 0'
                                                                       },
                                                                 'options': [
                                                                     {'label': i, 'value': i}
                                                                     for i in resin_uniq_name
                                                                 ]
                                                             },
                                                                 ]
                                                        )]),
                                                        html.Div([dt.DataTable( id = 'emc_table_w', 
                                                                         style_table=style_table_mw,
                                                                         style_as_list_view=style_as_list_view, 
                                                                         style_data=style_data,
                                                                         style_header=style_header,                                                
                                                                         style_cell=style_cell_mw,
                                                                         columns=[{'name': 'Overal Weight %', 'id': 'Overal Weight %'},
                                                                                  { 'name': 'Density', 'id': 'Density'},
                                                                                  { 'name': 'Price', 'id': 'Price',}], 
                                                                         data=[], fill_width=fill_width,
                                                                         
                                                                    )], ),
                                                         
                                              ],
                                              style={'color':'black',  'display': 'flex', 'width':'40%', 'marginLeft':'200px'} )
                                     ], style={'display':'flex'} ),
        
                                    
                                     html.Br(),
                                     html.Div( [
                                                 html.Div( [html.Div(id='ref_conv_bus_size', style=style_input_box_header),
                                                           dcc.Input(id='ref_conv_buis', type='number', value=1, style=style_input_box, step=0.5),
                                                           html.Div(id='ref_conv_sal_price', style=style_input_box_header),
                                                           dcc.Input(id='ref_conv_sales_pric', type='number', value=2000, style=style_input_box_long, step=100),
                                                           html.Div('sales price/raw material cost [%]', style=style_input_box_header),
                                                           html.Div(id='ratio_ref_sal', style=style_input_box_display),
                                                           html.Div('stock holding [days]', style=style_input_box_header),
                                                           dcc.Input(id='ref_holding_days', type='number', placeholder=90, style=style_input_box, step=10),
                                                           html.Div('Reference logistic cost', style=style_input_box_header),
                                                           dcc.Input(id='ref_log_cost', type='number', value=50, style=style_input_box, step=10),
                                                           ], style={ 'color':'blue',  'backgroundColor': 'yellow', 'width':'45%','textAlign':'left', 'display':'flex' }),
                                                 
                                                 html.Div( [html.Div(id='emc_conv_bus_size', style=style_input_box_header),
                                                           dcc.Input(id='emc_conv_buis', type='number', value=1, style=style_input_box, step=0.5),
                                                           html.Div('PRODUCTION CREDIT / DEBIT (REF = 100%) [%]', style=style_input_box_header),
                                                           html.Div(id='alt_emc_conv_bus_size', style=style_input_box_display),
                                                           html.Div(id='emc_thick_reduct', style=style_input_box_header),
                                                           html.Div(id='thickness_reduction', style=style_input_box_display),
                                                           html.Div('performance vs. reference [%]:', style=style_input_box_header),
                                                           dcc.Input(id='performance_reference', type='number', value=100, style=style_input_box_long, step=10),
                                                           html.Div(id='emc_conv_sal_price', style=style_input_box_header),
                                                           dcc.Input(id='emc_conv_sales_pric', type='number', value=2000, style=style_input_box_long, step=100),
                                                           ], style={ 'marginLeft':'100px', 'color':'blue', 'backgroundColor': 'yellow', 'width':'45%', 'textAlign':'left', 'display':'flex'}),
                                                 ], style={'display':'flex'}),
                                     
                                     html.Div( [
                                                 html.Div([
                                                             html.H1('Reference Raw Material Cost', style=style_result_head),
                                                             html.Div( [html.Div(id='USD_per_1000_sq_m', style=style_input_box_header),
                                                                        html.Div(id='ref_raw_cost_1', style=style_input_box_display),
                                                                        html.Div(id='KG_1000_sq_m', style=style_input_box_header),
                                                                        html.Div(id='ref_raw_cost_2', style=style_input_box_display),
                                                                        html.Div(id='USD_TON', style=style_input_box_header),
                                                                        html.Div(id='ref_raw_cost_3', style=style_input_box_display),
                                                                        html.Div('Overall Density [gr/cm^3]:', style=style_input_box_header),
                                                                        html.Div(id='ref_overall_density', style=style_input_box_display),
                                                                       ], style={'textAlign':'left',  'color':'blue', 'display':'flex'})
                                                             ],  style={'textAlign':'center',  'display':'inline-block', 'backgroundColor': 'yellow', 'width':'45%'}),
                                                 html.Div([
                                                             html.H1('EMC Raw Material Cost', style=style_result_head),
                                                             html.Div( [html.Div(id='emc_USD_per_1000_sq_m', style=style_input_box_header),
                                                                        html.Div(id='emc_raw_cost_1', style=style_input_box_display),
                                                                        html.Div(id='emc_KG_1000_sq_m', style=style_input_box_header),
                                                                        html.Div(id='emc_raw_cost_2', style=style_input_box_display),
                                                                        html.Div(id='emc_USD_TON', style=style_input_box_header),
                                                                        html.Div(id='emc_raw_cost_3', style=style_input_box_display),
                                                                        html.Div('Overall Density [gr/cm^3]:', style=style_input_box_header),
                                                                        html.Div(id='emc_overall_density', style=style_input_box_display),
                                                                       ], style={'textAlign':'left',  'color':'blue', 'display':'flex'})
                                                             ], style={'marginLeft':'100px', 'textAlign':'center',  'color':'blue', 'display':'inline-block', 'backgroundColor': 'yellow', 'width':'45%'}),
                                                 ], style={'display':'flex'} ),
                                     html.Br(),
                                     html.Br(),
                                     html.Div([
                                                html.Div([html.H1('realization for reference', style=style_result_head),
                                                          html.Div([html.Div(id='ref_sal_price_head1', style=style_input_box_header),
                                                                    html.Div(id='ref_sal_price_num1', style=style_input_box_display),
                                                                    html.Div(id='ref_sal_price_head2', style=style_input_box_header),
                                                                    html.Div(id='ref_sal_price_num2', style=style_input_box_display)],
                                                                    style={'textAlign':'left',  'color':'blue', 'display':'flex'})],
                                                         style={'textAlign':'center',  'display':'inline-block', 'backgroundColor': 'yellow', 'width':'32%'}),
                                                html.Div([html.H1('book-end realizations for alternative', style=style_result_head),],
                                                         style={'textAlign':'center',  'display':'inline-block', 'backgroundColor': 'yellow', 'width':'32%'}),
                                                html.Div([html.H1('realization for alternative at example price', style=style_result_head),],
                                                         style={'textAlign':'center',  'display':'inline-block', 'backgroundColor': 'yellow', 'width':'32%'}),
                                         
                                         ],    style={'display':'flex'}
                                         ),
                ],
                style={'textAlign':'center', 'color':'red', 'backgroundColor':'#DAE4E4'} 
            )

  # callback to update the ref
@app.callback(  [ Output('ref_table', 'data'),    Output('ref_table', 'columns')],
                [ Input( 'num_layer', 'value'),
                  Input( 'num_mat',  'value'),] )          
def update_table_ref_org(num_layer, num_resin):
      
    
    
      df= df_lultilayer(num_layer, num_resin)
      
      if 'id' not in df.columns:
          df['id'] = df.index
          mycolumns = [{'name': i, 'id': i, 'type': 'numeric'} for i in df.columns[0:-1]]
          mycolumns[0]= {'name': 'overall composition', 'id': 'overall composition', 'presentation': 'dropdown'}
         
      return df.to_dict("rows"), mycolumns


# callback to update table Refrence
@app.callback([Output('table_ref_ly_w', 'data'), Output('table_ref_ly_w', 'columns')], 
              Input('ref_table', 'data'))
def update_table_ref_lw(data):
    
    df_ref=pd.DataFrame(data)
    
    num_layer=len(df_ref.columns)-2
    
    columns_ref_lw=[{'name': 'layer'+ str(i+1)+' W [%]', 'id':'layer'+ str(i+1)+' W [%]' } for i in range(0,num_layer)]
    
    sum_ave=0
    
    for i in range(num_layer):
        df_ref.to_csv('df_ref.csv')
        sum_ave+=df_ref[df_ref.columns[i+1]].iloc[0]
        
    data_ref_lw={}
    for i in range(num_layer):
        data_ref_lw[columns_ref_lw[i]['id']]=[round((df_ref[df_ref.columns[i+1]].iloc[0]/sum_ave)*100,float_round)]
    
    df_ref_lw=pd.DataFrame(data_ref_lw)

    return df_ref_lw.to_dict('rows'), columns_ref_lw

# callback to update the ref overal weight
@app.callback(  Output('ref_table_w', 'data'),
                [ Input( 'ref_table', 'data'),
                  Input( 'table_ref_ly_w', 'data')] )
def update_table_ref_overall( data, data_w):
      
      df= pd.DataFrame(data)
      df_w= pd.DataFrame(data_w)

      
      cols_layers   = [c for c in df.columns if 'Layer' in c] # columns name with layer composition
      cols_layers_w = [c for c in df_w.columns ]
          
      dot = (df[cols_layers].iloc[1:] * df_w[cols_layers_w].values).sum(axis=1)
      out=pd.DataFrame({'Overal Weight %':dot})
      out['Overal Weight %']=out['Overal Weight %']/100
      out['Price']=0
      out['Density'] = 0.920
      
      for index, num_mat in enumerate(df['overall composition']):
          if num_mat=='Input Layer Ratios e.g. 1-2-1' or num_mat=='Resin name':
              continue
          
          out['Price'].iloc[index-1]=pe_price[num_mat]
          out['Density'].iloc[index-1] = 0.920
      return out.to_dict('rows')

#############################################################################################################
#############################################################################################################
  # callback to update the ref
@app.callback(  [ Output('emc_table', 'data'),    Output('emc_table', 'columns')],
                [ Input( 'num_layer_emc', 'value'),
                  Input( 'num_mat',  'value'),] )          
def update_table_emc_org(num_layer, num_resin):
      
    
      df= df_lultilayer(num_layer, num_resin)
      
      if 'id' not in df.columns:
          df['id'] = df.index
          mycolumns = [{'name': i, 'id': i, 'type': 'numeric'} for i in df.columns[0:-1]]
          mycolumns[0]= {'name': 'overall composition', 'id': 'overall composition', 'presentation': 'dropdown'}
         
      return df.to_dict("rows"), mycolumns


# callback to update table Refrence
@app.callback([Output('table_emc_ly_w', 'data'), Output('table_emc_ly_w', 'columns')], 
              Input('emc_table', 'data'))
def update_table_emc_lw(data):
    
    df_ref=pd.DataFrame(data)
    
    num_layer=len(df_ref.columns)-2
    
    columns_ref_lw=[{'name': 'layer'+ str(i+1)+' W [%]', 'id':'layer'+ str(i+1)+' W [%]' } for i in range(0,num_layer)]
    
    sum_ave=0
    
    for i in range(num_layer):
        df_ref.to_csv('df_ref.csv')
        sum_ave+=df_ref[df_ref.columns[i+1]].iloc[0]
        
    data_ref_lw={}
    for i in range(num_layer):
        data_ref_lw[columns_ref_lw[i]['id']]=[round((df_ref[df_ref.columns[i+1]].iloc[0]/sum_ave)*100,float_round)]
    
    df_ref_lw=pd.DataFrame(data_ref_lw)

    return df_ref_lw.to_dict('rows'), columns_ref_lw

# callback to update the ref overal weight
@app.callback(  Output('emc_table_w', 'data'),
                [ Input( 'emc_table', 'data'),
                  Input( 'table_emc_ly_w', 'data')] )
def update_table_emc_overall( data, data_w):
      
      df= pd.DataFrame(data)
      df_w= pd.DataFrame(data_w)

      
      cols_layers   = [c for c in df.columns if 'Layer' in c] # columns name with layer composition
      cols_layers_w = [c for c in df_w.columns ]
      
     
      dot = (df[cols_layers].iloc[1:] * df_w[cols_layers_w].values).sum(axis=1)
      out=pd.DataFrame({'Overal Weight %':dot})
      out['Overal Weight %']=out['Overal Weight %']/100
      out['Price']=0
      out['Density'] = 0.920
      
      for index, num_mat in enumerate(df['overall composition']):
          if num_mat=='Input Layer Ratios e.g. 1-2-1' or num_mat=='Resin name':
              continue
          
          out['Price'].iloc[index-1]=pe_price[num_mat]
          out['Density'].iloc[index-1] = 0.920
      return out.to_dict('rows')

####################################################################Update
#############################################################################   

@app.callback([Output('ref_raw_cost_1', 'children'), Output('ref_raw_cost_2', 'children'), 
               Output('ref_raw_cost_3', 'children'), Output('ref_overall_density', 'children'),
               Output('USD_per_1000_sq_m', 'children'), Output('KG_1000_sq_m', 'children'), Output('USD_TON', 'children'),
               Output('ref_conv_bus_size', 'children'), Output('ref_conv_sal_price', 'children'), Output('ratio_ref_sal', 'children')],
              [Input('ref_table', 'data'), Input('ref_table_w', 'data'),   Input('ref_thick', 'value'),
               Input('dimen', 'value'), Input('currency', 'value'), Input('w_unit', 'value'), Input('mix_unit', 'value'), 
               Input('ref_conv_sales_pric', 'value')])

def update_refrence_raw_cost(data, data_w, ref_thic, dimen, currency, wunit, mixunit, ref_conv_sales_pric ):
    
    df= pd.DataFrame(data)
    df_w= pd.DataFrame(data_w)
    
    overal_density=  round(sum (df_w['Overal Weight %']*df_w['Density'])/100,3)
    
    dol_per_dim, kg_per_sq_m, dol_per_ton, text1, text2= cost_calculation(df_w, ref_thic, overal_density, dimen, currency, wunit, mixunit )
    if wunit in ['KG', 'TON']:
        ref_b_size='KT'
    else:
        ref_b_size='MLB'
    
    ref_conv_bus_size= 'reference converter business size ' + '['+ref_b_size+']'
    ref_conv_sal_price='reference converter sales price ' + '['+currency+'/'+wunit+']'
    ratio_ref_sal= round(ref_conv_sales_pric/dol_per_ton,1)*100
    return dol_per_dim, kg_per_sq_m, dol_per_ton, overal_density, currency+' per 1000'+text1+':', text2+':', currency+'/'+wunit+':', ref_conv_bus_size,  ref_conv_sal_price, ratio_ref_sal 

@app.callback([Output('emc_raw_cost_1', 'children'), Output('emc_raw_cost_2', 'children'), 
               Output('emc_raw_cost_3', 'children'), Output('emc_overall_density', 'children'),
               Output('emc_USD_per_1000_sq_m', 'children'), Output('emc_KG_1000_sq_m', 'children'), Output('emc_USD_TON', 'children'),
               Output('emc_conv_bus_size', 'children'), Output('emc_thick_reduct', 'children'), 
               Output('alt_emc_conv_bus_size','children'), Output('thickness_reduction', 'children'), Output('emc_conv_sal_price', 'children')],
              [Input('emc_table', 'data'), Input('emc_table_w', 'data'),   Input('emc_thick', 'value'),
               Input('dimen', 'value'), Input('currency', 'value'), Input('w_unit', 'value'), Input('mix_unit', 'value'), 
               Input('ref_conv_buis', 'value'), Input('emc_conv_buis', 'value'), Input('ref_thick', 'value')])

def update_refrence_raw_cost(data, data_w, emc_thic, dimen, currency, wunit, mixunit,  ref_conv_buis, emc_conv_buis, ref_thic ):
    
    df= pd.DataFrame(data)
    df_w= pd.DataFrame(data_w)
    
    overal_density=  round(sum (df_w['Overal Weight %']*df_w['Density'])/100,3)
    
    dol_per_dim, kg_per_sq_m, dol_per_ton, text1, text2= cost_calculation(df_w, emc_thic, overal_density, dimen, currency, wunit, mixunit )
    if wunit in ['KG', 'TON']:
        emc_b_size='KT'
    else:
        emc_b_size='MLB'
    
    emc_conv_bus_size= 'EMC converter business size ' + '['+emc_b_size+']'
    emc_thick_reduct='thickness reduction vs. reference [%]:'
    
    alt_emc_conv_bus_size=round(emc_conv_buis/ref_conv_buis,1)*100 
    thick_reduction=round((ref_thic-emc_thic)/ref_thic,1)*100
    emc_conv_sal_price='EMC converter sales price ' + '['+currency+'/'+wunit+']'
    
    return dol_per_dim, kg_per_sq_m, dol_per_ton, overal_density, currency+' per 1000'+text1+':', text2+':', currency+'/'+wunit+':', emc_conv_bus_size, emc_thick_reduct,  alt_emc_conv_bus_size,thick_reduction, emc_conv_sal_price 
            
            
if __name__=='__main__':
    app.run_server(debug=True, use_reloader=False)
