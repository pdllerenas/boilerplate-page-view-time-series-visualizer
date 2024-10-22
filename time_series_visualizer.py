import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=True)

# Clean data - only consider those between 2.5% and 97.5%
df = df.loc[(df['value'] < df['value'].quantile(0.975)) & (df['value'] > df['value'].quantile(0.025))]

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(df.date, df.value)

    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_xticks(df.date[::90*3])

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['year'] = df_bar['date'].apply(lambda x: str(x)[:4])
    df_bar['month'] = df_bar['date'].apply(lambda x: str(x)[5:7])

    df_bar = df_bar.groupby(['month', 'year'])['value'].mean().unstack()
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(15,8))
    years = df_bar.columns
    months = df_bar.index

    x = np.arange(len(years))
    width = 0.05
    for i, year in enumerate(years):
        for j, month in enumerate(months):

            ax.bar(x[i]+j*width, df_bar[year][month], width, label=MONTHS[int(month)-1] if i == 0 else "")

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.set_title("Monthly Average Page Views")

    ax.set_xticks(0.15+x + width * (len(years) - 1) / 2)
    ax.set_xticklabels(years, rotation = 45)

    ax.legend(title='Months')


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.split('-')[0] for d in df_box.date]
    df_box['month'] = [d.split('-')[1] for d in df_box.date]
    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1,2)
    fig.set_figwidth(15)
    ax1 = sns.boxplot(x = df_box["year"], y = df_box["value"], ax= ax1)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax2 = sns.boxplot(x = df_box["month"], y = df_box["value"], ax= ax2)
    ax2.set_xticks(list(range(0, 12)))
    ax2.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")
    ax2.set_title("Month-wise Box Plot (Seasonality)")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
