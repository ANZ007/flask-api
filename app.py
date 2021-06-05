from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Api, Resource, abort
import os
import tensorflow as tf
import tensorflow.keras.preprocessing.image as keras_pre_img
from tensorflow.keras.models import load_model
import numpy as np
import PIL

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png']
api = Api(app)

labels = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
MODEL_PATH = 'model/model.h5'
model = load_model(MODEL_PATH, compile=False)

class Predict_Json(Resource):
    def post(self):
        if os.path.exists('static/img.jpg'):
            os.remove("static/img.jpg") 
        img = request.files['img']
        fn_img = secure_filename(img.filename)
        if fn_img != '':
            fn_img_ext = os.path.splitext(fn_img)[1]
            if fn_img_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400, message="File Type not Allowed.")
            img.save("static/img.jpg")
            img = keras_pre_img.load_img("static/img.jpg", target_size=(180, 180))
            img_array = keras_pre_img.img_to_array(img)
            img_array = tf.expand_dims(img_array, axis=0)

            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            # print(
            #     "This image most likely belongs to {} with a {:.2f} percent confidence."
            #     .format(labels[np.argmax(score)], 100 * np.max(score))
            # )

            return {"labels": str(labels[np.argmax(score)]),"accuracy": str(np.max(score))}

        else:
            abort(400, message="File Not Found.")

api.add_resource(Predict_Json, "/json-predict")

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        if os.path.exists('static/img.jpg'):
            os.remove("static/img.jpg") 
        return render_template("index.html")

    elif flask.request.method == 'POST':
        img = request.files['img']
        img = request.files['img']
        fn_img = secure_filename(img.filename)
        if fn_img != '':
            fn_img_ext = os.path.splitext(fn_img)[1]
            if fn_img_ext not in app.config['UPLOAD_EXTENSIONS']:
                return render_template("index.html", prediction="File type not Allowed...")
            img.save("static/img.jpg")
            img = keras_pre_img.load_img("static/img.jpg", target_size=(180, 180))
            img_array = keras_pre_img.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)

            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            # print(
            #     "This image most likely belongs to {} with a {:.2f} percent confidence."
            #     .format(labels[np.argmax(score)], 100 * np.max(score))
            # )

            return render_template("index.html", prediction="This image most likely belongs to {} with a {:.2f} % confidence.".format(labels[np.argmax(score)], 100 * np.max(score)))
        else:
            return render_template("index.html", prediction="File Not Found.")

if __name__ == "__main__":
    app.run(debug=True)
