from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import psycopg2, hmac
from hashlib import sha256
from datetime import datetime

app = Flask(__name__, instance_relative_config=True)
api = Api(app)

app.config.from_pyfile('config.py')


conn_string = app.config["POSTGRES_URI"]


def insertIntoDatabase(args):
	conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
	values = "("+str(args['station_id'])+",'"+str(datetime.now())+"',"+str(args['temperature'])+","+str(args['windspeed'])+")"
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
	parser.add_argument('station_id',type=int,required=True)
	parser.add_argument('station_time',type=long,required=True)
	parser.add_argument('hmac_digest',type=str,required=True)
	args = parser.parse_args()
	key = "unitkey"
	message = str(args['station_id'])+str(args['temperature'])+str(args['windspeed'])+str(args['station_time'])
	hash_digest = hmac.HMAC(key, message, sha256).hexdigest()
	if hmac.compare_digest(hash_digest, args['hmac_digest']):
		insertIntoDatabase(args)
	

api.add_resource(addData, '/')

if __name__ == '__main__':
    app.run(debug=True)
