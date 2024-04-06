# Ubaid Mahmood
# S1906881

# Import Libraries
import tensorflow as tf
from keras.callbacks import TensorBoard as tb
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator
import os
import cv2
from sklearn.model_selection import train_test_split
import pickle
import matplotlib.pyplot as plt
import numpy as np
import mtcnn.mtcnn

# This class configures the GenderDetection model, required for pipeline.
# 
class GenderDetection:

    image = None

    # This function configures the ML model.
    # Return model - the gender detection model. 
    # 
    def config_model(self):
        
        # This loads in the data.
        data = open("data/wiki_data.pickle", "rb")
        data = pickle.load(data)
        open("data/wiki_data.pickle", "rb").close()

        datagen = ImageDataGenerator(zoom_range=0.15, width_shift_range=0.2, height_shift_range=0.2, shear_range=0.15,
                                     horizontal_flip=True)

        images = np.array(data['images'])
        genders = np.array(data['gender'])

        print('''The shape of the images array is : {}\n
                The shape is an image is : {}\n
                The shape of the gender array is : {}'''.format(images.shape, images[0].shape, genders.shape))
        
        # Deletes certain variables to clear up unnecessary space.
        del data


        # This makes the amount of female and male in the dataset equal.
        f = 0
        m = 0
        index = 0
        mod_genders = []
        mod_images = []
        males_images = []
        males_genders = []
        for z in genders:
            if z == 0.0:
                mod_images.append(images[index])
                mod_genders.append(genders[index])
                f += 1
            elif m <= f:
                mod_images.append(images[index])
                mod_genders.append(genders[index])
                males_images.append(images[index])
                males_genders.append(genders[index])
                m += 1

            index += 1

        # Deletes certain variables to clear up unnecessary space.
        del images, genders

        mod_images = np.array(mod_images)
        mod_genders = np.array(mod_genders)

        print(f'This is the number of females: {f}')
        print(f'This is the number of males: {m}')

        print(f'This is the length of modded genders var: {len(mod_genders)}')
        print(f'This is the length of modded images var: {len(mod_images)}')

        print('''The shape of the images array is : {}\n
                The shape is an image is : {}\n
                The shape of the gender array is : {}'''.format(mod_images.shape, mod_images[0].shape,
                                                                mod_genders.shape))

        genderCategorical = []

        # Performs One-hot encoding for genders, male and female.
        for i in mod_genders:
            if i[0] == 1:
                genderCategorical.append([1.0, 0.0])
            else:
                genderCategorical.append([0.0, 1.0])
        genderCategorical = np.array(genderCategorical)
        
        # Deletes certain variables to clear up unnecessary space.
        del mod_genders

        # This method splits the data into 80:20 for train and val, then 80:20 for train and test.
        train_images, val_images, train_gender, val_gender = train_test_split(mod_images, genderCategorical,
                                                                              test_size=.2, shuffle=True,
                                                                              random_state=10)

        train_images, test_images, train_gender, test_gender = train_test_split(train_images, train_gender,
                                                                                test_size=.2, shuffle=True,
                                                                                random_state=10)
        
        # Deletes certain variables to clear up unnecessary space.
        del val_gender, val_images, mod_images, genderCategorical
        
        # This file has a model that achieves 92.15% accuracy.
        file = "models/new_model_vgg16(7).json"
        fileJson = "models/new_model_vgg16(7).json"
        fileH5 = "models/new_model_vgg16(7).h5"
        
        print(f'The model being utilised is: {file}')

        # If file exists then configure the model, else throw FileNotFoundError Exception. 
        if os.path.exists(file):
            
            json_file = open(fileJson, 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)
            # load weights into new model
            loaded_model.load_weights(fileH5)
            model = loaded_model
            print("Loaded model from disk")

            model.summary()

            print("")

            model.compile(optimizer=tf.keras.optimizers.Adam(0.0001),
                          loss='binary_crossentropy',
                          metrics=['accuracy', tf.keras.metrics.Recall(),
                               tf.keras.metrics.Precision()])

            # This is testing on the same dataset but on unseen data, this achieves the highest accuracy.
            print("\nEvaluating the Model\n")
            results = model.evaluate(test_images, test_gender)

            print(f'Test Acc: {results[1]}\n'
                f'Test Recall: {results[2]}\n'
                f'Test Precision: {results[3]}\n')
            print('')
            print(f'F1-Score: {2 * (results[3] * results[2]) / (results[3] + results[2])}')
            print()

            del test_gender, test_images, train_gender, train_images, loaded_model, datagen
        
        else:
            raise FileNotFoundError('File does not exists!!!')
        
        return model
    
    # This function extracts faces from the specified image.
    # Return faces - this array contains all the faces identified.
    # 
    def extract_faces(self, img):

        cnn_face_detector = mtcnn.MTCNN()
        faces_cnn = cnn_face_detector.detect_faces(img)
        faces = []
        if (len(faces_cnn) > 0):
            for face in faces_cnn:

                x, y, width, height = face['box']
                print("face", x, y, width, height)

                face_img = tf.image.crop_to_bounding_box(img,
                                                         y, x,
                                                         height, width)

                face_img = tf.image.resize(face_img, (32, 32), method=tf.image.ResizeMethod.BICUBIC, antialias=True)

                face_img = tf.dtypes.cast(face_img, tf.int32)
                faces.append(
                    {'face': face_img.numpy(), 'coordinates': [x, y, width, height]}
                )

        return faces

    # This function displays the image with the predicted gender.
    # 
    def show_output(self, img, faces, predictions):

        for i, data in enumerate(faces):
            coordinates = data['coordinates']
            x1 = coordinates[0]
            y1 = coordinates[1]
            x2 = coordinates[2] + x1
            y2 = coordinates[3] + y1
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
            gender = 'Male' if np.argmax(predictions[i]) == 0 else 'Female'
            cv2.putText(img, gender, (x1 - 3, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
        plt.imshow(img)
        plt.show()

    # This method states if the model predicted male or female.
    # Return gender - This is the gender predicted by the model.
    # 
    def predicted_gender(self, prediction):
        gender = None

        print(f'\n'
              f'Gender prediction: {prediction}')

        if prediction[0] > prediction[1]:
            print(f'Its a Male')
            gender = "Male"
        else:
            print(f'Its a Female')
            gender = "Female"

        return gender

    # After the model is configured, this method is invoked to run the model.
    # Return prediction_gender - This is the predicted gender.
    # 
    def run(self, model, ran_img):

        faces = self.extract_faces(ran_img)

        prediction_gender = None

        predict_X = []
        for face in faces:
            predict_X.append(face['face'])

        predict_X = np.array(predict_X)

        predictions = []
        if predict_X.shape[0] > 0:
            predictions = model.predict(predict_X)

        print(f'This is the prediction guess of it being female or male: \n'
              f'{predictions}')
        frame = ran_img.copy

        if len(predictions) == 0:
            print(f'list is empty')
        else:

            prediction_gender = self.predicted_gender(predictions[0])

        # Deletes certain variables to clear up unnecessary space.
        del predict_X, faces, frame, predictions

        return prediction_gender

