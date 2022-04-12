from logging import warning
from pickle import NONE
from tkinter import N
import pytz
import datetime
import pandas as pd
import dash_bootstrap_components as dbc 
from dash import Dash, html, dcc, dash_table, Input, Output

import warnings
warnings.filterwarnings('ignore')

IST = pytz.timezone('ignore')

today_date = datetime.datetime.now(IST).strftime('%d-%m-%Y')

app = Dash(__name__)
app.title = 'Stock Alert Dashboard(v1.0)'

def get_filtered_data():
    df = pd.read_csv('data/stock.csv', header=None)
    df.rename(columns={0: 'Stock Name',
                       1: 'Previous Close',
                       2: 'Current Price',
                       3: 'Minimum(Day)',
                       4: 'Maximum(Day)',
                       5: 'Minimum(Year)',
                       6: 'Maximum(Year)',
                       7: 'Minimum(Threshold)',
                       8: 'Maximum(Threshold)',
                       9: 'Last Update',
                       10: 'difference',
                       11: 'difference(%)',
                       12: 'buy',
                       13: 'market',
                       14: 'currency'}, inplace=True)


    columns = ['Stock Name', 'Previous Close', 'Current Price', 'difference', 'difference(%)',
               'Minimum(Day)', 'Maximum(Day)', 'Minimum(Year)', 'Maximum(Year)', 'Minimum(Threshold)', 'Maximum(Threshold)']
    df = df.round(2)
    df['Last Update'] = pd.to_datetime(df['Last Update'])
    lastest_date = df.groupby(['Stock Name'])[
        'Last Update'].max().reset_index()['Last Update']

    filtered_df = df[df['Last Update'].isin(lastest_date)]
    filtered_df.sort_values(by=['difference(%)'], inplace=True, ascending=False)
    filtered_df['difference(%)'] = filtered_df['difference(%)'].apply(lambda x: '{} %'.format(x))
    filtered_df["Last Update"] = filtered_df["Last Update"].apply(lambda x: x.strftime('%H:%M:%S'))
    df["Last Update"] = df["Last Update"].apply(lambda x: x.strftime('%H:%M:%S'))

    indian_stocks = filtered_df[filtered_df['market'] == 'IN']

    buy_table = indian_stocks[indian_stocks['buy'] == True]
    watch_table = indian_stocks[indian_stocks['buy'] == False]

    buy_table = buy_table[columns]
    watch_table = watch_table[columns]

    us_stocks = filtered_df[filtered_df['market'] == 'US']
    us_stocks = us_stocks[columns]

    return df, buy_table, watch_table, us_stocks

def overall_market_data():
    market_data = pd.read_csv('data/market.csv', header=None)
    columns = ['Stock Name', 'Previous Close', 'Current Price', 'difference', 'difference(%)',
               'Minimum(Day)', 'Maximum(Day)', 'Minimum(Year)', 'Maximum(Year)']
    market_data.rename(columns={0: 'Stock Name',
                                1: 'Previous Close',
                                2: 'Current Price',
                                3: 'Minimum(Day)',
                                4: 'Maximum(Day)',
                                5: 'Minimum(Year)',
                                6: 'Maximum(Year)',
                                7: 'Last Update',
                                8: 'difference',
                                9: 'difference(%)'}, inplace=True)
    market_data = market_data.round(2)
    market_data['Last Update'] = pd.to_datetime(market_data['Last Update'])
    lastest_date = market_data.groupby(['Stock Name'])['Last Update'].max().reset_index()['Last Update']
    filtered_df = market_data[market_data['Last Update'].isin(lastest_date)]
    filtered_df = filtered_df[columns]

    return filtered_df, lastest_date[0]