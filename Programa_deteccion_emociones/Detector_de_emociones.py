## Código reacondiciando por: Mac Alfred Pinnock Chacón
## Instituto Tecnológico de Costa Rica
## Taller de sistemas embebidos 
## 2do proyecto

import cv2
import tflite_runtime.interpreter as tf
import numpy as np
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y___%H_%M_%S")+'.txt'
emociones = []
def crop_center(img, x, y, w, h):    
    return img[y:y+h,x:x+w]

def preprocess_img(raw):
    img = cv2.resize(raw,(200,200))/255
    img = np.expand_dims(img,axis=0)
    if(np.max(img)>1):
        img = img/255.0
    return img

def time(emocion, dt_string):
    # dd_mm_YY___h_m_s
    now = datetime.now()
    dt_string_now = now.strftime("%d_%m_%Y___%H_%M_%S")
    array = []
    array = [dt_string_now,emocion]
    with open(dt_string, 'a') as f:
        f.write(' '.join(array))
        f.write('\n')
def contar_emociones(emociones):
    print('Estadisticadas de las emociones detectadas \n')
    print(' | | | | | | | | | | | | | | | | | | | | | | \n')
    print(' v v v v v v v v v v v v v v v v v v v v v v \n')
    directorio = {i:emociones.count(i) for i in emociones}
    suma_emociones = sum(list(directorio.values()))
    for i in list(directorio.keys()):
        print (i, directorio.get(i), 'Porcentaje = ', 100*(directorio.get(i) /suma_emociones))
    print(' ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ ʌ \n')
    print(' | | | | | | | | | | | | | | | | | | | | | | \n')

def brain(raw, x, y, w, h, dt_string):
    emocion = ''
    img = crop_center(raw, x, y , w , h)
    img = preprocess_img(img)
    f.set_tensor(i['index'], img.astype(np.float32))
    f.invoke()
    res = f.get_tensor(o['index'])
    classes = np.argmax(res,axis=1)
    if classes == 0:
        emocion= 'enojo'
    elif classes == 1:
        emocion= 'disgusto'
    elif classes == 2:
        emocion= 'miedo'
    elif classes == 3:
        emocion= "felicidad"
    elif classes == 4:
        emocion= "neutral"
    elif classes == 5:
        emocion= 'tristeza'
    else :
        emocion= 'sorpresa'
    time(emocion, dt_string)
    return emocion
    

print('Cargando ..')

f = tf.Interpreter("model_optimized.tflite")
f.allocate_tensors()
i = f.get_input_details()[0]
o = f.get_output_details()[0]

print('Carga completa')

cascPath = "haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascPath)


cap = cv2.VideoCapture(0)
ai = 'enojado'
img = np.zeros((200, 200, 3))
ct = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    ct+=1
    gray = frame

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(150, 150)
    )
    
    emocion = ''    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, ai, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
        if ct > 3:
            ai = brain(gray, x, y, w, h, dt_string)
            ct = 0
            emociones.append(ai)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
contar_emociones(emociones)
cap.release()
cv2.destroyAllWindows()