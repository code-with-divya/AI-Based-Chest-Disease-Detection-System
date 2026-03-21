import os
from Respire.Utils import decodeImage
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, render_template
from Respire.Pipeline.Prediction_Pipeline import PredictionPipeline

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)


# Home Route
@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


# Predict Route (FINAL FIX)
@app.route("/predict", methods=['POST'])
def predictRoute():
    try:
        print("API HIT")

        # get base64 image from frontend
        image = request.json.get('image')

        if image is None:
            return jsonify({"error": "No image received"})

        # decode image and save
        decodeImage(image, clApp.filename)
        print("Image decoded")

        # prediction
        result = clApp.classifier.predict()
        print("Result:", result)

        return jsonify(result)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    clApp = ClientApp()
    app.run(debug=True, port=5000)