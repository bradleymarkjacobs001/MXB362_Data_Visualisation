

import pandas as pd





     
     


def main():

    #LOAD DATA
    df = pd.read_csv(r'C:\Users\bradley.jacobs\Documents\GitHub\MXB362_Data_Visualisation-\NYPD_Shooting_Incident_Data__Historic__20240817_1.csv',parse_dates=['OCCUR_DATE'])

    df1 = pd.read_csv(r'C:\Users\bradley.jacobs\Documents\GitHub\MXB362_Data_Visualisation-\NYPD_Shooting_Incident_Data__Historic__20240817_1.csv', usecols=[3,6,8],index_col= None)
    precinct =10
    year = 2023
    df2 = df1[(df1['YEAR'] == year)].value_counts().to_frame().reset_index()
    df2.rename(columns={"count": "No_of_incidents"})
    print(df2.columns)
    print(df2)
    count = df2.loc[df2['PRECINCT'] == precinct, 'count'].values[0] if precinct in df2['PRECINCT'].values else 0
    print(count)
    
  

  
  




    #DISPLAY METRICS



if __name__ == "__main__":
    main()

