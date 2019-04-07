from flask import Flask
from flask_restful import Resource, Api
import os
import json
#from arbitrage import arbitrage

app = Flask(__name__)
api = Api(app)

path = './time_data/'
files = os.listdir(path)

def truncate(elem):
    return int(elem[0:-5])

sorted_files = sorted(files, key=truncate)


class MarketTimeData(Resource):

    def get(self):
        # we are deleting things off this list
        # and we probably shouldn't be
        curr_file = sorted_files[0]
        sorted_files.pop(0)
        curr_path = path + curr_file
        with open(curr_path, 'r') as infile:
            curr_market_time_data = json.load(infile)
        return curr_market_time_data

#class ArbitrageCycle(Resource):

 #   def get(self):
  #      path, rates = arbitrage('Liquid/ETH')
   #     return json.dumps(path)

api.add_resource(MarketTimeData, '/data')
#api.add_resource(ArbitrageCycle, '/cycle')


if __name__ == '__main__':
    app.run(debug=True)
