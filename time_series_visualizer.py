import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data
df = df[(df.value > df.value.quantile(0.025)) & (df.value < df.value.quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig = df.plot.line(figsize=(15,5), color='red', legend=False);
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019');
    plt.xlabel('Date');
    plt.xticks(rotation = 0)
    plt.ylabel('Page Views');

    fig = fig.figure
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df.index.year
    df_bar['month'] = df.index.month_name()

    # grouping and orgenizing the df
    df_bar_group = df_bar.groupby(['year', 'month'])['value'].mean()
    df_bar_group = df_bar_group.unstack(level='month')
    df_bar_group = df_bar_group[['January', 'February', 'March', 'April', 'May',
                                'June', 'July', 'August', 'September', 'October', 'November', 'December']]

    # Draw bar plot
    fig = df_bar_group.plot.bar(figsize=(7,7)).figure
    plt.xlabel('Years');
    #plt.xticks(rotation = 0)
    plt.ylabel('Average Page Views');
    plt.legend(title='Months');

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


# Box plot function
def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year.astype(str)  # Ensure 'year' is a string
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')

    # Ensure value column is float64
    df_box['value'] = df_box['value'].astype(np.float64)

    # Debugging, print data types
    #print(df_box.dtypes)

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Sort 'year' column before plotting
    df_box['year'] = pd.Categorical(df_box['year'], categories=sorted(df_box['year'].unique()), ordered=True)

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0]) #Note this wont work unless you have updated seaborn numpy*******
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    
    plt.tight_layout()
    plt.savefig('box_plot.png')
    return fig