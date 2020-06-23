
# coding=utf-8
import sys
import os
import glob
import re


from keras.models import load_model
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.preprocessing import image

import numpy as np
import cv2



# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer



PEOPLE_FOLDER = os.path.join('static', 'people_photo')
# Define a flask app
app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/', methods=['GET'])
def index():
    # Main page        
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        
        model = load_model('models/model-090.model')
        face_clsfr=cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
        

        
        
        img = cv2.imread(file_path)

        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        labels_dict={0:'MASK',1:'NO MASK'}
        color_dict={0:(0,255,0),1:(0,0,255)}
        
        faces=face_clsfr.detectMultiScale(gray,1.3,5) 
           
        for (x,y,w,h) in faces:
        
            face_img=gray[y:y+w,x:x+w]
            resized=cv2.resize(face_img,(100,100))
            normalized=resized/255.0
            reshaped=np.reshape(normalized,(1,100,100,1))
            result=model.predict(reshaped)
            #print(result)
            label=np.argmax(result,axis=-1)[0]
        
            
            #txt=str(label*100)
            cv2.rectangle(img,(x,y),(x+w,y+h),color_dict[label],2)
            cv2.rectangle(img,(x,y-40),(x+w,y),color_dict[label],-1)
            cv2.putText(img, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.8,(255,255,255),2)
            result=labels_dict[label]
        filename = 'static\people_photo\savedImage.jpg'
        cv2.imwrite(filename, img)
        
        #print(img)
       # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'savedImage.jpg')
        #return render_template('predict.html',user_image= full_filename )
        return result
    return None

    #return render_template('start.html',user_image= full_filename )
if __name__ == '__main__':
    app.run(debug=False)