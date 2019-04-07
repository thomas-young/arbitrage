import json
import os

markets = ['Bitfinex', 'Kucoin', 'BitMEX', 'Binance', 'Huobi', 'Bithumb', 'Liquid', 'Coinbase', 'Deribit', 'Kraken']
coins = ['BTC', 'ETH', 'XRP', 'XLM', 'EOS', 'LTC', 'ADA', 'XMR', 'DASH', 'TRX']

def reformat():
    path = './data/'
    time_data_path = './time_data/'
    if not os.path.exists(time_data_path):
        os.makedirs(time_data_path)

    for market in markets:
        print(market)
        market_path = path + market
        for coin in coins:
            print(" ")
            print(coin)
            coin_path = market_path + '/' + coin + '_data.json'
            with open(coin_path, 'r') as infile:
                curr_market_coin_data = json.load(infile)
            for entry in curr_market_coin_data:
                curr_time = entry['time']
                curr_price = entry['close']
                #print(curr_time)
                time_path = './time_data/' + str(curr_time) + '.json'
                if not os.path.exists(time_path):
                    infile = open(time_path, 'w+')
                    curr_json_data = {}
                    curr_json_data[market] = [[coin, curr_price]]
                    json.dump(curr_json_data, infile)
                    infile.close()

                else:
                    infile = open(time_path, 'r')
                    curr_json_data = json.load(infile)
                    if market not in curr_json_data.keys():
                        curr_json_data[market] = [[coin, curr_price]]
                    else:
                        coin_price_list = curr_json_data[market]
                        coin_price_list.append([coin, curr_price])
                        curr_json_data[market] = coin_price_list
                    infile.close()
                    infile = open(time_path, 'w')
                    json.dump(curr_json_data, infile)
                    infile.close()






reformat()