import os
import mysql.connector
import bcrypt

from Respire.Utils import decodeImage
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, render_template, redirect
from Respire.Pipeline.Prediction_Pipeline import PredictionPipeline

# ENV
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)

# ================= DATABASE CONNECTION =================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",   
    database="chest_db"
)

cursor = db.cursor()

# ================= MODEL =================
class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)

# ================= ROUTES =================

#  LOGIN PAGE FIRST
@app.route("/", methods=['GET'])
def home():
    return redirect('/login')


# ================= REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # HASH PASSWORD
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, hashed_password))
        db.commit()

        return redirect('/login')

    return render_template('register.html')


# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = "SELECT password FROM users WHERE username=%s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user[0]

            # CHECK PASSWORD
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                return render_template('index.html')   # go to main page
            else:
                return " Wrong Password"
        else:
            return " User Not Found"

    return render_template('login.html')


# ================= PREDICT =================
@app.route("/predict", methods=['POST'])
def predictRoute():
    try:
        print("API HIT")

        image = request.json.get('image')

        if image is None:
            return jsonify({"error": "No image received"})

        decodeImage(image, clApp.filename)

        result = clApp.classifier.predict()
        print("Result:", result)

        return jsonify(result)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)})


# ================= RUN =================
if __name__ == "__main__":
    clApp = ClientApp()
    app.run(debug=True, port=5000)