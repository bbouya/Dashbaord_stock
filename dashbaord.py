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
    df = pd.read_csv('data/stock.csv', header = None)
    df.rename(columns = {0:'Stock Name',
                }) 