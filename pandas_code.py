import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("PremierLeague.csv")

#Filtering df to only include games including big 6 for more efficient processing
big_6 = ['Man United', 'Tottenham', 'Man City', 'Liverpool', 'Arsenal', 'Chelsea' ]

df = df[df['HomeTeam'].isin(big_6) | df['AwayTeam'].isin(big_6)]

#Converting to date for easier filtering
df['Date'] = pd.to_datetime(df['Date'])


#Making new column for home points
df['HomePoints'] = np.where(

    df['FullTimeHomeTeamGoals'] > df['FullTimeAwayTeamGoals'], 3,
    np.where(df['FullTimeHomeTeamGoals'] == df['FullTimeAwayTeamGoals'], 1, 0
    )
    
)

#Making new column for away points
df['AwayPoints'] = np.where(

    df['FullTimeHomeTeamGoals'] < df['FullTimeAwayTeamGoals'], 3,
    np.where(df['FullTimeHomeTeamGoals'] == df['FullTimeAwayTeamGoals'], 1, 0
    )
)




'''
TEAM POINTS HOME, AWAY AND TOTAL BELOW

'''

#Calculating total points at home
home_pts = df.groupby('HomeTeam')['HomePoints'].sum().sort_values(ascending=False).rename('TotalHomePoints')

#Calculating points away 
away_pts = df.groupby('AwayTeam')['AwayPoints'].sum().sort_values(ascending=False).rename('TotalAwayPoints')

#Creating new Df with home points, away points and total points
df2 = pd.concat([home_pts, away_pts], axis=1)
df2['TotalPoints'] = df2['TotalHomePoints'] + df2['TotalAwayPoints']
df2 = df2.head(6)

#Plotting df2
df2.plot(kind='bar', title='Big 6 Points Summary', xlabel='Teams', ylabel='Points')
#plt.show()




'''
NUMBER OF WINS AND DRAWS (HOME AND AWAY) AND TOTAL 
'''

#Calculating number of home wins
home_wins = df[df['HomePoints'] > 1].groupby('HomeTeam')['HomePoints'].count().sort_values(ascending=False).rename('TotalHomeWins')

#Calculating number of away wins
away_wins = df[df['AwayPoints'] > 1].groupby('AwayTeam')['AwayPoints'].count().rename('TotalAwayWins')



#Calculating the number of draws at home
home_draws = df[(df['HomePoints'] == 1)].groupby('HomeTeam')['HomePoints'].count().rename('TotalHomeDraws')

#Calculating numbr of away draws
away_draws = df[(df['HomePoints'] == 1)].groupby('AwayTeam')['AwayPoints'].count().rename('TotalAwayDraws')

#Creating new Df to house wins both home and away and draws both home and away
df3 = pd.concat([home_wins, away_wins, home_draws, away_draws], axis=1)
df3.fillna(0, inplace=True)

#Changing columns from float back to int
df3_columns = df3.columns.to_list()
for col in df3_columns:
    df3[col] = df3[col].astype(int)
    
df3['TotalWins'] = df3['TotalHomeWins'] + df3['TotalAwayWins']
df3['TotalDraws'] = df3['TotalHomeDraws'] + df3['TotalAwayDraws']

df3 = df3.loc[big_6]

#Plotting all win data
df3[['TotalHomeWins', 'TotalAwayWins', 'TotalWins']].plot(kind='bar', title='Big 6 Wins Stats', xlabel='Teams', ylabel='Points')
#plt.show()

#Plotting all Draw Data
df3[['TotalHomeDraws', 'TotalAwayDraws', 'TotalDraws']].plot(kind='bar', title='Big 6 Draw Stats', xlabel='Teams', ylabel='Points')
#plt.show()



'''
NUMBER OF LOSSES (HOME AND AWAY)
'''
#Calculating number of home wins
home_losses = df[df['HomePoints'] == 0].groupby('HomeTeam')['HomePoints'].count().sort_values(ascending=False).rename('TotalHomeLosses')

#Calculating number of away wins
away_losses = df[df['AwayPoints'] == 0].groupby('AwayTeam')['AwayPoints'].count().rename('TotalAwayLosses')

#Creating new DF for loss data
df4 = pd.concat([home_losses, away_losses], axis=1)
df4['TotalLosses'] = df4['TotalHomeLosses'] + df4['TotalAwayLosses']
df4 = df4.loc[big_6]

df4.plot(kind='bar', title='Big 6 Losses Stats', xlabel='Teams', ylabel='Points')
#plt.show()



'''
GETTING NUMBER OF WINS DRAWS AND LOSSES AS A PERCENT OF GAMES
'''

total_games_played = df3['TotalWins'] + df3['TotalDraws'] + df4['TotalLosses']

df3['TotalGamesPlayed'] = total_games_played
df3['WinPercentage'] = (df3['TotalWins']/df3['TotalGamesPlayed']) * 100
df3['DrawPercentage'] = (df3['TotalDraws']/df3['TotalGamesPlayed']) * 100

df4['TotalGamesPlayed'] = total_games_played
df4['LossPercentage'] = (df4['TotalLosses']/df4['TotalGamesPlayed']) * 100

df5 = df3[['WinPercentage', 'DrawPercentage']].copy()
df5['LossPercentage'] = df4['LossPercentage']


df5.plot(kind='bar', legend='true', title='Big 6 Win Loss Draw Percentages', xlabel='Teams', ylabel='Percentage')
plt.show()

