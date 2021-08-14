
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
import playerdb as pdb
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from highlight_text import fig_text
from matplotlib import patches as mpatches
from matplotlib import colors
from matplotlib import font_manager

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
               'Newcastle':'#F1BE48', 'Norwich':'#00A650', 'Sheffield Utd':'#0D171A', 
               'Southampton':'#130C0E', 'Tottenham':'#FFFFFF', 'Watford':'#ED2127', "West Brom": '#FFFFFF', 'West Ham':'#1BB1E7',
               'Wolves':'#231F20'}

team_colors = {'Arsenal':'#ef0107', 'Aston Villa':'#95bfe5', 'Bournemouth':'#000000','Brentford':'#D60019', 'Brighton':'#0057b8',
               'Burnley':'#6c1d45', 'Chelsea':'#034694', 'Crystal Palace':'#1b458f', 'Everton':'#003399', "Fulham": "#000000",
               'Leicester City':'#003090', "Leeds United": "#1D428A", 'Liverpool':'#c8102e', 'Manchester City':'#6cabdd', 'Manchester Utd':'#da291c',
               'Newcastle Utd':'#241f20', 'Norwich':'#fff200', 'Sheffield Utd':'#ee2737', 
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
  main = main.rename(columns={"Succ": "Successful Dribles","ProgCarries": "Progressive Carries","ProgPasses": "Progressive Passes","TklW": "Tackles Won","Poss": "Possesion[%]","Int": "Interceptions","1/3": "Passes into final third"})
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


#######################

# st.title("Premier League Team Dashboard | Season {}/{} ".format(season,season+1))

#######################

col1, col2, col3 = st.columns([1,2,2])
# playerdb = pdb.createDatabase(season)

# leaguetable = pdb.createTable(season)

# main = prepare(season)

#######################

st.sidebar.header("Dashboard Settings")

with st.sidebar.expander("Season"):
  season = st.selectbox("",options=[2021,2020])

st.title("Premier League Team Dashboard | Season {}/{} ".format(season,season+1))

playerdb = pdb.createDatabase(season)

leaguetable = pdb.createTable(season)

main = prepare(season)

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
              round_int=[False]*len(categories),
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

