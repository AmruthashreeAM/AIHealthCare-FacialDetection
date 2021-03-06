''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''
from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api
import cv2 as cv2
import numpy as np
import os 
import json

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/facialRecognition')
def facialRecognition():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('./trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);

    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0

    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'Omar', 'Anish', 'Amrutha', 'Soumya', 'Omkar', 'Tushar', 'Hassan', 'Shannon', 'Gauhar'] 

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    while True:

        ret, img =cam.read()
        #img = cv2.flip(img, -1) # Flip vertically

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.1,
            minNeighbors = 10,
            minSize = (int(minW), int(minH)),
        )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            print(id, confidence)

            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 80):
                id = names[id]
                # if id == username
                # print(str(id))
                confidence = "  {0}%".format(round(100 - confidence))
                response = json.dumps({'identifiedPateintName': id})
                return response
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
        
        cv2.imshow('camera',img) 

        # k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        # if k == 27:
        #     break

    # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cam.release()
            cv2.destroyAllWindows()



if __name__ == '__main__':
    app.run(host="localhost", port=5001)
   