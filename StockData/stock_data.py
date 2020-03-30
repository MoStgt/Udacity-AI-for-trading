#!/usr/bin/env python
# coding: utf-8

# ## Stock Data
# Now that you've had exposure to time series data, let's look at bringing stock prices into Pandas.
# ## Reading in Data
# Your dataset can come in a variety of different formats. The most common format is the [CSV](https://en.wikipedia.org/wiki/Comma-separated_values). We'll use the "prices.csv" file as an example csv file.

# In[1]:


with open('prices.csv', 'r') as file:
    prices = file.read()
    
print(prices)


# The data provider will provide you with information for each field in the CSV. This csv has the fields ticker, date, open, high, low, close, volume, adj_close, adj_volume in that order. That means, the first line in the CSV has the following data:
# 
# - ticker: ABC
# - date: 2017-09-05
# - open: 163.09
# - high: 164.24
# - low: 160.21
# - close: 162.63
# - volume: 29417590.0
# - adj_close: 162.49
# - adj_volume: 29414672.0
# 
# Let's move this data into a DataFrame. For this, we'll need to use the [`pd.read_csv`](https://pandas.pydata.org/pandas-docs/version/0.21.1/generated/pandas.read_csv.html) function. This allows you generate a DataFrame from CSV data.

# In[2]:


import pandas as pd

price_df = pd.read_csv('prices.csv')

price_df


# That generated a DataFrame using the CSV, but assumed the first row contains the field names. We'll have to supply the function's parameter `names` with a list of fiels names.

# In[3]:


price_df = pd.read_csv('prices.csv', names=['ticker', 'date', 'open', 'high', 'low',
                                             'close', 'volume', 'adj_close', 'adj_volume'])

price_df


# ## DataFrame Calculations
# Now that we have the data in a DataFrame, we can start to do calculations on it. Let's find out the median value for each stock using the [`DataFrame.median`](https://pandas.pydata.org/pandas-docs/version/0.21/generated/pandas.DataFrame.median.html) function.

# In[4]:


price_df.median()


# That's not right. Those are the median values for the whole stock universe. We'll use the [`DataFrame.groupby`](https://pandas.pydata.org/pandas-docs/version/0.21/generated/pandas.DataFrame.groupby.html) function to get mean for each stock.

# In[5]:


price_df.groupby('ticker').median()


# That's what we're looking for! However, we don't want to run the `groupby` function each time we make an operation. We could save the GroupBy object by doing `price_df_ticker_groups = price_df.groupby('ticker')`. This limits us to the operations of GroupBy objects. There's the [`GroupBy.apply`](https://pandas.pydata.org/pandas-docs/version/0.21/generated/pandas.core.groupby.GroupBy.apply.html), but then we lose out on performance. The true problem is the way the data is represented.

# In[6]:


price_df.iloc[:16]


# Can you spot our problem? Take a moment to see if you can find it.
# 
# The problem is between lines [6, 7] and  [13, 14]

# In[7]:


price_df.iloc[[6, 7, 13, 14]]


# Data for all the tickers are stacked. We're representing 3 dimensional data in 2 dimensions. This was solved using Panda's Panels, which is [deprecated](https://pandas.pydata.org/pandas-docs/version/0.21.0/dsintro.html#deprecate-panel). The Pandas documentation recommends we use either [MultiIndex](https://pandas.pydata.org/pandas-docs/version/0.21/advanced.html) or [xarray](http://xarray.pydata.org/en/stable/). [MultiIndex](https://pandas.pydata.org/pandas-docs/version/0.21/advanced.html) still doesn't solve our problem, since the data is still represented in 2 dimensions. [xarray](http://xarray.pydata.org/en/stable/) is able to store 3 dimensional data, but Finance uses Pandas, so we'll stick with this library. After you finish this program, I recommend you check out [xarray](http://xarray.pydata.org/en/stable/).
# 
# So, how do we use our 3-dimensional data with Pandas? We can split each 3rd dimension into it's own 2 dimension DataFrame. Let's take this array as an example:
# ```
# [
#     [
#         [ 0,  1],
#         [ 2,  3],
#         [ 4,  5]
#     ],[
#         [ 6,  7],
#         [ 8,  9],
#         [10, 11]
#     ],[
#         [12, 13],
#         [14, 15],
#         [16, 17]
#     ],[
#         [18, 19],
#         [20, 21],
#         [22, 23]
#     ]
# ]    
# ```
# We want to split it into these two 2d arrays:
# ```
# [
#     [0, 2, 4],
#     [6, 8, 10],
#     [12, 14, 16],
#     [18, 20, 22]
# ] 
# [
#     [1, 3, 5],
#     [7, 8, 11],
#     [13, 15, 17],
#     [19, 21, 23]
# ] 
# ```
# In our case, our third dimensions are "open", "high", "low", "close", "volume", "adj_close", and  "adj_volume". We'll use the [`DataFrame.pivot`](https://pandas.pydata.org/pandas-docs/version/0.21/generated/pandas.DataFrame.pivot.html) function to generate these DataFrames.

# In[8]:


open_prices = price_df.pivot(index='date', columns='ticker', values='open')
high_prices = price_df.pivot(index='date', columns='ticker', values='high')
low_prices = price_df.pivot(index='date', columns='ticker', values='low')
close_prices = price_df.pivot(index='date', columns='ticker', values='close')
volume = price_df.pivot(index='date', columns='ticker', values='volume')
adj_close_prices = price_df.pivot(index='date', columns='ticker', values='adj_close')
adj_volume = price_df.pivot(index='date', columns='ticker', values='adj_volume')

open_prices


# That gives you DataFrames for all the open, high low, etc.. Now, what we have been waiting for.. The mean for each ticker.

# In[9]:


open_prices.mean()


# We can also get the mean for each date by doing a transpose.

# In[10]:


open_prices.T.mean()


# It doesn't matter whether date is the index and tickers are the colums or the other way around. It's always a transpose away. Since we're going to do a lot of operations across dates, we will stick with date as the index and tickers as the colums throughtout this program.
# ## Quiz
# Let's see if you can apply what you learned. Implment the `csv_to_close` function to take in a filepath, `csv_filename`, and output the close 2d array. You can assume the CSV file used by `csv_to_close` has the same field names as "prices.csv" and in the same order.
# 
# To help with your implemention of quizzes, we provide you with unit tests to test your function implemention. For this quiz, we'll be using the function `test_csv_to_close` in the `quiz_tests` module to test `csv_to_close`.

# In[13]:


import quiz_tests


def csv_to_close(csv_filepath, field_names):
    """Reads in data from a csv file and produces a DataFrame with close data.
    
    Parameters
    ----------
    csv_filepath : str
        The name of the csv file to read
    field_names : list of str
        The field names of the field in the csv file

    Returns
    -------
    close : DataFrame
        Close prices for each ticker and date
    """
    
    # TODO: Implement Function
    price_df = pd.read_csv(csv_filepath, names=field_names)
    close_prices = close_df.pivot(index='date', columns='ticker', values='close')
    
    return close_prices


quiz_tests.test_csv_to_close(csv_to_close)


# ## Quiz Solution
# If you're having trouble, you can check out the quiz solution [here](stock_data_solution.ipynb).
