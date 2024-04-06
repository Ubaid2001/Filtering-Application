# Ubaid Mahmood
# S1906881

# Import Libraries
import numpy
import os
import tensorflow as tf
import sys
import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.models import  model_from_json
from keras.optimizers import Adam
from keras.callbacks import TensorBoard as tb
from keras.preprocessing.image import ImageDataGenerator
import efficientnet.keras as efn

# This class will configure the Clothes Detection model, required for the pipeline.
class ClothesDetection:

    global IMG_SIZE

    # The input size of the image 
    IMG_SIZE = 224

    # The function configures the model.
    # Returns model - the respected model after configuration.
    def config_model(self):

        pickle_file = "data/fashionImagesDC12.pickle"
        # pickle_file = "data/fashionImagesDC13.pickle"


        data = open(pickle_file, "rb")
        data = pickle.load(data)
        open(pickle_file, "rb").close()

        images = np.array(data['images'])
        clothes = np.array(data['clothes'])

        print(f'''The shape of the images array is : {images.shape}\n
                The shape is an image is : {images[0].shape}\n
                The shape of the clothes array is : {clothes.shape}''')
        
        # Deletes certain variables to clear up unnecessary space.
        del data


        # This is for DC12 and DC13 as the classes match
        class_names = ["Tshirts", "Briefs", "Shirts", "Shorts", "Jeans", "Tops", "Trousers", "Bra", "Track Pants",
                        "Innerwear Vests"]


        datagen_val = ImageDataGenerator(data_format='channels_last', preprocessing_function=efn.preprocess_input)

        clothesCategorical = []

        # This is for DC12 and DC13 pickle files
        # One-hot encodes the specified categories.
        for i in clothes:
            if i == "Tshirts":
                clothesCategorical.append([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif i == "Briefs":
                clothesCategorical.append([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif i == "Shirts":
                clothesCategorical.append([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif i == "Shorts":
                clothesCategorical.append([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif i == "Jeans":
                clothesCategorical.append([0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif i == "Tops":
                clothesCategorical.append([0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
            elif i == "Trousers":
                clothesCategorical.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
            elif i == "Bra":
                clothesCategorical.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0])
            elif i == "Track Pants":
                clothesCategorical.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0])
            elif i == "Innerwear Vests":
                clothesCategorical.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
        clothesCategorical = np.array(clothesCategorical)


        batch_size = 64

        # This method partitions the data into 80:20 train and val, then 80:20 traina and test.
        train_images, val_images, train_clothes, val_clothes = train_test_split(images, clothesCategorical,
                                                                                test_size=.2, shuffle=True,
                                                                                random_state=10)

        train_images, test_images, train_clothes, test_clothes = train_test_split(train_images, train_clothes,
                                                                                test_size=.2, shuffle=True,
                                                                                random_state=10)

        num_train_examples = len(train_images) * 0.8


        print(f"Number of training images samples: {train_images.shape}")
        print(f"Number of training clothes samples: {train_clothes.shape}")
        print(f"Number of test images samples: {test_images.shape}")
        print(f"Number of test clothes samples: {test_clothes.shape}")

        # Deletes certain variables to clear up unnecessary space.
        del clothes, images, val_clothes, val_images, train_clothes, train_images, clothesCategorical


        # This is the model trained with the data generator of DC12 images ver 2.0
        # Changed learning rate to .001
        model_name = "models/new_model_ecnDC12_dg_LTF_v2.json"
        model_h5 = "models/new_model_ecnDC12_dg_LTF_v2.h5"
        
        # # This is the model trained with the data generator of DC13 images
        # # Changed learning rate to .0001
        # model_name = "models/new_model_ecnDC13_dg_LTF.json"
        # model_h5 = "models/new_model_ecnDC13_dg_LTF.h5"
        
        print(f'The model being utilised is: {model_name}')
        
        # If the file exists then model is configured, else FileNotFoundError exception is thrown. 
        if os.path.exists(model_name):
            json_file = open(model_name, 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)

            # load weights into new model
            loaded_model.load_weights(model_h5)
            model = loaded_model
            print("Loaded model from disk")

            loaded_model.summary()

            # optimizer = Adam(learning_rate=0.0001)

            optimizer = Adam(learning_rate=0.001)

            model.compile(optimizer=optimizer,
                            loss='categorical_crossentropy',
                            metrics=['accuracy', tf.keras.metrics.Recall(),
                            tf.keras.metrics.Precision()])

            print("\nEvaluating the Model\n")
            results = model.evaluate(datagen_val.flow(test_images, test_clothes))

            # print("test loss, test acc:", results)

            # print("test loss, test acc, test recall, test precision:", results)
            print(f'Test Acc: {results[1]}\n'
                    f'Test Recall: {results[2]}\n'
                    f'Test Precision: {results[3]}\n')
            print('')
            print(f'F1-Score: {2 * (results[3] * results[2]) / (results[3] + results[2])}')
            print()

            # Deletes certain variables to clear up unnecessary space.
            del loaded_model, test_clothes, test_images, datagen_val

            # return model
            
        else:
            raise FileNotFoundError('File does not exists!!!')

        return model


    # This function, the model produces a prediction based off the input image.
    # Return result, pred
    # result - is the key of clothes_dict
    # pred - is the array of prediction probabilities.
    def make_prediction(self, image, model):

        # print(image.shape)
        nImg = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
        nImg = nImg[np.newaxis, :, :, :]
        # print(nImg.shape)

        nImg = efn.preprocess_input(nImg)
        predictions = model.predict(nImg)
        # predictions = np.round(predictions)
        # print(predictions.shape)
        print(predictions[0])


        # This is for DC12 and DC13 images
        # the elements value is changed to 1.0, if model predicts that element.
        clothes_dict = {"Tshirts": 0, "Briefs": 0, "Shirts": 0, "Shorts": 0, "Jeans": 0, "Tops": 0, "Trousers": 0,
                        "Bra": 0, "Track Pants": 0, "Innerwear Vests": 0, "No Clothing Item": 0}

        index = 0
        pred = np.copy(predictions[0])
        preds = predictions[0]

        largest_pb = max(preds)

        # If prediction probability is not above the .35 threshold then set prediction of No Clothing Item.
        if largest_pb < .35:
            print(f'the largest prediction is less than .35')
            for pb in range(len(preds)):
                    preds[pb] = 0.0
            preds = numpy.append(preds, 1.0)
        else:
            print(f'the largest prediction is greater than .35')
            for pb in range(len(preds)):
                if preds[pb] == largest_pb:
                    preds[pb] = 1.0
                    # print(f'This is the largest value: {c[pb]}, {largest_pb}')
                else:
                    preds[pb] = 0.0
                    # print(f'This is not the largest value: {c[pb]}')
            preds = numpy.append(preds, 0.0)

        for key in clothes_dict:
            clothes_dict[key] = preds[index]
            index += 1

        print(clothes_dict)

        print(len(preds))

        result = ""
        for key in clothes_dict:
            if clothes_dict[key] == 1.0:
                result = key

        print(result)

        return result, pred
