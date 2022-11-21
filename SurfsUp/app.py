#dependencies
import flask as Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)
Measurements = Base.classes.measurement
Station = Base.classes.station
last_date = '2016-08-23'
#creating app through __name__
app = Flask(__name__)

@app.route("/")
def home():
    return ('Available routes:\n/api/v1.0/precipitation\n/api/v1.0/stations\n/api/v1.0/tobs\n/api/v1.0/<start>\n/api/v1.0/<start>/<end>')


# Define what to do when a user hits the /about route
@app.route('/api/v1.0/precipitation')
def precip():
    precip_list = []
    precip_dict ={}
    session = Session(engine)
    precip_data = session.query(Measurements.date,Measurements.prcp).filter(Measurements.date >= last_date).all()
    session.close()
    for date, precip in precip_data:
        precip_dict['Date'] = date
        precip_dict['Precipitation'] = precip
        precip_list.append(precip_dict)
    
        
    return jsonify(precip_list)
        
@app.route('/api/v1.0/stations')
def stations():
    station_list = []
    session = Session(engine)
    station_data = session.query(Station.station).all()
    session.close()
    for station in station_data:
        station_list.append(station)
        
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    active_station_list= []
    active_station_dict={}
    session = Session(engine)
    active_station_data = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date >= last_date).filter(Measurements.station == 'USC00519281').all()
    session.close()
    for date, tobs in active_station_data:
        active_station_dict['Date']= date
        active_station_dict['Tobs'] = tobs
        active_station_list.append(active_station_dict)
    
    return jsonify(active_station_list)
    
@app.route('/api/v1.0/<start>')
def start_route(start):
    temp_dict = {}
    temp_list = []
    session = Session(engine)
    temp_data = session.query(func.min(Measurements.tobs),func.avg(Measurements.tobs),func.max(Measurements.tobs)).filter(Measurements.date >= start).all()
    session.close()
    for mini, aveg, maxi in temp_data:
        temp_dict['Minimum'] = mini
        temp_dict['Average'] = aveg
        temp_dict['Maximum'] = maxi
        temp_list.append(temp_dict)
    
    return jsonify(temp_list)
    
@app.route('/api/v1.0/<start>/<end>')
def start_end_route(start, end):
    temp_dict = {}
    temp_list = []
    session = Session(engine)
    temp_data = session.query(func.min(Measurements.tobs),func.avg(Measurements.tobs),func.max(Measurements.tobs)).filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    session.close()
    for mini, aveg, maxi in temp_data:
        temp_dict['Minimum'] = mini
        temp_dict['Average'] = aveg
        temp_dict['Maximum'] = maxi
        temp_list.append(temp_dict)
    
    return jsonify(temp_list)



if __name__ == "__main__":
    app.run(debug=True)