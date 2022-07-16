from flask import Flask
from flask import request

from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from parking_manager import ParkingTLV
from validate import Validate


app = Flask(__name__)
api = Api(app)

v = Validate()
p = ParkingTLV()


class One():
    def check():
        print("check")


class Server():
    def __init__(self) -> None:
        self.cls_root = 'parking/'

    @app.route('/one/<name>', methods=('GET', 'POST'))
    def routeone(self=None, name: str = None):
        if request.method == 'GET':
            if(v.validate_request(name)):
                response = p.get_parking_space_tonnage(name)
                return response, 200
            else:
                return 400

    # @app.route('/two/')

    @app.route('/two/', methods=('GET', 'POST'))
    def routetwo(self=None):
        # self.cls_root
        if request.method == 'GET':
            return ("this is response from two", 200)
        return ("check", 200)


if __name__ == "__main__":
    app.run(debug=True)
