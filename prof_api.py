from flask import Flask
from flask_restful import Resource, Api
import os
import json

app = Flask(__name__)
api = Api(app)

path = './prof_data/'
files = os.listdir(path)

def truncate(elem):
    return int(elem[0:-5])

sorted_files = sorted(files, key=truncate)


class MarketTimeData(Resource):

    def get(self):
        # we are deleting things off this list
        # and we probably shouldn't be
        curr_file = files[0]
        curr_path = path + curr_file
        with open(curr_path, 'r') as infile:
            prof_data = json.load(infile)
        return prof_data


api.add_resource(MarketTimeData, '/professors')


if __name__ == '__main__':
    app.run(debug=True)
