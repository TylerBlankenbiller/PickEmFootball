import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

homeTeam= '49ers'
awayTeam= 'Cowboys'

data = pd.read_csv('picks.csv', low_memory=False)

winners = pd.read_csv('newPreSeason.csv', low_memory=False)

winners = winners.loc[(winners.Month == 8) & (winners.Day <= 10)]

names = data['Name'].unique()

finalPicks = pd.DataFrame(columns=['Name', 'HomeScore', 'AwayScore', '49ers', 'Bears', 'Bengals', 'Bills', 
                            'Broncos', 'Browns', 'Bucaneers', 'Cardinals', 'Chargers', 'Chiefs', 'Colts',
                            'Cowboys', 'Dolphins', 'Eagles', 'Falcons', 'Giants', 'Jaguars', 'Jets', 'Lions',
                            'Packers', 'Panthers', 'Patriots', 'Raiders', 'Rams', 'Ravens', 'Redskins', 
                            'Saints', 'Seahawks', 'Steelers', 'Texans', 'Titans', 'Vikings'])
                            
columns = list(data.columns.values)
columns.remove('Name')
columns.remove('Week')
columns.remove('Month')
columns.remove('Day')
columns.remove('Hour')
columns.remove('Minute')
for name in names:
    series = pd.DataFrame({'Name':['a'], 'HomeScore':[0], 'AwayScore':[0], '49ers':[0], 'Bears':[0], 
                            'Bengals':[0], 'Bills':[0], 'Broncos':[0], 'Browns':[0], 'Bucaneers':[0],
                            'Cardinals':[0], 'Chargers':[0], 'Chiefs':[0], 'Colts':[0], 'Cowboys':[0], 
                            'Dolphins':[0], 'Eagles':[0], 'Falcons':[0], 'Giants':[0], 'Jaguars':[0], 
                            'Jets':[0], 'Lions':[0], 'Packers':[0], 'Panthers':[0], 'Patriots':[0],
                            'Raiders':[0], 'Rams':[0], 'Ravens':[0], 'Redskins':[0], 'Saints':[0], 
                            'Seahawks':[0], 'Steelers':[0], 'Texans':[0], 'Titans':[0], 'Vikings':[0]})
    for index, row in data.iterrows():
        if(name == row['Name']):
            series['Name'] = name
            for column in columns:
                if(row[column] == column):#Check if picked to win
                    loser = winners.loc[(winners.VisTm == column) | (winners.HomeTm == column)]
                    if((row['Month'] == loser['Month'].iloc[0] and row['Day'] == loser['Day'].iloc[0] and row['Hour'] == loser['Hour'].iloc[0] and row['Minute'] < loser['Minute'].iloc[0])
                        or (row['Month'] == loser['Month'].iloc[0] and row['Day'] == loser['Day'].iloc[0] and row['Hour'] < loser['Hour'].iloc[0])
                        or (row['Month'] == loser['Month'].iloc[0] and row['Day'] < loser['Day'].iloc[0])
                        or (row['Month'] < loser['Month'].iloc[0])):
                        series[column] = 1
                        if(loser['VisTm'].iloc[0] == column):
                            series[loser['HomeTm'].iloc[0]] = 0
                        else:
                            series[loser['VisTm'].iloc[0]] = 0
                elif(column == 'HomeScore'):
                    loser = winners.loc[(winners.HomeTm == homeTeam)]
                    if((row['Month'] == loser['Month'].iloc[0] and row['Day'] == loser['Day'].iloc[0] and row['Hour'] == loser['Hour'].iloc[0] and row['Minute'] < loser['Minute'].iloc[0])
                        or (row['Month'] == loser['Month'].iloc[0] and row['Day'] == loser['Day'].iloc[0] and row['Hour'] < loser['Hour'].iloc[0])
                        or (row['Month'] == loser['Month'].iloc[0] and row['Day'] < loser['Day'].iloc[0])
                        or (row['Month'] < loser['Month'].iloc[0])
                        and ((row['HomeScore'] != '') or (row['AwayScore'] != ''))):
                        series['HomeScore'] = row['HomeScore']
                        series['AwayScore'] = row['AwayScore']
                        if(row['HomeScore'] > row['AwayScore']):
                            series[homeTeam] = 1
                            series[awayTeam] = 0
                        else:
                            series[homeTeam] = 0
                            series[awayTeam] = 1
                        
    
    finalPicks = finalPicks.append(series, ignore_index=True)

columns.remove('HomeScore')
columns.remove('AwayScore')
correctPicks = pd.DataFrame(columns=['Name', 'Hit', 'Miss', 'Points'])
for index, row in finalPicks.iterrows():
    series = pd.DataFrame({'Name':[row['Name']], 'Hit':[0], 'Miss':[0], 'Points':[0]})
    for column in columns:
        #if(row[column] == 1):#Check if team was picked and if they actually won
        #    loser = winners.loc[(winners.VisTm == column) | (winners.HomeTm == column)]
        #    if(loser['Winner'].iloc[0] == column):
        #        series['Hit'] += 1
        #    else:
        #        series['Miss'] += 1
        if(row[column] == 0):#Picked to Lose
            loser = winners.loc[(winners.VisTm == column) | (winners.HomeTm == column)]
            if(loser['Winner'].iloc[0] == column):
                series['Miss'] += 1
            else:
                if(row[loser['Winner'].iloc[0]] == 1):
                    series['Hit'] += 1
                #else:
                #    series['Miss'] += 1
    correctPicks = correctPicks.append(series, ignore_index=True)
    
correctPicks.to_csv('PickRecord.csv', index=False)
finalPicks.to_csv('FinalPicks.csv', index=False)