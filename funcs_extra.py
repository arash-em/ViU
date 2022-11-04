# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 10:45:12 2022

@author: asfard1
"""
import pandas as pd
#from difflib import SequenceMatcher

def df_lultilayer(num_layer, num_resin):
     
     data={'overall composition':[ 'Input Layer Ratios e.g. 1-2-1', 'Resin name']} 
     for i in range(num_layer):
         data['Layer'+str(i+1)+' composition']=[0,0]
         
     for i in range(num_resin-1):
         data['overall composition'].append('Resin name')
         
         for l in range(num_layer):
             data['Layer'+str(l+1)+' composition'].append(0)


     df=pd.DataFrame(data)
     
     
     return df # pandas dataframe
  
def update_table_ref_lw(df_ref):
    
    num_layer=len(df_ref.columns)-3

    sum_ave=0
    
    for i in range(num_layer):
        sum_ave+=df_ref[df_ref.columns[i+1]].iloc[1]
        
    for i in range(num_layer):
        df_ref['Layer'+str(i+1)+' composition'].iloc[0]=round((df_ref[df_ref.columns[i+1]].iloc[1]/sum_ave)*100,2)

    return df_ref    


def resin_uniq_name(df):
    Pe_list=['enable', 'exceed', 'exceedxp', 'exceeds', 'hta', 'ld', 'll'  ]
    Pe_dummy_price={'enable':1400, 'exceed':1300, 'exceedxp':1700, 'exceeds':1600, 'hta':1300, 'ld':1300, 'll':1200 }
    prod_list= df['Finished'].unique()
    pe_unique_global=set()
    pe_price={}
    
    for ch in prod_list:
        for ent in Pe_list:
            if ent in ch.lower():
                pe_unique_global.add(ent.upper()+ ch.replace(ent.upper(),' '))
                #pe_price[ent.upper()+ ch.replace(ent.upper(),' ')]= df['CGL5'][df['Finished']==ch].median()
                pe_price[ent.upper()+ ch.replace(ent.upper(),' ')]= Pe_dummy_price[ent]
    
    return pe_unique_global, pe_price
    
    

def density (pe_unique_global):
    
    UL_Prospector=pd.read_csv('Copy of ProspectorExport PE copolymer.csv', encoding = "ISO-8859-1")
    density_mat_uniq= UL_Prospector['Product'].unique()
    
    #def similar(a, b):
    #    return SequenceMatcher(None, a, b).ratio()

    density=[]
    for mat in  pe_unique_global:
        density.append(0.920)
    
    return density

def cost_calculation(df_w, ref_thic, overal_density, dimen, currency, wunit, mixunit ):
    
    unit=pd.read_csv('meta_data/units.csv')
    
    if wunit=='KG':
        unit['W. FACTOR']=1
        uu='KG or TON'
    elif wunit=='TON':
        unit['W. FACTOR']=0.001
        uu='KG or TON'
    else:
        unit['W. FACTOR']=1
        uu='LB'
        
    unit['UNIT COST']=unit['W. FACTOR'] * unit ['cal1']
    
    unit1= unit[unit['weight_unit']==uu]
    
    AK29= unit1[unit1['dimension']==dimen]['UNIT COST'].values 
    print(AK29[0])
    print(sum (df_w['Overal Weight %']*df_w['Price']/100))
    print(overal_density)
    print(ref_thic)
    if mixunit=='Mix by Weight':
        dol_per_dim=1000*AK29[0]*overal_density*ref_thic * sum (df_w['Overal Weight %']*df_w['Price']/100)
    else:
        dol_per_dim=1000*AK29[0]*ref_thic * sum (df_w['Overal Weight %']*df_w['Price']/100)
    
    
    BE= unit1[unit1['dimension']==dimen]['cal1'].values
    
    text1 = unit1[unit1['dimension']==dimen]['cal_unit2'].values
    text2 = unit1[unit1['dimension']==dimen]['cal_unit1'].values
    if dimen in ['liter', 'gallon']:
        kg_per_sq_m= overal_density*BE[0]*1000
    else:
        kg_per_sq_m= overal_density*ref_thic*BE[0]*1000
        
    dol_per_ton=  dol_per_dim /  kg_per_sq_m
    if wunit in ['KG', 'TON']:
        dol_per_ton=dol_per_ton*1000
        
    return round(dol_per_dim,2), round(kg_per_sq_m,2), round(dol_per_ton,2), text1[0], text2[0]
    
    