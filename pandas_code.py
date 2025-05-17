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


#Calculating total points for home team
home_pts = df.groupby('HomeTeam')['HomePoints'].sum().sort_values(ascending=False).rename('TotalHomePoints')
print(home_pts)

#Calculating points for away team
away_pts = df.groupby('AwayTeam')['AwayPoints'].sum().sort_values(ascending=False).rename('TotalAwayPoints')

#Creating new Df with home points, away points and total points
df2 = pd.concat([home_pts, away_pts], axis=1)
df2['TotalPoints'] = df2['TotalHomePoints'] + df2['TotalAwayPoints']
df2 = df2.head(6)

print(df2)


df2.plot(kind='bar', title='Big 6 Points Summary', xlabel='Teams', ylabel='Points')
plt.show()