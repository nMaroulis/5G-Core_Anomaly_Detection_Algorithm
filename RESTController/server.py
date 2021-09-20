from flask import Flask, request
from flask_restful import Resource, Api
from tensorflow.keras.models import load_model
import logging
import numpy as np
from sklearn.externals import joblib

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
api = Api(app)

# load the model
model = load_model('models/model.h5')
# load the scaler
scaler = joblib.load('models/scaler.save')

behaviors = {'0': 'Suspicious Behavior', '1': 'Suspicious Behavior', '2': 'Normal Behavior', '3': 'Anomalous Behavior'}

SERVER_IP = ""
SERVER_PORT = ""

class PredictionModel(Resource):
    def post(self):
        measurements = request.json['ran_meas']
        received_feature = [measurements['ul_delay'],
                            measurements['dl_delay'],
                            measurements['lost_packets'],
                            measurements['cell_id'],
                            measurements['rsrp'],
                            measurements['ulrx_cell'],
                            measurements['transfer_protocol']]
        received_feature = np.asarray([received_feature])
        received_feature_scaled = scaler.transform(received_feature)
        res = int(np.argmax(model.predict(received_feature_scaled), axis=-1)[0])
        behavior = behaviors[str(res)]
        return {'timestamp': measurements['timestamp'], 'predicted_cluster': res, 'behavior': behavior}


api.add_resource(PredictionModel, '/measurements')

if __name__ == '__main__':
    app.run(host=SERVER_IP, port=SERVER_PORT)
