import sys
import cv2
import numpy as np
#pytesseract.pytesseract.tesseract_cmd=r'C:Program FilesTesseract-OCRtesseract.exe'

try:
    gotdata = sys.argv[1]
except IndexError:
    gotdata = 'null'

if (gotdata == 'null'):
    print("ERROR: No a puesto el nombre de la imagen a procesar")
    quit()
else:
    archivo = str(sys.argv[1])


img = cv2.imread(archivo)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_notnoise = cv2.medianBlur(img,5)

kernel = np.ones((5,5),np.uint8)
img_th = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


print('-----------------------------------------')
print('SALIDA OPENCV --> ORIGINAL GRAYSCALE')
print('-----------------------------------------')
cv2.imwrite('text_gray.jpg', img_gray)


print('-----------------------------------------')
print('SALIDA OPENCV --> NOT NOISE')
print('-----------------------------------------')
cv2.imwrite('text_notnoise.jpg', img_notnoise)


print('-----------------------------------------')
print('SALIDA OPENCV --> Thresholding')
print('-----------------------------------------')
cv2.imwrite('text_th.jpg', img_th)
