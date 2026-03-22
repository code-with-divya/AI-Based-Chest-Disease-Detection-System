import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename
        self.model = load_model("Artifacts/Model_Training/Trained_Model.h5")

    def predict(self):   #  correct indentation
        test_image = image.load_img(self.filename, target_size=(224,224))
        test_image = image.img_to_array(test_image)

        test_image = test_image / 255.0
        test_image = np.expand_dims(test_image, axis=0)

        result = self.model.predict(test_image)[0][0]

        print("Prediction value:", result)

        if result > 0.5:
            prediction = "Adenocarcinoma Cancer"
            confidence = result * 100
        else:
            prediction = "Normal"
            confidence = (1 - result) * 100

        return [{
            "image": prediction,
            "confidence": round(confidence, 2)
        }]