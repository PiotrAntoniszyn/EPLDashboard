import time 
import requests
import json
import pandas as pd
import numpy as np
import os
import sys
from bs4 import BeautifulSoup, Comment
import lxml.html as lh
import streamlit as st
from datetime import datetime
from dateutil import relativedelta


@st.cache
def createDatabase(season):
    if season == 2020:
        url = 'https://fbref.com/en/comps/9/10728/stats/2020-2021-Premier-League-Stats'
        url2 = 'https://fbref.com/en/comps/9/10728/gca/2020-2021-Premier-League-Stats'
        url3 = 'https://fbref.com/en/comps/9/10728/shooting/2020-2021-Premier-League-Stats'
        url4 = 'https://fbref.com/en/comps/9/10728/passing/2020-2021-Premier-League-Stats'
    elif season == 2021:
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
    return main_df

@st.cache
def createTable(season):
    if season == 2020:
        url = 'https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats'
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        table = soup.find("table",{"id":"results107281_overall"})
    elif season == 2021:
        url = 'https://fbref.com/en/comps/9/Premier-League-Stats'
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        table = soup.find("table",{"id":"results111601_overall"})
    table = pd.read_html(table.prettify(),encoding='utf-8')
    table_df = pd.DataFrame(table[0])
    return table_df

@st.cache()
def createCalendar():
    # url = 'https://fantasy.premierleague.com/api/fixtures/'
    # soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    r=requests.get('https://fantasy.premierleague.com/api/fixtures/')
    calendar = r.json()
    cal_df = pd.DataFrame(calendar)
    t = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
    fpl_data = t.json()
    team_df = pd.DataFrame(fpl_data['teams'])
    team_df = team_df[['id','name','form','strength', 'strength_overall_home', 'strength_overall_away',
       'strength_attack_home', 'strength_attack_away', 'strength_defence_home',
       'strength_defence_away']]
    cal_df['team_a'] = cal_df['team_a'].replace(list(team_df['id']),list(team_df['name']))
    cal_df['team_h'] = cal_df['team_h'].replace(list(team_df['id']),list(team_df['name']))
    for x in range(len(cal_df)):
        cal_df['kickoff_time'][x] = cal_df['kickoff_time'][x][:10] + ' ' +cal_df['kickoff_time'][x][-9:-1]
    cal_df['kickoff_time'] = cal_df['kickoff_time'].astype('datetime64')
    cal_df = cal_df[['id','team_h','team_a','team_h_score','team_a_score','kickoff_time','stats']]

    return cal_df,team_df
