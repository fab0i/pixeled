from flask import Flask
from flask_restful import Api, Resource

from RgbMatrixLocal import RgbMatrix
import time
import sys
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
api = Api(app)
matrix = RgbMatrix(32, 32)

class ImageDisplay(Resource):
    def get(self):
        return "What?"

    def post(self, action, image):
        matrix.render_gif(image, 0)