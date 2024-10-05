import folium.features
import streamlit as st
import pandas as pd
import folium
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium


url_shooting = 'https://github.com/bradleymarkjacobs001/MXB362_Data_Visualisation/raw/main/NYPD_Shooting_Incident_Data__Historic__20240817_1.csv'

url_police_precients ='https://github.com/bradleymarkjacobs001/MXB362_Data_Visualisation/raw/main/Police Precincts.geojson'

APP_TITLE = "NYC Police Precincts Report"
APP_SUB_TITLE = 'Source: NYC Open Data'


def display_incidents(df,year,metric_title):

   df = df[(df['YEAR'] == year)]
   total =df['YEAR'].count()
   st.metric(metric_title, '{:,}'.format(total))
   
   df1=df[(df['YEAR'] == year)].value_counts().rename("Incidents").to_frame().reset_index()
   df2 =df1.style.format({"Year":lambda x: f"{x:0f}"})
   st.dataframe(df2, column_config={
        "Incidents": st.column_config.ProgressColumn(
            "Incidents",
            format="%f",
            min_value=0,
            max_value=100,
        ),
    },hide_index=True) 
   
def graphic_view(year):
    df = pd.read_csv(url_shooting , usecols=[3,6,8],index_col= None)
    #df = pd.read_csv(r'C:\Users\bradley.jacobs\Documents\GitHub\MXB362_Data_Visualisation-\NYPD_Shooting_Incident_Data__Historic__20240817_1.csv', usecols=[3,6,8],index_col= None)
    df4 = df[(df['YEAR'] == year)]
    df5 = df4['BORO'].value_counts().rename('Incidents').to_frame().reset_index()
    x_lab = "Boroughs of NYC"
    y_lab = 'Number of incidents in year {}'.format(year)
    print(df5)
    
    fig = px.bar(df5, x='Incidents', y='BORO', color="BORO",facet_col_wrap=True, labels=True, title=("Number of incidents in year {0}".format(year)))

# Display the Plotly figure in Streamlit
    st.plotly_chart(fig)



def map (year):
    map = folium.Map(location=[ 40.71277530, -74.00597280  ], tiles='CartoDB positron')
    df = pd.read_csv(url_shooting , usecols=[3,6,8],index_col= None)
    #df = pd.read_csv(r'C:\Users\bradley.jacobs\Documents\GitHub\MXB362_Data_Visualisation-\NYPD_Shooting_Incident_Data__Historic__20240817_1.csv', usecols=[3,6,8],index_col= None)
   
    df1 = df[(df['YEAR'] == year)].value_counts().to_frame().reset_index()
  
    choropleth = folium.Choropleth (
        
        geo_data= url_police_precients,
       # geo_data= r'C:\Users\bradley.jacobs\Documents\GitHub\MXB362_Data_Visualisation-\Police Precincts.geojson',
        data= df1,
        columns=["PRECINCT","count","BORO"],
        line_opacity=0.8,
        fill_color="YlGn",
        key_on='feature.properties.precinct',
        highlight=True
        ).add_to(map)



  # Add tooltips to the GeoJson features
    for feature in choropleth.geojson.data['features']:
        precinct = int(feature['properties']['precinct'])
        feature['properties']['precinct'] = feature['properties']['precinct'].upper()  # Capitalize the precinct
        

        count = df1.loc[df1['PRECINCT'] == precinct, 'count'].values[0] if precinct in df1['PRECINCT'].values else 0
        feature['properties']['COUNT'] = f': {count}'
        boro = df1.loc[df1['PRECINCT'] == precinct, 'BORO'].values[0] if precinct in df1['PRECINCT'].values else 0
        feature['properties']['BORO'] = f': {boro}'
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['precinct','COUNT','BORO'], labels=True)
    )
    st.html(f'<h4><bold><div style="text-align: center;">NYC Police Precincts Choropleth Map for {year}</div></bold></h4>')
    st_map =st_folium(map,width=700,height=450)
    

#Display heatmap

def heatmap_all():
   df = pd.read_csv(url_shooting, usecols=[3,6],index_col= None)
   #df = pd.read_csv(r'C:\Users\bradley.jacobs\Documents\GitHub\MXB362_Data_Visualisation-\NYPD_Shooting_Incident_Data__Historic__20240817_1.csv', usecols=[3,6],index_col= None)

   df = df[(df['YEAR'] != None)]
   
   df1=df[(df['YEAR'] != None)].value_counts().rename("Incidents").to_frame().reset_index()
   
   fig =go.Figure(data=go.Heatmap(x=df1['YEAR'],y=df1['BORO'],z=df1['Incidents'], colorscale='Viridis'))
   fig.update_layout(
        title = '                                            Heatmap of NYC incidents in Police precincts from 2006 -2023'
    )
   st.plotly_chart(fig)


def main():

    st.set_page_config(layout="wide")
    st.html('<h1><div style="text-align: center;"> NYC Police Precincts Report</div></h1>')
   
    st.caption(APP_SUB_TITLE)

    #LOAD DATA
    df = pd.read_csv(url_shooting,usecols=[3,6,8],index_col= None)
    #df = pd.read_csv(r'C:\Users\bradley.jacobs\Documents\GitHub\MXB362_Data_Visualisation-\NYPD_Shooting_Incident_Data__Historic__20240817_1.csv',usecols=[3,6,8],index_col= None)
    
    
    metric_title =f' Number of Incidents'

    col1, col2, col3  = st.columns([1,1.5,1])

    with col1:
        year = st.selectbox('Choose an option:', df['YEAR'].sort_values(ascending=False).unique(),label_visibility='collapsed')
        st.write('You selected:', year)
        display_incidents(df,year,metric_title)
        
    with col2:
       map(year)
       heatmap_all()

    with col3:
       graphic_view(year)



if __name__ == "__main__":
    main()

