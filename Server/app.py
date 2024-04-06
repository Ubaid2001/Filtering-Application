# Ubaid Mahmood
# S1906881

# This is the initiation of a Flask server, the Client-side sends requests to the server in the form of http.

# importing libraries
import sys
import tensorflow as tf
import numpy as np
import os
import cv2

from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from model_configs.GenderDetection import GenderDetection
from model_configs.ClothesDetection import ClothesDetection
from model_configs.Movenet import Movenet
# from blueprints.fileupload import fileupload_bp

# This will remove the warnings from tensorflow about AVX
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# This checks current library versions.
# It also verifies if the interpreter is using a GPU. 
print(f"Tensor Flow Version: {tf.__version__}")
print(f"Keras Version: {tf.keras.__version__}")
print("")
print(f"Python {sys.version}")
gpu = len(tf.config.list_physical_devices('GPU')) > 0
print("GPU is", "available" if gpu else "NOT AVAILABLE")
print("")


app = Flask(__name__)
# app.register_blueprint(fileupload_bp)

# The enable and block print methods, disables or enables any information from being printed in the terminal.
# 
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

# This function determines if the image should be blocked, according to specific standards. 
def block_image(result1, result2, gender):
    isBlock = False

    # This is for DC11 images
    if gender == "Male":
        print(f'This is a Male')
        if result1 == "Innerwear Vests" or result1 == "No Clothing Item":
            print(f'This is image is BLOCKED!!!!!!!!!')
            print(f'Blocked beacause male is wearing: {result1}')
            isBlock = True

        if result2 == "Briefs" or result2 == "Trunk" or result2 == "Boxers" or result2 == "No Clothing Item" \
                or result2 == "Shorts":
            print(f'This is image is BLOCKED!!!!!!!!!')
            print(f'Blocked beacause male is wearing: {result2}')
            isBlock = True
    elif gender == "Female":
        print(f'This is a Female')
        if result1 == "Bra" or result1 == "Innerwear Vests" or result1 == "No Clothing Item":
            print(f'This is image is BLOCKED!!!!!!!!!')
            print(f'Blocked beacause female is wearing: {result1}')
            isBlock = True

        if result2 == "Shorts" or result2 == "Briefs" or result2 == "Trunk" or result2 == "Boxers" \
                or result2 == "Boxers" or result2 == "Leggings" or result2 == "No Clothing Item":
            print(f'This is image is BLOCKED!!!!!!!!!')
            print(f'Blocked beacause female is wearing: {result2}')
            isBlock = True
    
    return isBlock


# @app.route('/')
# def hello():
#     return 'The Name is, Ubby G Outlaws!'


# Constructs the paths, which the images will be saved.
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder


# This is the Image endpoint.
# This endpoint receives Post requests.
# In the function, the image is received and saved.
# Image preprocessing is performed, Image is passed into the pipeline to determine if the image is appropriate. 
# Return response - states whether the image is appropriate or not.
@app.route('/Image', methods=['POST'])
def upload_image():

    global isBlock

    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        print(img)

        frame = cv2.imread(f'{img}')
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame2 = frame.copy()

        # Predicts the gender of the person.
        predicted_gender = gender_detection.run(Gmodel, frame)

        blockPrint()
        predicted_gender = gender_detection.run(Gmodel, frame)

        if predicted_gender is not None:
            # This method returns and image of the upperbody and lowerbody of the person.
            image1, image2 = pose_model.get_image(frame2)
            enablePrint()

            if image1 is not None and image2 is not None:

                # Makes prediction on the clothes the perosn in wearing. 
                blockPrint()
                res1, preds1 = clothes_detection.make_prediction(image1, Cmodel)
                res2, preds2 = clothes_detection.make_prediction(image2, Cmodel)
                enablePrint()


                print(f'res1 - {res1} \n'
                      f'res2 - {res2}')

                # Determins if the image should be blocked.
                isBlock = block_image(res1, res2, predicted_gender)
     

            else:
                print(f'\n'
                      f'Since, image1 and image2 is None\n'
                      f'Clothes Detection cannot advance\n'
                      f'Find another full body image\n'
                      f'\n')
        else:
            print(f'prediction is None')

        print(f'isBlock: {isBlock}\n'
                f'\n')
        
        # return 'Image Delivered'
        response = jsonify([f'Image is Blocked: {isBlock}'])
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    

    response = jsonify(['Image Not Delivered'])
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':

    # Configures all the models required for the pipeline.
    gender_detection = GenderDetection()
    Gmodel = gender_detection.config_model()

    pose_model = Movenet()

    clothes_detection = ClothesDetection()
    Cmodel = clothes_detection.config_model()
    
    # fileupload(Gmodel)

    # app.run(debug=True)
    

    app.run()
