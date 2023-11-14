import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime as dt

#Read in csv
df = pd.read_csv('strava_nov_23.csv') 

#Change columns to lower case
df.columns=df.columns.str.lower() 

#Only include relevant columns in df 
cols = ['activity id', 'activity date', 'activity type', 'elapsed time', 'moving time', 'distance',   
         'elevation gain', 'max speed'
       ]
df = df[cols] 

# Convert 'activity date' to datetime
df['activity_date'] = pd.to_datetime(df['activity date'], format="%d %b %Y, %H:%M:%S")

# Extract additional date related information
df['start_time'] = df['activity_date'].dt.time
df['start_date_local'] = df['activity_date'].dt.date
df['month'] = df['activity_date'].dt.month_name()
df['year'] = df['activity_date'].dt.year.astype(object)
df['dayofyear'] = df['activity_date'].dt.dayofyear
df['dayofyear'] = pd.to_numeric(df['dayofyear'])

# Create extra columns to create metrics which aren't in the dataset already
df['moving minutes'] = df['moving time'] /60 
df['km per hour'] = df['distance'] / (df['moving minutes'] / 60)
df['avg pace'] = df['moving minutes'] / df['distance']

# Create df to include only valid runs 
runs = df[df['activity type'] == 'Run']
runs = runs[runs['elapsed time'] <= 100000]

# # Create a pairplot 
# pp_df = runs[['moving minutes', 'distance', 'elevation gain', 'avg pace', 'activity_date']]
# sns.pairplot(pp_df)
# plt.show()

# Summary of data
print(runs.describe().round(0))

# Plot distance by month 
fig, ax = plt.subplots()
sns.set(style="whitegrid", font_scale=1)
sns.boxplot(x="month", y="distance", hue="month", data=runs, ax=ax, legend=False)
plt.gcf().set_size_inches(9, 6)

# Optional: Add a custom legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, title="Month", loc="upper right")

plt.show()

