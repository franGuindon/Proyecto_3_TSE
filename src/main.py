from unittest import result
from fer import FER
import cv2

def main():
    # detector = FER(mtcnn=True)
    cap = cv2.VideoCapture("/dev/video0")
    if not cap.isOpened(): raise IOError
    #results = []
    for _ in range(100):
        ret, frame = cap.read()
        if ret is False: raise IOError
        #result = detector.detect_emotions(frame)
        #results.append(result)
        cv2.imshow("frame", frame)
        cv2.waitKey(1)
    #print(results)

if __name__ == "__main__": main()