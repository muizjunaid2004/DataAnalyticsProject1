import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    'Year': [2021, 2022, 2023],
    'Sales': [100, 200, 300]
})

plt.plot(df['Year'], df['Sales'])      # Plot X vs Y
plt.xlabel('Year')                     # Add X axis label
plt.ylabel('Sales')                    # Add Y axis label
plt.title('Year vs Sales')             # Add plot title
plt.xticks(df['Year'])                 # Set X-axis ticks explicitly
plt.show()   