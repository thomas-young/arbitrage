import requests
import json
import random
import pandas as pd
import os
import flask
from time import sleep

good_coins = ['BTC', 'ETH', 'XRP', 'XLM', 'EOS', 'LTC', 'ADA', 'XMR', 'DASH', 'TRX']
markets = ['Bitfinex', 'Kucoin', 'BitMEX', 'Binance', 'Huobi', 'Bithumb', 'Liquid', 'Coinbase', 'Deribit', 'Kraken']
historical_token = '95278ffa593f3e22d3b0608466ee0b8875245bcba090aa1769ea0f1514cb7546'
historical_url_base = 'https://min-api.cryptocompare.com/data/'
historical_data_p1 = 'histominute?fsym='
historical_data_p2 = '&tsym=USD&limit=1000&api_key='


def write_historical_data():
    for coin in good_coins:
        print("fetching historical data for " + coin)
        historical_data_query = historical_url_base + historical_data_p1 + coin + historical_data_p2 + historical_token
        response_histo = requests.get(historical_data_query)
        histo_data = response_histo.json()
        new_histo_data = response_histo.json()
        for datum in histo_data:
            if datum != 'Data':
                new_histo_data.pop(datum)
        directory = './histo'
        if not os.path.exists(directory):
            os.makedirs(directory)
        fileout = './histo/' + coin + '_histo_data.json'
        with open(fileout, 'w') as outfile:
            json.dump(new_histo_data['Data'], outfile)


def parse_histo_json_to_pandas():
    histo_dict = {}
    for coin in good_coins:
        print("Attempting to create dataframe from " + coin + " historical data")
        infile_name = './histo/' + coin + "_histo_data.json"
        with open(infile_name, 'r') as infile:
            curr_histo_data = json.load(infile)
        dataframe = pd.DataFrame.from_dict(curr_histo_data, orient='columns')
        dataframe.drop(['high', 'low', 'open', 'volumefrom', 'volumeto'], axis=1, inplace=True)
        histo_dict[coin] = dataframe
    return histo_dict


def master_modulate_price():

    histo_dfs = parse_histo_json_to_pandas()
    market_dfs = {}
    for market in markets:
        print(" ")
        print(market)
        coin_dfs = {}
        for coin, histo_df in histo_dfs.items():
            print(coin)
            coin_df = histo_df.copy(deep=True)
            for index, row in coin_df.iterrows():
                old_price = row['close']
                variability = random.uniform(0, 2)
                variability = variability / 100
                diff = variability * old_price
                add = random.randint(0,1)
                if add:
                    new_price = old_price + diff
                else:
                    new_price = old_price - diff
                coin_df.at[index, 'close'] = new_price
            coin_dfs[coin] = coin_df
        market_dfs[market] = coin_dfs
    return market_dfs

def master_dfs_to_json(dfs_dict):
    for market, coin_dict in dfs_dict.items():
        for coin, market_coin_df in coin_dict.items():
            output_path = r'./data/' + market + '/' + coin + '_data.json'
            master_directory = './data'
            if not os.path.exists(master_directory):
                os.makedirs(master_directory)

            directory = './data/' + market
            if not os.path.exists(directory):
                os.makedirs(directory)
            open(output_path, 'a')
            print(output_path)
            market_coin_df.to_json(output_path, orient='records')



write_historical_data()
dfs_dict = master_modulate_price()
master_dfs_to_json(dfs_dict)
