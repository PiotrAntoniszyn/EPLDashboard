
import asyncio
import aiohttp
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch, add_image, PyPizza, FontManager, Radar
import json
import requests
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.lines as mlines
from highlight_text import fig_text
import ipywidgets as widgets
from PIL import Image
import os
import html5lib
from understat import Understat
import streamlit as st
import time
import fpldb as fpldb
import playerdb as pdb
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from highlight_text import fig_text
from matplotlib import patches as mpatches
from matplotlib import colors
from matplotlib import font_manager
from datetime import datetime
from dateutil import relativedelta

fm_rubik = FontManager()


font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))
URL1 = ('https://github.com/googlefonts/SourceSerifProGFVersion/blob/main/'
        'fonts/SourceSerifPro-Regular.ttf?raw=true')
serif_regular = FontManager(URL1)
URL2 = ('https://github.com/googlefonts/SourceSerifProGFVersion/blob/main/'
        'fonts/SourceSerifPro-ExtraLight.ttf?raw=true')
serif_extra_light = FontManager(URL2)
URL3 = ('https://github.com/google/fonts/blob/main/ofl/rubikmonoone/'
        'RubikMonoOne-Regular.ttf?raw=true')
rubik_regular = FontManager(URL3)
URL4 = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Thin.ttf?raw=true'
robotto_thin = FontManager(URL4)
URL5 = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Regular.ttf?raw=true'
robotto_regular = FontManager(URL5)
URL6 = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Bold.ttf?raw=true'
robotto_bold = FontManager(URL6)


edge_team_colors = {'Arsenal':'#063672', 'Aston Villa':'#670E36', 'Bournemouth':'#da291c','Brentford':'#FFFFFF',  'Brighton':'#FFFFFF',
               'Burnley':'#99D6EA', 'Chelsea':'#D1D3D4', 'Crystal Palace':'#C4122E', 'Everton':'#FFFFFF', "Fulham": "#FFFFFF",
               'Leicester City': '#FDBE11', "Leeds United": "#FFCD00", 'Liverpool':'#00B2A9', 'Manchester City':'#1C2C5B', 'Manchester Utd':'#FBE122',
               'Newcastle':'#F1BE48', 'Norwich City':'#00A650', 'Sheffield Utd':'#0D171A', 
               'Southampton':'#130C0E', 'Tottenham':'#FFFFFF', 'Watford':'#ED2127', "West Brom": '#FFFFFF', 'West Ham':'#1BB1E7',
               'Wolves':'#231F20'}

team_colors = {'Arsenal':'#ef0107', 'Aston Villa':'#95bfe5', 'Bournemouth':'#000000','Brentford':'#D60019', 'Brighton':'#0057b8',
               'Burnley':'#6c1d45', 'Chelsea':'#034694', 'Crystal Palace':'#1b458f', 'Everton':'#003399', "Fulham": "#000000",
               'Leicester City':'#003090', "Leeds United": "#1D428A", 'Liverpool':'#c8102e', 'Manchester City':'#6cabdd', 'Manchester Utd':'#da291c',
               'Newcastle Utd':'#241f20', 'Norwich City':'#fff200', 'Sheffield Utd':'#ee2737', 
               'Southampton':'#d71920', 'Tottenham':'#132257', 'Watford':'#fbee23', "West Brom": '#122F67', 'West Ham':'#7a263a',
               'Wolves':'#fdb913'}

#######################

st.set_page_config(
 page_title="EPL Team Dashboard",
 page_icon=":trophy:",
 layout="wide",
 initial_sidebar_state="auto",
)


@st.cache
def prepare(season):
  if season == 2020:
    url = 'https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats'
  elif season == 2021:
    url = 'https://fbref.com/en/comps/9/Premier-League-Stats'
  soup = BeautifulSoup(requests.get(url).content, 'html.parser')


  gkping = soup.find( "table",{"id":"stats_squads_keeper_for"})
  shooting = soup.find( "table",{"id":"stats_squads_shooting_for"})
  passing = soup.find( "table",{"id":"stats_squads_passing_for"})
  gca = soup.find( "table",{"id":"stats_squads_gca_for"})
  defending = soup.find( "table",{"id":"stats_squads_defense_for"})
  possession = soup.find( "table",{"id":"stats_squads_possession_for"})
  main = [gkping,shooting,passing,gca,defending,possession]

  gkping = pd.read_html(gkping.prettify(),encoding='utf-8')
  gkping = pd.DataFrame(gkping[0])

  shooting = pd.read_html(shooting.prettify(),encoding='utf-8')
  shooting = pd.DataFrame(shooting[0])

  passing = pd.read_html(passing.prettify(),encoding='utf-8')
  passing = pd.DataFrame(passing[0])

  gca = pd.read_html(gca.prettify(),encoding='utf-8')
  gca = pd.DataFrame(gca[0])

  defending = pd.read_html(defending.prettify(),encoding='utf-8')
  defending = pd.DataFrame(defending[0])

  possession = pd.read_html(possession.prettify(),encoding='utf-8')
  possession = pd.DataFrame(possession[0])

  main = [gkping,shooting,passing,gca,defending,possession]
  for x in main:
      x.columns = x.columns.droplevel(0)

  possession = possession.iloc[:, :-1]

  gkping = gkping[['Squad','GA','CS']]
  shooting = shooting[['Squad', 'SoT/90','npxG']]
  passing = passing[['Squad','1/3','Prog']]
  gca = gca[['Squad','GCA90']]
  defending = defending[['Squad','TklW','Int']]
  possession = possession[['Squad','Poss','Succ','Prog']]

  possession = possession.rename(columns={"Prog": "ProgCarries"})
  passing = passing.rename(columns={"Prog":"ProgPasses"})

  main = pd.merge(gkping,shooting,on='Squad')
  main = pd.merge(main,passing,on='Squad')
  main = pd.merge(main,gca,on='Squad')
  main = pd.merge(main,defending,on='Squad')
  main = pd.merge(main,possession,on='Squad')
  # values2 = []
  # for x in main.columns[1:]:
  #     values2.append(main[x].mean().round(1))
  # In[75]:
  main = main.rename(columns={"Succ": "Successful Dribbles","ProgCarries": "Progressive Carries","ProgPasses": "Progressive Passes","TklW": "Tackles Won","Poss": "Possesion[%]","Int": "Interceptions","1/3": "Passes into final third"})
  return main

#######################

def radar_mosaic(radar_height=0.915, title_height=0.06, figheight=14):
    """ Create a Radar chart flanked by a title and endnote axes.

    Parameters
    ----------
    radar_height: float, default 0.915
        The height of the radar axes in fractions of the figure height (default 91.5%).
    title_height: float, default 0.06
        The height of the title axes in fractions of the figure height (default 6%).
    figheight: float, default 14
        The figure height in inches.

    Returns
    -------
    fig : matplotlib.figure.Figure
    axs : dict[label, Axes]
    """
    if title_height + radar_height > 1:
        error_msg = 'Reduce one of the radar_height or title_height so the total is ≤ 1.'
        raise ValueError(error_msg)
    endnote_height = 1 - title_height - radar_height
    figwidth = figheight * radar_height
    figure, axes = plt.subplot_mosaic([['title'], ['radar'], ['endnote']],
                                      gridspec_kw={'height_ratios': [title_height, radar_height,
                                                                     endnote_height],
                                                   # the grid takes up the whole of the figure 0-1
                                                   'bottom': 0, 'left': 0, 'top': 1,
                                                   'right': 1, 'hspace': 0},
                                      figsize=(figwidth, figheight))
    axes['title'].axis('off')
    axes['endnote'].axis('off')
    return figure, axes

def show_next_five(calendar, selected_club):
  next_five = []
  tmp = calendar[calendar['kickoff_time'] > datetime.now()-relativedelta.relativedelta(hours=2)]

  for x in range(len(tmp)):
      if tmp.iloc[x]['team_a'] == selected_club:
          next_five.append(tmp.iloc[x]['team_h']+ '(A)')

      elif tmp.iloc[x]['team_h'] == selected_club: 
          next_five.append(tmp.iloc[x]['team_a'] + '(H)')

      if len(next_five)==5:
          break

  return next_five


def fixStrength(next_five):
    strength = 0
    for x in next_five:
        y=x[:-3]
        strength += int(team_form_temp[team_form_temp['name']==y]['strength'])
    if strength > 20:
      return '{}/25 - Very Hard'.format(strength)
    elif strength >17:
      return '{}/25 - Hard'.format(strength)
    elif strength >14:
      return '{}/25 - Moderate'.format(strength)
    elif strength >11:
      return '{}/25 - Easy'.format(strength)
    else:
      return '{}/25 - Very Easy'.format(strength)


def expPoints(opp,player,player_team):
  team = opp[:-3]
  h_a =opp[-3:]  
  if h_a == '(H)':
    str_attack = (team_form_temp.iloc[team_form_temp[team_form_temp['name']==player_team].index[0]]['strength_attack_home'] - team_form_temp[team_form_temp['name']==team]['strength_defence_away'])*0.01
    strength = 1 - team_form_temp[team_form_temp['name']==team]['strength_attack_away']/2000
  else:
    str_attack = (team_form_temp.iloc[team_form_temp[team_form_temp['name']==player_team].index[0]]['strength_attack_away'] - team_form_temp[team_form_temp['name']==team]['strength_defence_home'])*0.01
    strength = 1 - team_form_temp[team_form_temp['name']==team]['strength_attack_home']/2000
   
  cats = ['xA/90','xG/90','yellow_cards','red_cards','bonus','minutes','element_type']

  tmp = playerdb.iloc[playerdb[playerdb['Player'].str.contains(player)==True].index[0]][cats]
  pos = {'1':[3,6,4],'2':[3,6,4],'3':[3,5,1],'4':[3,4,0]}
  xmin = minutes.iloc[minutes[minutes['Player'].str.contains(player)==True].index[0]]['xMin']
  mins = minutes.iloc[minutes[minutes['Player'].str.contains(player)==True].index[0]]['Min']
  if xmin>=60:
    xP = tmp[0] * pos[str(tmp[-1])][0] * (xmin/90) * str_attack + tmp[1] * pos[str(tmp[-1])][1] * (xmin/90) * str_attack + tmp[2]/tmp[-2] - tmp[3]/tmp[-2] + tmp[4]/(tmp[-2]/90)+ pos[str(tmp[-1])][2] * strength + 1 
  else:
    xP = tmp[0] * pos[str(tmp[-1])][0] * (xmin/90) * str_attack  + tmp[1] * pos[str(tmp[-1])][1] * (xmin/90)* str_attack  + tmp[2]/tmp[-2] - tmp[3]/tmp[-2] + tmp[4]/(tmp[-2]/90)
  return round(xP,2)

def exp_five(next_five,player,team):
  exp = []
  for x in next_five:
    exp.append(float(expPoints(x,player,team)))
  return exp

#######################

# st.title("Premier League Team Dashboard | Season {}/{} ".format(season,season+1))

#######################

# playerdb = pdb.createDatabase(season)

# leaguetable = pdb.createTable(season)

# main = prepare(season)

#######################

calendar,team_form = pdb.createCalendar()


st.sidebar.header("App Menu")

with st.sidebar.expander("Page Selection"):
  page = st.selectbox("",options=['Team Performance Dashboard','FPL Player Comparison', 'Top 10 in xP'])


if page == 'Team Performance Dashboard':
  with st.sidebar.expander("Season"):
    season = st.selectbox("",options=[2021,2020])
  st.title("Premier League Team Dashboard | Season {}/{} ".format(season,season+1))

  col1, col2, col3 = st.columns([1.3,2,2])

  playerdb = pdb.createDatabase(season)

  leaguetable = pdb.createTable(season)

  

  main = prepare(season)
  #######################

  st.sidebar.header("Dashboard Settings")

  

  with st.sidebar.expander("Club"):
    selected_club = st.selectbox("",options=list(main['Squad'].sort_values(ascending=True)))

  with st.sidebar.expander("View Mode"):
    mode = st.radio("", ("Percentile","Stats"))

    # bar=st.progress(0)
    # time.sleep(0.01)
    # for x in range(100):
    #   time.sleep(.001)
    #   bar.progress(x+1)ó

  st.sidebar.header("Player Comparison Settings")

  with st.sidebar.expander("Metrics"):
    categories = st.multiselect('',list(playerdb.columns[10:]),['xG','xA','Shot Creating Actions','Shots','Shots on target','Key Passes','Crosses into penalty area','Final third passes'])

  with st.sidebar.expander("Players"):
    player1 = st.selectbox("Player 1:",options=list(playerdb[playerdb['Squad']==selected_club]['Player'].sort_values(ascending=True)),index=0)
    player2 = st.selectbox("Player 2:",options=list(playerdb[playerdb['Squad']==selected_club]['Player'].sort_values(ascending=True)),index=1)

  #######################




  image = Image.open('Dashboard/PL_Logos/{}.png'.format(selected_club))

  with st.expander("Browse squad data"):
    st.dataframe(playerdb[playerdb['Squad']==selected_club].reset_index(drop=True))

  with st.sidebar.expander("Scatter Plot Settings"):
    cat1 = st.selectbox('X',options=list(playerdb.columns[10:]),index=9)
    cat2 = st.selectbox('Y',options=list(playerdb.columns[10:]),index=11)

  with col1:
    with st.container():
      st.image(image, width=80)
      st.text("Rank: {} - {} pts".format(leaguetable[leaguetable['Squad']==selected_club]['Rk'].reset_index(drop=True)[0],leaguetable[leaguetable['Squad']==selected_club]['Pts'].reset_index(drop=True)[0]))
      st.text(" {} - {} - {}".format(leaguetable[leaguetable['Squad']==selected_club]['W'].reset_index(drop=True)[0],leaguetable[leaguetable['Squad']==selected_club]['D'].reset_index(drop=True)[0],leaguetable[leaguetable['Squad']==selected_club]['L'].reset_index(drop=True)[0]))
      #st.text("Last 5 matches: {}".format(leaguetable[leaguetable['Squad']==selected_club]['Last 5'].reset_index(drop=True)[0]))
      st.text("Top scorer(s):\n{}".format(leaguetable[leaguetable['Squad']==selected_club]['Top Team Scorer'].reset_index(drop=True)[0]))

  #######################

  if mode == 'Percentile':
    values = []
    values.append(int(main["GA"].rank(ascending=False,pct=True)[main["Squad"]==selected_club].iloc[0]*100))
    for x in main.columns[2:]:
        values.append(int(main[x].rank(ascending=True,pct=True)[main["Squad"]==selected_club].iloc[0]*100))
    max_range = []
    for x in main.columns[1:]:
        max_range.append(100)
    min_range = []
    for x in main.columns[1:]:
        min_range.append(0)
    low = []
    high = []
    for x in categories:
      low.append(0)
      high.append(100)
    pvalues1 = []
    pvalues2 = []
    for x in categories:
      pvalues1.append(playerdb[x].rank(pct=True).iloc[playerdb[playerdb['Player'].str.contains(player1)==True].index].reset_index(drop=True)[0]*100)
      pvalues2.append(playerdb[x].rank(pct=True).iloc[playerdb[playerdb['Player'].str.contains(player2)==True].index].reset_index(drop=True)[0]*100)

  else:

    values = []
    for x in main.columns[1:]:
        values.append(main[main["Squad"]==selected_club].iloc[0][x])
    max_range = []
    for x in main.columns[1:]:
        max_range.append(main[x].max())
    min_range = []
    for x in main.columns[1:]:
        min_range.append(main[x].min())
    low = []
    high = []
    for x in categories:
      if max(playerdb['Min'])<300:
        low.append(min(playerdb[x]))
        high.append(max(playerdb[x]))
      else:
        low.append(min(playerdb[playerdb['Min']>300][x]))
        high.append(max(playerdb[playerdb['Min']>300][x]))
    pvalues1 = playerdb.iloc[playerdb[playerdb['Player'].str.contains(player1)==True].index[0]][categories]
    pvalues2 = playerdb.iloc[playerdb[playerdb['Player'].str.contains(player2)==True].index[0]][categories]

  #######################

  params = main.columns[1:]
  baker = PyPizza(
      params=params,                  # list of parameters
      background_color='#0E1117',
      last_circle_color='#FFFFFF',
      other_circle_color='#FFFFFF',
      min_range=min_range,
      max_range=max_range,
      straight_line_color="#FFFFFF",  # color for straight lines
      straight_line_lw=1,             # linewidth for straight lines
      last_circle_lw=6,               # linewidth of last circle
      other_circle_lw=1,              # linewidth for other circles
      other_circle_ls="-."            # linestyle for other circles
  )
       
  fig, axs = baker.make_pizza(
      values,
      figsize=(8, 8),      # adjust figsize according to your need
      param_location=110,  # where the parameters will be added
      kwargs_slices=dict(
          facecolor=team_colors[selected_club], edgecolor="#FFFFFF",
          zorder=2, linewidth=1
      ), 
      kwargs_compare=dict(
          facecolor="#BEBEBE", edgecolor="#222222",alpha=1, zorder=3, linewidth=1,
      ), # values to be used when plotting slices
      kwargs_params=dict(
          color="#FFFFFF", fontsize=12,
          fontproperties=font_normal.prop, va="center"
      ),                   # values to be used when adding parameter
      kwargs_values=dict(
          color="#FFFFFF", fontsize=12,
          fontproperties=font_normal.prop, zorder=4,
          bbox=dict(
              edgecolor="#FFFFFF", facecolor=team_colors[selected_club], alpha=.8,
              boxstyle="round,pad=0.2", lw=1
          )
      ),
      kwargs_compare_values=dict(
          color="#000000", fontsize=12,
          fontproperties=font_normal.prop, zorder=3,
          bbox=dict(
              edgecolor="#000000", facecolor="#BEBEBE", alpha=0.75,
              boxstyle="round,pad=0.2", lw=1
          )
      )     # values to be used when adding parameter-values
  )

  #######################

  with col2:

    with st.spinner("Loading..."):
      st.subheader("Team Performance")
      st.pyplot(fig)



  # st.image('PL_Logos\{}.png'.format(selected_club))
  radar = Radar(categories, low, high,
                # whether to round any of the labels to integers instead of decimal places
                round_int=[True]*len(categories),
                num_rings=4,  # the number of concentric circles (excluding center circle)
                # if the ring_width is more than the center_circle_radius then
                # the center circle radius will be wider than the width of the concentric circles
                ring_width=1, center_circle_radius=1)

  # creating the figure using the function defined above:
  fig1, axs = radar_mosaic(radar_height=0.915, title_height=0.06, figheight=14)

  # plot the radar
  radar.setup_axis(ax=axs['radar'], facecolor='None', dpi=500)
  rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#28252c', edgecolor='#39353f', lw=1.5)
  radar_output = radar.draw_radar_compare(pvalues1, pvalues2, ax=axs['radar'],kwargs_radar={'facecolor': '#00f2c1', 'alpha': 0.6},
                                          kwargs_compare={'facecolor': '#d80499', 'alpha': 0.6})                                
  radar_poly, radar_poly2, vertices1, vertices2 = radar_output
  range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25, color='#fcfcfc',
                                         fontproperties=robotto_thin.prop)
  param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25, color='#fcfcfc',
                                         fontproperties=robotto_regular.prop)
  axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
                       c='#00f2c1', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)
  axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
                       c='#d80499', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)

  title1_text = axs['title'].text(0.01, 0.65, '{}'.format(player1), fontsize=28, color='#01c49d',
                                  fontproperties=robotto_bold.prop, ha='left', va='center')
  title2_text = axs['title'].text(0.99, 0.65, '{}'.format(player2), fontsize=28,
                                  fontproperties=robotto_bold.prop,
                                  ha='right', va='center', color='#d80499')

  fig1.set_facecolor('#0E1117')

  #######################

  with col3:
    with st.spinner("Loading..."):
      st.subheader("Player Radar comparison")
      st.pyplot(fig1)

  #######################

  col21, col22 = st.columns(2)

  #######################

  fig2 = px.scatter(playerdb, x=playerdb[cat1], y=playerdb[cat2],title='Scatter Plot {} / {}'.format(cat1,cat2), template="simple_white", hover_data=['Player'],labels={
                       "x": cat1,
                       "y": cat2 
                   })

  marker_color = np.where(playerdb['Squad'] == selected_club , team_colors[selected_club] , 'black')
  fig2.update_traces(
                    marker = dict(color=marker_color),
                    opacity = .8,
                    )

  #######################

  fig3 = go.Figure(go.Bar(
            x=[sum(playerdb[playerdb['Squad']==selected_club][playerdb['Pos'].str[:2]=='DF']['Goals']), sum(playerdb[playerdb['Squad']==selected_club][playerdb['Pos'].str[:2]=='MF']['Goals']), sum(playerdb[playerdb['Squad']==selected_club][playerdb['Pos'].str[:2]=='FW']['Goals'])],
            y=['DF', 'MF', 'FW'],
            marker=dict(color=team_colors[selected_club]),
            opacity=.7,
            orientation='h'))
  fig3.update_layout(
      title='Goals via position',
      yaxis=dict(
          showgrid=False,
          showline=False,
          showticklabels=True,
          domain=[0, 1],
      )
    )

  #######################

  with col21:

    st.plotly_chart(fig2, use_container_width=True)

  with col22:
    
    st.plotly_chart(fig3, use_container_width=True)

elif page == 'FPL Player Comparison':
  season = 2021
  playerdb = fpldb.createFPLDB()

  leaguetable = pdb.createTable(season)

  main = prepare(season)
  team_form_temp = team_form.copy()
  calendar_temp = calendar.copy()
  team_form_temp['name'] = main['Squad'].copy()
  calendar_temp['team_a'] = calendar_temp['team_a'].replace(list(calendar_temp['team_a'].sort_values().unique()),list(main['Squad']))
  calendar_temp['team_h'] = calendar_temp['team_h'].replace(list(calendar_temp['team_h'].sort_values().unique()),list(main['Squad']))
  fixes = pd.read_csv('fixes.csv').drop('Unnamed: 0',axis=1)
  fixes = fixes.set_index('name')

  minutes = playerdb[['Min','Starts','chance_of_playing_this_round','chance_of_playing_next_round']].astype('float64').fillna(100.0)
  minutes['Player'] = playerdb['Player'].copy()
  minutes['xMin'] = (minutes['Starts']/max(minutes['Starts'])*minutes['Min']/max(minutes['Starts'])*0.95)*minutes['chance_of_playing_this_round']/100


  st.sidebar.header("Comparison Tools")

  with st.sidebar.expander("Metrics"):
    categories = st.multiselect('',list(playerdb.columns[10:]),['xG','xA','Shot Creating Actions','Shots','Shots on target','Key Passes','Crosses into penalty area','Final third passes'])


  
# values = []
#     for x in main.columns[1:]:
#         values.append(main[main["Squad"]==selected_club].iloc[0][x])
  # max_range = []
  # for x in main.columns[1:]:
  #     max_range.append(main[x].max())
  # min_range = []
  # for x in main.columns[1:]:
  #     min_range.append(main[x].min())
  # low = []
  # high = []
  # for x in categories:
  #   if max(playerdb['Min'])<300:
  #     low.append(min(playerdb[x]))
  #     high.append(max(playerdb[x]))
  #   else:
  #     low.append(min(playerdb[playerdb['Min']>300][x]))
  #     high.append(max(playerdb[playerdb['Min']>300][x]))
  # pvalues1 = playerdb.iloc[playerdb[playerdb['Player'].str.contains(player1)==True].index[0]][categories]
  # pvalues2 = playerdb.iloc[playerdb[playerdb['Player'].str.contains(player2)==True].index[0]][categories]
    



  # radar = Radar(categories, low, high,
  #             # whether to round any of the labels to integers instead of decimal places
  #             round_int=[True]*len(categories),
  #             num_rings=4,  # the number of concentric circles (excluding center circle)
  #             # if the ring_width is more than the center_circle_radius then
  #             # the center circle radius will be wider than the width of the concentric circles
  #             ring_width=1, center_circle_radius=1)

  # # creating the figure using the function defined above:
  # fig1, axs = radar_mosaic(radar_height=0.915, title_height=0.06, figheight=14)

  # # plot the radar
  # radar.setup_axis(ax=axs['radar'], facecolor='None', dpi=500)
  # rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#28252c', edgecolor='#39353f', lw=1.5)
  # radar_output = radar.draw_radar_compare(pvalues1, pvalues2, ax=axs['radar'],kwargs_radar={'facecolor': '#00f2c1', 'alpha': 0.6},
  #                                         kwargs_compare={'facecolor': '#d80499', 'alpha': 0.6})                                
  # radar_poly, radar_poly2, vertices1, vertices2 = radar_output
  # range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25, color='#fcfcfc',
  #                                        fontproperties=robotto_thin.prop)
  # param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25, color='#fcfcfc',
  #                                        fontproperties=robotto_regular.prop)
  # axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
  #                      c='#00f2c1', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)
  # axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
  #                      c='#d80499', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)

  # title1_text = axs['title'].text(0.01, 0.65, '{}'.format(player1), fontsize=28, color='#01c49d',
  #                                 fontproperties=robotto_bold.prop, ha='left', va='center')
  # title2_text = axs['title'].text(0.99, 0.65, '{}'.format(player2), fontsize=28,
  #                                 fontproperties=robotto_bold.prop,
  #                                 ha='right', va='center', color='#d80499')
  # subtitle1_text = axs['title'].text(0.01, 0.2, '{}'.format(selected_club1), fontsize=20, color='#01c49d',
  #                                 fontproperties=robotto_bold.prop, ha='left', va='center')
  # subtitle2_text = axs['title'].text(0.99, 0.2, '{}'.format(selected_club2), fontsize=20,
  #                                 fontproperties=robotto_bold.prop,
  #                                 ha='right', va='center', color='#d80499')


  # fig1.set_facecolor('#0E1117')

  # col1, col2, col3 = st.columns([1,2,1])


  # with col2:
  #   with st.spinner("Loading..."):
  #     st.subheader("Player Radar comparison")
  #     st.pyplot(fig1)
  # with col1:
  #   st.header("Next 5 matches")
  #   st.subheader(selected_club1)
  #   st.subheader("{} - {} - {} - {} - {}".format(fixes.loc[selected_club1][0],fixes.loc[selected_club1][1],fixes.loc[selected_club1][2],fixes.loc[selected_club1][3],fixes.loc[selected_club1][4]))
  #   st.subheader(selected_club2)
  #   st.subheader("{} - {} - {} - {} - {}".format(fixes.loc[selected_club2][0],fixes.loc[selected_club2][1],fixes.loc[selected_club2][2],fixes.loc[selected_club2][3],fixes.loc[selected_club2][4]))

  st.header("Percentile stats comparison")

  col21, col22= st.columns([2,2])

  with col21:
    selected_club1 = st.selectbox("Club 1:",options=list(main['Squad'].sort_values(ascending=True)))

    player1 = st.selectbox("Player 1:",options=list(playerdb[playerdb['Squad']==selected_club1]['Player'].sort_values(ascending=True)),index=0)
    #st.subheader("{} - {} - {} - {} - {}".format(fixes.loc[selected_club1][0],fixes.loc[selected_club1][1],fixes.loc[selected_club1][2],fixes.loc[selected_club1][3],fixes.loc[selected_club1][4]))
    
  with col22:
    selected_club2 = st.selectbox("Club 2:",options=list(main['Squad'].sort_values(ascending=True)),index=1)

    player2 = st.selectbox("Player 2:",options=list(playerdb[playerdb['Squad']==selected_club2]['Player'].sort_values(ascending=True)),index=0)
    #st.subheader("{} - {} - {} - {} - {}".format(fixes.loc[selected_club2][0],fixes.loc[selected_club2][1],fixes.loc[selected_club2][2],fixes.loc[selected_club2][3],fixes.loc[selected_club2][4]))


  max_range = []
  for x in main.columns[1:]:
      max_range.append(100)
  min_range = []
  for x in main.columns[1:]:
      min_range.append(0)
  low = []
  high = []
  for x in categories:
    low.append(0)
    high.append(100)
  pvalues1 = []
  pvalues2 = []
  for x in categories:
    pvalues1.append(round(playerdb[x].rank(pct=True).iloc[playerdb[playerdb['Player'].str.contains(player1)==True].index].reset_index(drop=True)[0]*100))
    pvalues2.append(round(playerdb[x].rank(pct=True).iloc[playerdb[playerdb['Player'].str.contains(player2)==True].index].reset_index(drop=True)[0]*100))

  fig = go.Figure()
  fig.update_layout(
    #title_text=player1
  )
  fig.add_trace(go.Bar(
    y=categories,
    x=pvalues1,
    orientation='h',
    marker=dict(
        color=team_colors[selected_club1],
        line=dict(color=team_colors[selected_club1], width=3)
    )
  ))
  fig.update_xaxes(range=[0,100])
  fig2 = go.Figure()
  fig2.update_xaxes(range=[0,100])
  fig2.add_trace(go.Bar(
    y=categories,
    x=pvalues2,
    orientation='h',
    marker=dict(
        color=team_colors[selected_club2],
        line=dict(color=team_colors[selected_club2], width=3)
    )
  ))
  fig2.update_layout(
    #title_text=player2
    )  

  with col21:
    st.plotly_chart(fig,use_container_width=True)
    st.subheader('Next five matches')
    team = playerdb.iloc[playerdb[playerdb['Player']==player1].index[0]]['Squad']
    next_five1 = show_next_five(calendar_temp,selected_club1)
    fixStr1 = fixStrength(next_five1)
    exp1 = exp_five(next_five1,player1,team)
    st.write(' - '.join(map(str, show_next_five(calendar_temp,selected_club1))))
    st.write(' - '.join(map(str, exp1)))
    st.write("xPoints: {:.2f}".format(round(sum(exp1), 2)))


    st.write('Fixture difficulty: '+ fixStr1)

  with col22:
    st.plotly_chart(fig2,use_container_width=True)
    st.subheader('Next five matches')
    team = playerdb.iloc[playerdb[playerdb['Player']==player2].index[0]]['Squad']
    next_five2 = show_next_five(calendar_temp,selected_club2)
    fixStr2 = fixStrength(next_five2)
    exp2 = exp_five(next_five2,player2,team)
    st.write(' - '.join(map(str, show_next_five(calendar_temp,selected_club2))))
    st.write(' - '.join(map(str, exp2)))

    st.write("xPoints: {:.2f}".format(round(sum(exp2), 2)))

    st.write('Fixture difficulty: '+ fixStr2)

  player1
  playerdb[playerdb['Player'].str.contains(player1)==True][categories]
  player2
  playerdb[playerdb['Player'].str.contains(player2)==True][categories]

elif page == 'Top 10 in xP':
  season = 2021
  playerdb = fpldb.createFPLDB()

  leaguetable = pdb.createTable(season)

  main = prepare(season)
  
  team_form_temp = team_form.copy()
  calendar_temp = calendar.copy()
  
  team_form_temp['name'] = main['Squad'].copy()
 
  calendar_temp['team_a'] = calendar_temp['team_a'].replace(list(calendar_temp['team_a'].sort_values().unique()),list(main['Squad']))
  calendar_temp['team_h'] = calendar_temp['team_h'].replace(list(calendar_temp['team_h'].sort_values().unique()),list(main['Squad']))

  fixes = pd.read_csv('fixes.csv').drop('Unnamed: 0',axis=1)
  fixes = fixes.set_index('name')

  minutes = playerdb[['Min','Starts','chance_of_playing_this_round','chance_of_playing_next_round']].astype('float64').fillna(100.0)
  minutes['Player'] = playerdb['Player'].copy()
  minutes['xMin'] = (minutes['Starts']/max(minutes['Starts'])*minutes['Min']/max(minutes['Starts'])*0.95)*minutes['chance_of_playing_this_round']/100


  st.header("Top 50 in xP")
  xP_table = []
  for x in playerdb['Player']:
    team = playerdb.iloc[playerdb[playerdb['Player']==x].index[0]]['Squad']
    xmin = minutes.iloc[minutes[minutes['Player']==x].index[0]]['xMin']
    nf = show_next_five(calendar_temp,team)
    exp = exp_five(nf,x,team)
    xP_table.append([x,xmin,sum(exp),nf[0],nf[1],nf[2],nf[3],nf[4]])
  xP_df = pd.DataFrame(xP_table,columns=['Name','xMin','xP','1','2','3','4','5'])
  st.write(xP_df.sort_values('xP',ascending=False).head(50))




  # with col21:
  #   st.plotly_chart(fig,use_container_width=True)
  #   st.subheader('Next five matches')
  #   next_five1 = show_next_five(calendar_temp,selected_club1)
  #   fixStr1 = fixStrength(next_five1)
  #   exp1 = exp_five(next_five1,player1)
  #   st.write(' - '.join(map(str, show_next_five(calendar_temp,selected_club1))))
  #   st.write("xPoints: {:.2f}".format(round(sum(exp1), 2)))


  #   st.write('Fixture difficulty: '+ fixStr1)

  # with col22:
  #   st.plotly_chart(fig2,use_container_width=True)
  #   st.subheader('Next five matches')
  #   next_five2 = show_next_five(calendar_temp,selected_club2)
  #   fixStr2 = fixStrength(next_five2)
  #   exp2 = exp_five(next_five2,player2)
  #   st.write(' - '.join(map(str, show_next_five(calendar_temp,selected_club2))))
  #   st.write("xPoints: {:.2f}".format(round(sum(exp2), 2)))

  #   st.write('Fixture difficulty: '+ fixStr2)

  # player1
  # playerdb[playerdb['Player'].str.contains(player1)==True][categories]
  # player2
  # playerdb[playerdb['Player'].str.contains(player2)==True][categories]