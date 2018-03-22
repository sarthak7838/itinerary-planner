#from keras.models import model_from_json
from keras.layers import Activation, Convolution2D, Dropout, Conv2D,Dense
from keras.layers import AveragePooling2D, BatchNormalization
from keras.layers import GlobalAveragePooling2D
from keras.models import Sequential
from keras.layers import Flatten
from keras.models import Model
from keras.layers import Input
from keras.layers import MaxPooling2D
from keras.layers import SeparableConv2D
from keras import layers
from keras.regularizers import l2
import h5py
from keras.optimizers import Adam,SGD

from keras.optimizers import SGD
import numpy as np
from time import sleep
import cv2
from scipy.ndimage import zoom

stop=0
problike=0
probdislike=0
count=0
w, h = 7, 5;
matrix = [[[0,0,0] for x in range(w)] for y in range(h)]

def change_active(a,b):
    global probdislike,problike,count,matrix
    matrix[a][b][0]=matrix[a][b][0]+problike
    matrix[a][b][1]=matrix[a][b][1]+probdislike
    matrix[a][b][2]=matrix[a][b][2]+count
    problike=0
    probdislike=0
    count=0
def clean():
    global probdislike,problike,count,matrix
    w, h = 7, 5;
    matrix = [[[0,0,0] for x in range(w)] for y in range(h)]

def finaldata():
    global matrix
    toreturn={}
    for i in range(0,5):
        for j in range(0,7):
            if matrix[i][j][2]!=0:
                toreturn[i,j]=matrix[i][j][0]/matrix[i][j][2]
            else:
                toreturn[i,j]=0
    return toreturn

def stop_thread():
    global stop
    stop=1
def start_thread():
    global stop
    stop=0

def extract_face_features(gray, detected_face, offset_coefficients):
        (x, y, w, h) = detected_face
        #print x , y, w ,h
        horizontal_offset = np.int(np.floor(offset_coefficients[0] * w))
        vertical_offset = np.int(np.floor(offset_coefficients[1] * h))


        extracted_face = gray[y+vertical_offset:y+h,
                          x+horizontal_offset:x-horizontal_offset+w]
        #print extracted_face.shape
        new_extracted_face = zoom(extracted_face, (48. / extracted_face.shape[0],
                                               48. / extracted_face.shape[1]))
        new_extracted_face = new_extracted_face.astype(np.float32)
        new_extracted_face /= float(new_extracted_face.max())
        return new_extracted_face

def detect_face(frame):
        cascPath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=6,
                minSize=(48, 48),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
        return gray, detected_faces


def func():
    """
Best performing model till now. Added layers to the webcamemocognizer one.
"""
    global probdislike,problike,count,stop

    model = Sequential()
    model.add(Convolution2D(32, (3, 3), padding='valid', input_shape=(48,48,1)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(64,(3,3),padding='valid',activation='relu'))
    #model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(128,(3,3),padding='valid'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(256,(3,3),padding='valid'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(128,kernel_initializer="lecun_uniform"))
    #model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dense(2))
    model.add(Activation('softmax'))


    #model = model_from_json(open('./models/Face_model_architecture.json').read())
    #model.load_weights('_model_weights.h5')
    model.load_weights('deep_model_weights_binary_best.h5py')
    #optimizer =Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0)
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

    model.compile(loss='binary_crossentropy', optimizer=sgd)

    cascPath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    video_capture = cv2.VideoCapture(0)


    while True:
        # Capture frame-by-frame
        #    sleep(0.8)
        ret, frame = video_capture.read()

        # detect faces
        gray, detected_faces = detect_face(frame)

        face_index = 0

        # predict output
        for face in detected_faces:
            (x, y, w, h) = face
            if w > 100:
                # draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # extract features
                extracted_face = extract_face_features(gray, face, (0.075, 0.05)) #(0.075, 0.05)

                # predict smile
                prediction_result = model.predict_classes(extracted_face.reshape(1,48,48,1))
                pn=model.predict(extracted_face.reshape(1,48,48,1))
                # draw extracted face in the top right corner
                frame[face_index * 48: (face_index + 1) * 48, -49:-1, :] = cv2.cvtColor(extracted_face * 255, cv2.COLOR_GRAY2RGB)

                # annotate main image with a label
                if prediction_result == 1:
                    cv2.putText(frame, "like!!",(x,y), cv2.FONT_ITALIC, 2, 155, 10)
                    #print("Like")
                    problike=problike+pn[0][1]
                    probdislike=probdislike+pn[0][0]
                    count=count+1
                elif prediction_result == 0:
                    cv2.putText(frame, "dislike",(x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, 155, 10)
                    #print("DisLike")
                    problike=problike+pn[0][1]
                    probdislike=probdislike+pn[0][0]
                    count=count+1

                # increment counter
                face_index += 1


        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if stop==1:
            video_capture.release()
            while True:
                if stop==0:
                    video_capture=cv2.VideoCapture(0)
                    break


        # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
