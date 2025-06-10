import pandas as pd
import requests
from io import StringIO

from datetime import datetime

import matplotlib.pyplot as plt

# Define Functions

def split_date_range(df, column_name, start_col = 'date_start', end_col = 'date_end'):

    def parse_date_range(date_string):

        try:

            clean_string = date_string.split('@@')[0].strip()

            parts = clean_string.split(',')

            date_range = parts[0].strip()

            year = parts[1].strip()

            start_date_str, end_date_str = date_range.split(' - ')

            start_date_full = f"{start_date_str}/{year}"
            end_date_full = f"{end_date_str}/{year}"

            start_date = pd.to_datetime(start_date_full, format = '%m/%d/%Y')
            end_date =  pd.to_datetime(end_date_full, format = '%m/%d/%Y')

            return start_date, end_date

        except Exception as e:

            print(f"Error parsing date: {date_string}, Error {e}")

            return(pd.NaT, pd.NaT)

    df_copy = df.copy()

    date_pairs = df_copy[column_name].apply(parse_date_range)

    df_copy[start_col] = [pair[0] for pair in date_pairs]

    df_copy[end_col] = [pair[1] for pair in date_pairs]

    return df_copy
            
# Read Trump Approval Rating .csv from URL

url = "https://static.dwcdn.net/data/wWI2Y.csv?v=1749325560000"

response = requests.get(url)
response.raise_for_status()

df = pd.read_csv(StringIO(response.text))

# Clean Up Dates

df_clean = split_date_range(df, 'Dates')

# Save Clean Data

df_clean[['date_start','date_end','Influence','Approve','Disapprove','Net']].sort_values(by = 'date_end', ascending = False).to_csv('trump_approval.csv', index = False)

# Select Only Relevant Variables for Plot

df_plot = df_clean[['date_end','Approve', 'Disapprove', 'Net']]

# Create Daily Average

df_plot_mean = df_plot.groupby('date_end').mean()[['Approve', 'Disapprove','Net']].rolling(window = 7, min_periods = 1, center = True).mean().reset_index()

# Create Net Approval Plot

plt.figure(figsize = (8,6))

plt.scatter(df_plot['date_end'], df_plot['Net'], alpha = 0.3, c = 'purple', s = 50)

plt.plot(df_plot_mean['date_end'], df_plot_mean['Net'], c = 'purple', linewidth = 3)

plt.xlabel('Date Polling Ended')
plt.ylabel('Approval Rating - Dissaproval Rating')
plt.title('Trump Net Approval Over Time')

plt.xticks(pd.date_range(start = min(df_plot['date_end']), end = max(df_plot['date_end']), freq = '1ME'))

plt.grid(False)

plt.savefig('trump_polling_net.png', dpi = 300, bbox_inches = 'tight')

plt.clf()

# Create Approval and Disapproval Plot

plt.figure(figsize = (8,6))

plt.scatter(df_plot['date_end'], df_plot['Approve'], alpha = 0.3, c = 'green', s = 50)

plt.scatter(df_plot['date_end'], df_plot['Disapprove'], alpha = 0.3, c = 'red', s = 50)

plt.plot(df_plot_mean['date_end'], df_plot_mean['Approve'], c = 'green', linewidth = 3)

plt.plot(df_plot_mean['date_end'], df_plot_mean['Disapprove'], c = 'red', linewidth = 3)

plt.xlabel('Date Polling Ended')
plt.ylabel('Approval / Disapproval Rating')
plt.title('Trump Approval and Disapproval Over Time')

plt.xticks(pd.date_range(start = min(df_plot['date_end']), end = max(df_plot['date_end']), freq = '1ME'))

plt.grid(False)

plt.savefig('trump_polling_appdis.png', dpi = 300, bbox_inches = 'tight')

plt.clf()

