import warnings
import pandas as pd
import numpy as np
from datetime import datetime
warnings.filterwarnings("ignore")

df = pd.read_csv("taxiwala.csv")

airport_df = df[df['Pickup Point'] == "Airport"]
kamakhya_df = df[df['Pickup Point'] == "Kamakhya Railway Station"]
guwahati_df = df[df['Pickup Point'] == "Guwahati Railway Station"]

INIT_TIME = '12/29/2023 12:00:00 AM'
format = '%m/%d/%Y %I:%M:%S %p'

def get_minutes(current_dt):
    init_date = datetime.strptime(INIT_TIME, format)
    current_date = datetime.strptime(current_dt, format)
    delta = (current_date - init_date).total_seconds() / 60
    return delta

def get_df_groups(df):
    
    df['datetime'] = df['Arrival Date'] + " " + df['Flight/Train Arrival Time']
    df['delta'] = df['datetime'].apply(get_minutes)
    df = df.sort_values(['delta'], ascending=True)
    
    timestamps = df['delta'].values

    n = len(timestamps)
    i = 0

    groups = []

    while(i < n):
        
        current_g = []
        current_g.append({"Name" : df.iloc[i]['Name'], "Phone" : df.iloc[i]['Phone Number'], "Time" : df.iloc[i]['datetime']})

        j = i + 1

        for x in range(3):

            if(i + x + 1 >= n):
                break

            if(timestamps[i + x + 1] - timestamps[i] <= 30):
                current_g.append({"Name" : df.iloc[i + x + 1]['Name'], "Phone" : df.iloc[i + x + 1]['Phone Number'], "Time" : df.iloc[i + x + 1]['datetime']})
            else:
                j = i + x + 1
                break
            
        groups.append(current_g)
        i = j

    return groups

dfs = [airport_df, kamakhya_df, guwahati_df]

for i, df in enumerate(dfs):
    if(i == 0):
        f = open("airport.txt", "w")
        grps = get_df_groups(airport_df)
    elif(i == 1):
        f = open("kamakhya.txt", "w")
        grps = get_df_groups(kamakhya_df)
    else:
        f = open("guwahati.txt", "w")
        grps = get_df_groups(guwahati_df)

    for i, grp in enumerate(grps):
        f.write(f"Group {i + 1}\n")
        for ind in grp:
            f.write(f"Name : {ind['Name']}, Phone : {ind['Phone']}, Time : {ind['Time']}\n")
        f.write('\n')