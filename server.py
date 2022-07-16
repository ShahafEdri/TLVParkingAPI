from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from parking_manager import ParkingTLV
from validate import Validate


app = Flask(__name__)
api = Api(app)

v = Validate()
p = ParkingTLV()


class ClassRouteOne(Resource):
    def get(self, name):
        if(v.validate_request(name)):
            response = p.get_parking_space_tonnage(name)
            return response, 200
        else:
            return 400

    def post(self):
        pass

    def delete(self):
        pass


class ClassRouteTwo(Resource):
    def get(self):
        return "check", 200

    def post(self):
        pass

    def delete(self):
        pass


api.add_resource(ClassRouteOne, '/one/')
api.add_resource(ClassRouteTwo, '/two/')


if __name__ == "__main__":
    app.run(debug=True)
