import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

games = pd.read_csv("preSeason.csv", low_memory=False)

#Convert Months to numbers
months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

games['Week'] = games['Week'].str[3:]
games["VisTm"] = games["VisTm"].str.split().str[-1]
games["HomeTm"] = games["HomeTm"].str.split().str[-1]
games['Day'], games['Month'] = games['Date'].str.split('-', 1).str
games['Hour'], games['Minute'] = games['Time'].str.split(':', 1).str
games['Hour'] = games['Hour'].astype(int) + 12
games['Minute'], games['Trash'] = games['Minute'].str.split(' ', 1).str

games["Month"] = games["Month"].map(months)
                                   
games.to_csv('newPreSeason.csv', index=False)