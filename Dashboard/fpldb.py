import time 
import requests
import json
import pandas as pd
import numpy as np
import os
import sys
from bs4 import BeautifulSoup, Comment
import lxml.html as lh

# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_absolute_error
# from sklearn.tree import DecisionTreeRegressor
# from sklearn.model_selection import train_test_split
def createFPLDB():
    url = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
    url2 = 'https://fbref.com/en/comps/9/gca/Premier-League-Stats'
    url3 = 'https://fbref.com/en/comps/9/shooting/Premier-League-Stats'
    url4 = 'https://fbref.com/en/comps/9/passing/Premier-League-Stats'
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    table = BeautifulSoup(soup.select_one('#all_stats_standard').find_next(text=lambda x: isinstance(x, Comment)), 'html.parser')
    soup2 = BeautifulSoup(requests.get(url2).content, 'html.parser')

    table2 = BeautifulSoup(soup2.select_one('#all_stats_gca').find_next(text=lambda x: isinstance(x, Comment)), 'html.parser')

    soup3 = BeautifulSoup(requests.get(url3).content, 'html.parser')

    table3 = BeautifulSoup(soup3.select_one('#all_stats_shooting').find_next(text=lambda x: isinstance(x, Comment)), 'html.parser')
    soup4 = BeautifulSoup(requests.get(url4).content, 'html.parser')

    table4 = BeautifulSoup(soup4.select_one('#all_stats_passing').find_next(text=lambda x: isinstance(x, Comment)), 'html.parser')

    tds=[]
    for tr in table.select('tr:has(td)'):
        tdx = [td.get_text(strip=True) for td in tr.select('td')]
        tds.append(tdx)
        #print('{:<30}{:<20}{:<10}'.format(tds[0], tds[3], tds[5]))
    tds2=[]
    for tr in table2.select('tr:has(td)'):
        tdx = [td.get_text(strip=True) for td in tr.select('td')]
        tds2.append(tdx)
        #print('{:<30}{:<20}{:<10}'.format(tds[0], tds[3], tds[5]))
    tds3=[]
    for tr in table3.select('tr:has(td)'):
        tdx = [td.get_text(strip=True) for td in tr.select('td')]
        tds3.append(tdx)
        #print('{:<30}{:<20}{:<10}'.format(tds[0], tds[3], tds[5]))
    tds4=[]
    for tr in table4.select('tr:has(td)'):
        tdx = [td.get_text(strip=True) for td in tr.select('td')]
        tds4.append(tdx)
        #print('{:<30}{:<20}{:<10}'.format(tds[0], tds[3], tds[5]))

    df = pd.DataFrame(tds)
    df2 = pd.DataFrame(tds2)
    df3 = pd.DataFrame(tds3)
    df4 = pd.DataFrame(tds4)

    legend = {0:'Player',1:'Nation',2:'Pos',3:'Squad',4:'Age',5:'Born',6:'MP',7:'Starts',8:'Min',9:'90s',10:'Goals',11:'Assists',12:'Non-penalty goals',13:'Penalty goals',14:'Penalty attempts',15:'Yellow cards',16:'Red cards',17:'Gls/90',18:'Ast/90',19:'G+A/90',20:'Non-penalty goals/90',21:'G+A-PK/90',22:'xG',23:'npxG',24:'xA',25:'npxG+xA',26:'xG/90',27:'xA/90',28:'xG+xA/90',29:'npxG/90',30:'npxG+xA/90',31:'Matches'}
    legend2 = {0:'Player',1:'Nation',2:'Pos',3:'Squad',4:'Age',5:'Born',6:'90s',7:'Shot Creating Actions',8:'SCA/90',15:'Goal Creating Actions',16:'GCA/90'}
    legend3 = {0:'Player',1:'Nation',2:'Pos',3:'Squad',4:'Age',5:'Born',6:'90s',8:'Shots',9:'Shots on target',10:'SoT%',11:'Sh/90',12:'SoT/90',13:'Goals/shot',14:'Goals/SoT',15:'Avg shot dist',16:'Free kicks made',21:'npxG/shot'}
    legend4 = {0:'Player',1:'Nation',2:'Pos',3:'Squad',4:'Age',5:'Born',6:'90s',7:'Completed passes',8:'Pass attempts',9:'Completed passes %',24:'Key Passes',25:'Final third passes',26:'Penalty area passes',27:'Crosses into penalty area',28:'Progressive passes'}


    df[df.columns[10:31]]=df[df.columns[10:31]].apply(pd.to_numeric, axis=1)
    df2[df2.columns[7:-1]]=df2[df2.columns[7:-1]].apply(pd.to_numeric, axis=1)
    df3[df3.columns[7:-1]]=df3[df3.columns[7:-1]].apply(pd.to_numeric, axis=1)
    df4[df4.columns[7:-1]]=df4[df4.columns[7:-1]].apply(pd.to_numeric, axis=1)


    df = df.rename(columns=dict(legend))
    df2 = df2.rename(columns=dict(legend2))
    df3 = df3.rename(columns=dict(legend3))
    df4 = df4.rename(columns=dict(legend4))
    df2 = df2.drop([9,10,11,12,13,14,17,18,19,20,21,22,23], axis=1)
    df3 = df3.drop([7,17,18,19,20,22,23,24], axis=1)
    df4 = df4.drop([10,11,12,13,14,15,16,17,18,19,20,21,22,23,29], axis=1)

    df['Min'] = df['Min'].str.replace(',', '').astype(float)

    main_df = pd.merge(df, df2, on=['Player','Nation','Pos','Squad','Age','Born','90s'],copy=False)
    main_df = pd.merge(main_df,df3, on=['Player','Nation','Pos','Squad','Age','Born','90s'],copy=False)
    main_df = pd.merge(main_df,df4, on=['Player','Nation','Pos','Squad','Age','Born','90s'],copy=False)

    main_df = main_df.drop(["Nation","Born","90s"],axis=1)



    r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
    fpl_data = r.json()

    element_data = pd.DataFrame(fpl_data['elements'])
    team_data = pd.DataFrame(fpl_data['teams'])
    elements_team = pd.merge(element_data, team_data, left_on='team', right_on='id')

    team_data['name'] = team_data['name'].replace(list(team_data['name']),list(main_df['Squad'].sort_values().unique()))

    element_data['team'] =element_data['team'].replace(list(team_data['id']),list(team_data['name']))


    fpl = elements_team.copy()


    df = pd.read_csv('Dashboard/ID_Dictionary.csv',encoding='cp1252').sort_values('FPL name',ascending=True)

    df = df[['fbref','fbref ID','FPL name','FPL ID','Team']]

    df.loc[249,'fbref'] = 'İlkay Gündoğan'
    df.loc[407,'fbref'] = 'Łukasz Fabiański'
    df.loc[480,'fbref'] = 'Asmir Begović'
    df.loc[566,'fbref'] = 'Filip Benković'
    df.loc[94,'fbref'] = 'Halil Dervişoğlu'
    df.loc[92,'fbref'] = 'Jan Žambůrek'
    df.loc[157,'fbref'] = 'Jarosław Jach'
    df.loc[151,'fbref'] = 'Luka Milivojević'
    df.loc[110,'fbref'] = 'Matěj Vydra'
    df.loc[124,'fbref'] = 'Mateo Kovačić'
    df.loc[548,'fbref'] = 'Michał Karbownik'
    df.loc[270,'fbref'] = 'Nemanja Matić'
    df.loc[421,'fbref'] = 'Tomáš Souček'
    df.loc[216,'fbref'] = 'Çağlar Söyüncü'
    df.loc[327,'fbref'] = 'Przemysław Płacheta'


    fpl['fbref name'] = fpl['id_x'].replace(list(df['FPL ID']),list(df['fbref']))

    fpl_main = main_df[['Player','Starts','MP','Min','Squad','Goals',
           'Assists', 'Penalty attempts',
           'Yellow cards', 'Red cards', 'Gls/90', 'Ast/90', 'G+A/90', 'xG', 'npxG', 'xA', 'npxG+xA',
           'xG/90', 'xA/90', 'xG+xA/90', 'npxG/90', 'npxG+xA/90',
           'Shot Creating Actions', 'SCA/90', 'Goal Creating Actions', 'GCA/90',
           'Shots', 'Shots on target', 'SoT%', 'Sh/90', 'SoT/90', 'Goals/shot',
           'Goals/SoT', 'npxG/shot','Key Passes',
           'Final third passes', 'Penalty area passes',
           'Crosses into penalty area']]

    ##big = pd.merge(fpl,main,left_on=['first_name','team'],right_on=['first_name','Squad'])
    big = pd.merge(fpl_main,fpl,left_on=['Player'],right_on=['fbref name'])
    #są różnice w nazewnictwie piłkarzy, więc ok. 60 się nie merguje -NAPRAWIONE
    return big