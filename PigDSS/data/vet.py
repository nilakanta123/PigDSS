import numpy as np
import pandas as pd
df = pd.read_csv("vet_hospital.csv")
#print(df)
#print(len(df))
#print(df['Address'].values)
place='Guwahati'
for i in range(0,len(df)):
    if df.iloc[i].values[1]==place:
        print("Hospital name:\t\t",df.iloc[i].values[4])
        print("Phone no:\t\t",df.iloc[i].values[5])
        print("Address:\t\t",df.iloc[i].values[6])
        print("\n\n")
