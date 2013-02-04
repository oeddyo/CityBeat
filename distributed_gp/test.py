import time
import csv
import sys

from utility.prediction_interface import PredictionInterface
from utility.region import Region

pi = PredictionInterface(    )
pi.setDB('citybeat')
pi.setCollection('prediction_10by10')

region = Region([
    40.7303206,-73.9981039,40.743583799999996,-73.9780882
    ]
    )
print pi.getNearestPrediction(region, "1355313600")


