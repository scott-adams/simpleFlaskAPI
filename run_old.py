from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import psycopg2
from datetime import datetime

app = Flask(__name__, instance_relative_config=True)
api = Api(app)

app.config.from_pyfile('config.py')


conn_string = app.config["POSTGRES_URI"]


def insertIntoDatabase(temp,windsp):
	conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
	values = "(2,'"+str(datetime.now())+"',"+str(temp)+","+str(windsp)+")"
	query = "INSERT INTO weather_data VALUES " + values
	cur.execute(query)
	conn.commit()
	cur.close
	conn.close

class addData(Resource):
    def put(self):
	parser = reqparse.RequestParser()
	parser.add_argument('temperature', type=float,required=True)
	parser.add_argument('windspeed', type=float,required=True)
	args = parser.parse_args()

	insertIntoDatabase(args['temperature'],args['windspeed'])
	return args['temperature']
	

api.add_resource(addData, '/')

if __name__ == '__main__':
    app.run(debug=True)
