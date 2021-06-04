from flask import Flask, request, render_template
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Api, Resource
import keras.preprocessing.image as keras_pre_img
import tensorflow as tf
from keras.models import load_model
import numpy as np

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

labels = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
MODEL_PATH = 'model/model.h5'
model = load_model(MODEL_PATH, compile=False)

class Predict_Json(Resource):
    def post(self):
        img = request.files['img']
        img.save("temp/img.jpg")
        img = keras_pre_img.load_img("temp/img.jpg", target_size=(180, 180))
        img_array = keras_pre_img.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        # print(
        #     "This image most likely belongs to {} with a {:.2f} percent confidence."
        #     .format(labels[np.argmax(score)], 100 * np.max(score))
        # )

        return {"labels": str(labels[np.argmax(score)]),"accuracy": str(np.max(score))}

api.add_resource(Predict_Json, "/json-predict")

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return render_template("index.html")

    elif flask.request.method == 'POST':
        img = request.files['img']
        img.save("temp/img.jpg")
        img = keras_pre_img.load_img("temp/img.jpg", target_size=(180, 180))
        img_array = keras_pre_img.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        # print(
        #     "This image most likely belongs to {} with a {:.2f} percent confidence."
        #     .format(labels[np.argmax(score)], 100 * np.max(score))
        # )

        return render_template("index.html", data=labels[np.argmax(score)], data2=100 * np.max(score))

# @app.route("/predict", methods=["POST"])
# def prediction():
#     img = request.files['img']
#     img.save("temp/img.jpg")
#     img = keras_pre_img.load_img("temp/img.jpg", target_size=(180, 180))
#     img_array = keras_pre_img.img_to_array(img)
#     img_array = tf.expand_dims(img_array, 0)

#     predictions = model.predict(img_array)
#     score = tf.nn.softmax(predictions[0])

#     # print(
#     #     "This image most likely belongs to {} with a {:.2f} percent confidence."
#     #     .format(labels[np.argmax(score)], 100 * np.max(score))
#     # )

#     return render_template("index.html", data=labels[np.argmax(score)], data2=100 * np.max(score))

# @app.route("/json-predict", methods=["POST"])
# def json_predict():
#     img = request.files['img']
#     img.save("temp/img.jpg")
#     img = keras_pre_img.load_img("temp/img.jpg", target_size=(180, 180))
#     img_array = keras_pre_img.img_to_array(img)
#     img_array = tf.expand_dims(img_array, 0)

#     predictions = model.predict(img_array)
#     score = tf.nn.softmax(predictions[0])

#     # print(
#     #     "This image most likely belongs to {} with a {:.2f} percent confidence."
#     #     .format(labels[np.argmax(score)], 100 * np.max(score))
#     # )

#     return {"labels": str(labels[np.argmax(score)]),"accuracy": str(np.max(score))}

if __name__ == "__main__":
    app.run(debug=True)
