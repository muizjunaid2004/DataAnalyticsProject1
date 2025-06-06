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




'''
Calculating Points per season
'''

#Plotting df2
#df2.plot(kind='bar', title='Big 6 Points Summary', xlabel='Teams', ylabel='Points')
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
#df3[['TotalHomeWins', 'TotalAwayWins', 'TotalWins']].plot(kind='bar', title='Big 6 Wins Stats', xlabel='Teams', ylabel='Points')
#plt.show()

#Plotting all Draw Data
#df3[['TotalHomeDraws', 'TotalAwayDraws', 'TotalDraws']].plot(kind='bar', title='Big 6 Draw Stats', xlabel='Teams', ylabel='Points')
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

#df4.plot(kind='bar', title='Big 6 Losses Stats', xlabel='Teams', ylabel='Points')
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
df5['WinPercentage']= df5['WinPercentage'].sort_values(ascending=False)
print(df5)


df5.plot(kind='bar', legend='true', title='Big 6 Win Loss Draw Percentages', xlabel='Teams', ylabel='Percentage')
#plt.show()


'''
CALCULATING POINTS PER SEASON FOR TOP6
'''

#Calculating home points per season
home_pts = df.groupby(['Season','HomeTeam'])['HomePoints'].sum().rename('TotalHomePoints')
home_pts.index.names = ['Season', 'Team']

#Calculating away points per season
away_pts = df.groupby(['Season','AwayTeam'])['AwayPoints'].sum().rename('TotalAwayPoints')
away_pts.index.names = ['Season', 'Team']

df6 = pd.concat([home_pts, away_pts], axis=1)
df6['TotalPoints'] = df6['TotalHomePoints'] + df6['TotalAwayPoints']



#Creating pivot tables so I can graph data
df6 = df6.reset_index()
df6 = df6.fillna(0)


pivot_table = df6[df6['Team'].isin(big_6)].pivot_table(index='Season', columns='Team', values='TotalPoints')
pivot_table.fillna(0, inplace=True)

pivot_table.plot(marker= 'o', title='Man Utd & Man City Points Over the Years', xlabel='Year', ylabel='Points')


#Average points for teams in between years 1993-2003, 2003-2013, 2013-2023
period_1 = [
    "1993-1994", "1994-1995", "1995-1996", "1996-1997", "1997-1998",
    "1998-1999", "1999-2000", "2000-2001", "2001-2002", "2002-2003"
]

period_2 = [
    "2003-2004", "2004-2005", "2005-2006", "2006-2007", "2007-2008",
    "2008-2009", "2009-2010", "2010-2011", "2011-2012", "2012-2013"
]

period_3 = [
    "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018",
    "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023",
    "2023-2024"
]

new_df = pivot_table.reset_index()

def average_values(team, df=new_df):

    new_df_1 = new_df[new_df['Season'].isin(period_1)]
    new_df_2 = new_df[new_df['Season'].isin(period_2)]
    new_df_3 = new_df[new_df['Season'].isin(period_3)]    
    val = new_df_1[team].mean()
    val2 = new_df_2[team].mean()
    val3 = new_df_3[team].mean()
    print(f'\n\n\n\n{team}: 1993-2003:{val}, 2003:2013:{val2}, 2013-2024:{val3}\n\n\n\n')



'''
Liverpool specific
'''


df = pd.read_csv('EPL Standings 2000-2022.csv')
print(df)

df_liverpool = df[df['Team'] == 'Liverpool'].copy()

df_liverpool.loc[len(df_liverpool)] = {
    "Season": "2022-23", 
    "Pos": 5, 
    "Team": "Liverpool", 
    "Pts": 67
    }

df_liverpool.loc[len(df_liverpool)] = {
    "Season": "2023-24", 
    "Pos": 3, 
    "Team": "Liverpool", 
    "Pts": 82
    }

df_liverpool.loc[len(df_liverpool)] = {
    "Season": "2024-25", 
    "Pos": 1, 
    "Team": "Liverpool", 
    "Pts": 84
    }

average_values('Liverpool')

'''
Man Utd Specific
'''
df_united = df[df['Team'] == 'Manchester United'].copy()
df_united.loc[len(df_united)] = {
    "Season": "2022-23", 
    "Pos": 3, 
    "Team": "Manchester United", 
    "Pts": 75
    }

df_united.loc[len(df_united)] = {
    "Season": "2023-24", 
    "Pos": 8, 
    "Team": "Manchester United", 
    "Pts": 60
    }

df_united.loc[len(df_united)] = {
    "Season": "2024-25", 
    "Pos": 15, 
    "Team": "Manchester United", 
    "Pts": 42
    }



print(df_united['Pos'].value_counts())

average_values('Man United')





'''
Man City Specific
'''

df_city = df[df['Team'] == 'Manchester City'].copy()
df_city.loc[len(df_city)] = {
    "Season": "2022-23", 
    "Pos": 1, 
    "Team": "Manchester City", 
    "Pts": 89
    }

df_city.loc[len(df_city)] = {
    "Season": "2023-24", 
    "Pos": 1, 
    "Team": "Manchester City", 
    "Pts": 91
    }


df_city.loc[len(df_city)] = {
    "Season": "2024-25", 
    "Pos": 3, 
    "Team": "Manchester City", 
    "Pts": 71
    }

print(df_city['Pos'].value_counts())

average_values('Man City')

'''
Arsenal Specific
'''

df_arsenal = df[df['Team'] == 'Arsenal'].copy()
df_arsenal.loc[len(df_arsenal)] = {
    "Season": "2022-23", 
    "Pos": 2, 
    "Team": "Arsenal", 
    "Pts": 84
    }

df_arsenal.loc[len(df_arsenal)] = {
    "Season": "2023-24", 
    "Pos": 2, 
    "Team": "Arsenal", 
    "Pts": 89
    }


df_arsenal.loc[len(df_arsenal)] = {
    "Season": "2024-25", 
    "Pos": 2, 
    "Team": "Arsenal", 
    "Pts": 74
    }

print(df_arsenal['Pos'].value_counts())
print(df_arsenal)

average_values('Arsenal')

'''
Spurs Specific
'''

df_spurs = df[df['Team'] == 'Tottenham Hotspur'].copy()

df_spurs.loc[len(df_spurs)] = {
    "Season": "2022-23", 
    "Pos": 8, 
    "Team": "Tottenham Hotspur", 
    "Pts": 60
    }

df_spurs.loc[len(df_spurs)] = {
    "Season": "2023-24", 
    "Pos": 5, 
    "Team": "Tottenham Hotspur", 
    "Pts": 66
    }


df_spurs.loc[len(df_spurs)] = {
    "Season": "2024-25", 
    "Pos": 17, 
    "Team": "Tottenham Hotspur", 
    "Pts": 38
    }

print(df_spurs['Pos'].value_counts())
print(df_spurs)

average_values('Tottenham')

'''
Chelsea Specific
'''

df_chelsea = df[df['Team'] == 'Chelsea'].copy()

df_chelsea.loc[len(df_chelsea)] = {
    "Season": "2022-23", 
    "Pos": 12, 
    "Team": "Chelsea", 
    "Pts": 44
    }

df_chelsea.loc[len(df_chelsea)] = {
    "Season": "2023-24", 
    "Pos": 6, 
    "Team": "Chelsea", 
    "Pts": 63
    }


df_chelsea.loc[len(df_chelsea)] = {
    "Season": "2024-25", 
    "Pos": 4, 
    "Team": "chelsea", 
    "Pts": 69
    }

print(df_chelsea['Pos'].value_counts())
print(df_chelsea)

average_values('Chelsea')
