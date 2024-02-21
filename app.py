import streamlit as st
import pandas as pd
import plotly.express as px
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
force_csv_path = os.path.join(current_dir, 'force.csv')

force_df = pd.read_csv(force_csv_path)
force_df['year'] = pd.to_datetime(force_df['date']).dt.year
force_df = force_df.dropna(subset=['lat','lon','hour','civ.race','civ.gender','year'], how='any')


colors = {
    'background': '#f0f0f0', 
    'text': '#333333',         
    'primary': '#3498db',     
    'accent': '#2ecc71'        
}

race_color_map = {
   'BLACK': 'blue',
   'HISPANIC': 'red',
   'WHITE': 'green',
   'ASIAN/PACIFIC ISLANDER': 'orange',
   'NATIVE AMERICAN/ALASKAN NATIVE': 'purple',
}

st.markdown("<h2 style='text-align: center;'>Chicago Use of Force Incidents, 2012-2015</h2>", unsafe_allow_html=True)

selected_years = st.sidebar.header("Filters")
selected_years = st.sidebar.multiselect("Select Year", list(range(2012, 2016)), default=list(range(2012, 2016)))
selected_race = st.sidebar.multiselect("Select Race", force_df['civ.race'].unique(), default=force_df['civ.race'].unique())
selected_gender = st.sidebar.multiselect("Select Gender", force_df['civ.gender'].unique(), default=force_df['civ.gender'].unique())

dff = force_df[(force_df["year"].isin(selected_years)) & 
               (force_df["civ.race"].isin(selected_race)) & 
               (force_df["civ.gender"].isin(selected_gender))]


dff = force_df[(force_df["year"].isin(selected_years)) & 
               (force_df["civ.race"].isin(selected_race)) & 
               (force_df["civ.gender"].isin(selected_gender))]


filter_injured = st.sidebar.checkbox("Incidents With Civilians Injured")

if filter_injured:
    dff = dff[dff["civ.injured"] == 1]


filter_by_age = st.sidebar.checkbox("Filter by Age")

if filter_by_age:
    min_age, max_age = st.sidebar.slider("Select Age Range", int(force_df['civ.age'].min()), int(force_df['civ.age'].max()), (int(force_df['civ.age'].min()), int(force_df['civ.age'].max())))
    dff = dff[(dff["civ.age"] >= min_age) & (dff["civ.age"] <= max_age)]


filter_by_hour = st.sidebar.checkbox("Filter by Hour")

if filter_by_hour:
    min_hour, max_hour = st.sidebar.slider("Select Hour Range", int(force_df['hour'].min()), int(force_df['hour'].max()), (int(force_df['hour'].min()), int(force_df['hour'].max())))
    dff = dff[(dff['hour'] >= min_hour) & (dff['hour'] <= max_hour)]

fig = px.scatter_mapbox(
    data_frame=dff,
    lat="lat",
    lon="lon",
    color="civ.race",
    size_max=15,
    color_discrete_map=race_color_map,
    zoom=10,
    center=dict(lat=41.8781, lon=-87.6298),
    mapbox_style="open-street-map"
)

fig.update_layout(
    height=600,
    width=800,
    margin=dict(t=20),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)



st.plotly_chart(fig)
