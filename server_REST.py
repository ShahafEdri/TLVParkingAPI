from asyncio import Server
from logging import INFO, WARNING, FileHandler, Formatter

from flask import Flask, request
from flask_apscheduler import APScheduler
from flask_restful import Api, Resource, reqparse

from db.db_manager import DBManager
from parking.parking_manager import ParkingManager
from utils.logging_utils import FORMAT2

scheduler = APScheduler()

app = Flask(__name__)
api = Api(app)


file_handler = FileHandler('server_REST.log', mode='a',)
file_handler.setLevel(WARNING)
file_handler.setFormatter(Formatter(FORMAT2))
app.logger.addHandler(file_handler)
app.logger.setLevel(INFO)


# cron.start()
# crontab.every(1).month.do(Parking.update_all_parking_space_information)

p = ParkingManager()
dbm=DBManager()

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

def update():
    app.logger.critical('Server started')



if __name__ == "__main__":
    scheduler.add_job(id='update_db_tonnage', func=dbm.update_all_parking_spaces_tonnages_seqential, trigger='interval', minutes=10)
    scheduler.start()
    
    app.run(debug=True)
