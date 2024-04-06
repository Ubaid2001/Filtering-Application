from flask import Blueprint, redirect
from app import gender_detection

fileupload_bp = Blueprint("fileupload", __name__)

@fileupload_bp.route('/')
def hello():
    return 'The Name is, Ubby G Outlaws!'

upload_folder = os.path.join('../static', 'uploads')
app.config['UPLOAD'] = upload_folder

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

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

    # print(f'isBlock: {isBlock}\n'
    #       f'\n')
    
    return isBlock


@fileupload_bp.route('/Image', methods=['POST'])
def upload_image():

    global isBlock

    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        # print(img)

        frame = cv2.imread(f'{img}')
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame2 = frame.copy()

        predicted_gender = gender_detection.run(Gmodel, frame)
        # print(predicted_gender)

        blockPrint()
        predicted_gender = gender_detection.run(Gmodel, frame)

        if predicted_gender is not None:
            image1, image2 = pose_model.get_image(frame2)
            enablePrint()

            if image1 is not None and image2 is not None:

                blockPrint()
                res1, preds1 = clothes_detection.make_prediction(image1, Cmodel)
                res2, preds2 = clothes_detection.make_prediction(image2, Cmodel)
                enablePrint()

                print(f'res1 - {res1} \n'
                      f'res2 - {res2}')

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