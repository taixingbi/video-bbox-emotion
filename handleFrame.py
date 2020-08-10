import cv2
import numpy as np
from time import sleep
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import datetime
import json

# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class HandleFrame:
    def __init__(self):
        print("HandleFrame init...")
        self.face_classifier = cv2.CascadeClassifier('model/haarcascade_frontalface_alt2.xml')
        self.emotional_classifier = load_model('model/model_70.hdf5')
    
        self.class_labels= {0: 'angry', 1: 'fear', 2: 'happy', 3: 'sad', 4: 'surprised', 5: 'calm'}

    def emotional(self, face):

        if np.sum([face]) != 0.0:

            cv2.imwrite('tmp/face.jpg', face)
            roi = face.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # make a prediction on the ROI, then lookup the class
            preds = self.emotional_classifier.predict(roi)[0]

            preds= [ round(_, 3) for _ in preds]
            print(preds)
            #label = self.class_labels[preds.argmax()]   
            # print("label: ", label)  

            result_emotion= {   "HAPPY": float( preds[2] ),  
                                "CALM": float( preds[5] ),  
                                "SAD": float( preds[3] ),
                                "FEAR": float( preds[1] ),  
                                "ANGRY": float( preds[0] ),  
                                "SURPRISED": float( preds[4])
                            }

            #update anxiety
            result_emotion['ANXIETY']=  result_emotion['FEAR'] + result_emotion['ANGRY']
            return result_emotion

    def visualization(self, Faces, img):

        for Face in Faces:
            bbox= Face['bbox']
            rect= (bbox['x'], bbox['w'], bbox['y'],bbox['h'])

            sentiment= Face['sentiment']

            labels= [   "HAPPY: "+ str(sentiment['HAPPY']*100)[:4]+ '%',  
                        "CALM: "+ str(sentiment['CALM']*100)[:4]+ '%',
                        "SAD: "+ str(sentiment['SAD']*100)[:4]+ '%',
                        # "FEAR: "+ str(sentiment['FEAR']*100)[:4]+ '%',
                        # "ANGRY: "+ str(sentiment['ANGRY']*100)[:4]+ '%',
                        "ANXIETY: "+ str(sentiment['ANXIETY']*100)[:4]+ '%',
                        "SURPRISED: "+ str(sentiment['SURPRISED']*100)[:4]+ '%',
                    ]


            for i, label in enumerate (labels):
                label_position = (0, 25 + i*25) 
                # label_position = ( rect[0] + int((rect[1]/2)), i*12 +  rect[2] + 25 )
                cv2.putText(img, label, label_position , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
            #cv2.putText(img, 'text', org,            font,            fontScale, color, thickness, cv2.LINE_AA)

        path_out= 'output/test.jpg'
        cv2.imwrite(path_out, img)
        print(path_out)

    def face_detector(self, img):
        print("face_detector...")

        t1= datetime.datetime.now()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)

        if faces is ():
            faces = self.face_classifier.detectMultiScale(gray, 1.1, 4)

        if faces is ():
            print("faces not found")
            return ([], None, img )


        Faces=[]
        for i, rect in enumerate(faces):
            Face={}
            x,y,w,h= rect
            Face['bbox']=  { 'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h) }   


            #Face['bb']= bb
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]

            small= img[y:y+h, x:x+w]
            small = cv2.resize(small, (200, 200), interpolation = cv2.INTER_AREA)

            # winname= "small"
            #cv2.imshow(winname, small)

            try:
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation = cv2.INTER_AREA)
                result_emotion= self.emotional(roi_gray)
                Face['sentiment']= result_emotion

            except:
                return (x,w,y,h), np.zeros((48,48), np.uint8), img

            Faces.append(Face)
        #label= self.emotional(roi_gray)

        t2= datetime.datetime.now()
        t21 = str( round((t2 - t1).total_seconds(), 2) ) + 's' 
        print(t21)

        return Faces, img, t21

    def pipeline(self, mat, show=False):
        print("pipeline...")

        Faces, img, t21= self.face_detector(mat)
        if not Faces: return [], None

        print(t21, Faces)

        if show:
            self.visualization(Faces, img)

        return Faces[0]
        
if __name__=="__main__":
    filename= "input/anxiety/3.jpg"
    mat= cv2.imread(filename)
    print(mat[0])
    print(type(mat))

    hf= HandleFrame()
    hf.pipeline(mat, show=True)

    print("done")