from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return jsonify({'message': 'Flask SQLAlchemy Lab 1'}), 200

@app.route('/earthquakes/<int:id>')
def earthquake_id(id):
    try:
        earthquake = Earthquake.query.get(id)
        if earthquake:
            response_body = {
                'id': earthquake.id,
                'magnitude': earthquake.magnitude,
                'location': earthquake.location,
                'year': earthquake.year
            }
            response_status = 200
        else:
            response_body = {'message': f'Earthquake {id} not found.'}
            response_status = 404
    except Exception as e:
        response_body = {'message': str(e)}
        response_status = 500

    return jsonify(response_body), response_status

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    try:
        # Query earthquakes with magnitude greater than or equal to the specified value
        earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

        # Prepare response data
        quakes_list = [{
            'id': quake.id,
            'magnitude': quake.magnitude,
            'location': quake.location,
            'year': quake.year
        } for quake in earthquakes]

        response_body = {
            'count': len(quakes_list),
            'quakes': quakes_list
        }
        response_status = 200
    except Exception as e:
        response_body = {'message': str(e)}
        response_status = 500

    return jsonify(response_body), response_status

if __name__ == '__main__':
    app.run(port=5555, debug=True)
