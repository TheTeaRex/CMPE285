from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import datetime
import pytz
import requests


yf.pdr_override()


class NoInternetConnection(Exception):
    pass


class NoSuchTicker(Exception):
    pass


def get_datetime_now(tz='America/Los_Angeles'):
    return datetime.datetime.now(pytz.timezone(tz))

def get_current_date_and_time():
    now = get_datetime_now() 
    return now.strftime('%a %b %d %H:%M:%S %Z %Y')

def get_current_date():
    now = get_datetime_now() 
    return now.strftime('%Y-%m-%d')

def get_tomorrow_date():
    tomorrow = get_datetime_now() + datetime.timedelta(days=1)
    return tomorrow.strftime('%Y-%m-%d')

def get_x_days_back(days):
    old = get_datetime_now() - datetime.timedelta(days=days)
    return old.strftime('%Y-%m-%d')

def get_range(symbol, start=None, end=None):
    if start is None or end is None:
        start = get_current_date()
        end = get_tomorrow_date()
    try:
        data = pdr.get_data_yahoo(symbol, start=start, end=end)
    except requests.exceptions.ConnectionError as e:
        raise NoInternetConnection()
    if len(data) == 0:
        raise NoSuchTicker('Invalid Ticker: {}'.format(symbol.upper()))
    return data

def parse_data(data):
    result = []
    for index, row in data.iterrows():
        item = {}
        item['date'] = index
        item['open'] = row['Open']
        item['high'] = row['High']
        item['low'] = row['Low']
        item['close'] = row['Close']
        item['adj_close'] = row['Adj Close']
        item['volume'] = row['Volume']
        result.append(item)
    return result
