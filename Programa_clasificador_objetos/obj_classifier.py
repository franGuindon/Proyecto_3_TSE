import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter

from arg_parser import parse_args

ARGS = parse_args()

MODEL_FILE = "detect.tflite"

INTERPRETER = Interpreter(model_path=MODEL_FILE)

INTERPRETER.allocate_tensors()

INPUT_DETAILS = INTERPRETER.get_input_details()[0]
BOXES_DETAILS = INTERPRETER.get_output_details()[0]
SCORES_DETAILS = INTERPRETER.get_output_details()[2]

HEIGHT = INPUT_DETAILS['shape'][1]
WIDTH = INPUT_DETAILS['shape'][2]

FLOATING_MODEL = (INPUT_DETAILS['dtype'] == np.float32)

CAMERA = cv2.VideoCapture(0)
CAMERA.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
CAMERA.set(cv2.CAP_PROP_FRAME_WIDTH, ARGS.width)
CAMERA.set(cv2.CAP_PROP_FRAME_HEIGHT, ARGS.height)

def get_boxes_and_scores(frame):
    frame_copy = frame.copy()
    frame_rgb = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (WIDTH, HEIGHT))
    input_data = np.expand_dims(frame_resized, axis=0)

    INTERPRETER.set_tensor(INPUT_DETAILS['index'], input_data)
    INTERPRETER.invoke()

    boxes = INTERPRETER.get_tensor(BOXES_DETAILS['index'])[0]
    scores = INTERPRETER.get_tensor(SCORES_DETAILS['index'])[0]
    
    return boxes, scores

def parse_box(box):
    ymin, xmin, ymax, xmax = box

    ymin, ymax = ymin*ARGS.height, ymax*ARGS.height
    ymin, ymax = int(max(1, ymin)), int(min(ARGS.height, ymax))

    xmin, xmax = xmin*ARGS.width, xmax*ARGS.width
    xmin, xmax = int(max(1, xmin)), int(min(ARGS.width, xmax))

    return ymin, xmin, ymax, xmax

def get_main_dims_and_score(boxes, scores):
    m_area, m_dims, m_score = 0, (0, 0, 0, 0), 0
    for box, score in zip(boxes, scores):
        if (score <= ARGS.threshold) or (score > 1.0): continue
        dims = ymin, xmin, ymax, xmax = parse_box(box)
        area = (xmax-xmin)*(ymax-ymin)
        if area > m_area: m_area, m_dims, m_score = area, dims, score
    return m_dims, m_score

def get_obj_class(color):
    dist0 = np.linalg.norm(color - ARGS.color0)
    dist1 = np.linalg.norm(color - ARGS.color1)
    dist2 = np.linalg.norm(color - ARGS.color2)
    dists = list(enumerate((dist0, dist1, dist2)))
    dists.sort(key=lambda element: element[1])
    obj_class, _ = dists[0]
    return obj_class

def show_avg_color_box(frame, top_left, bot_right, avg_color):
    cv2.rectangle(frame, top_left, bot_right, avg_color, cv2.FILLED)
    cv2.imshow('Debug window', frame)

def show_class_and_score(frame, top_left, bot_right, obj_class, score):
    cv2.rectangle(frame, top_left, bot_right, (10, 255, 0), 2)
    label = f"Class: {obj_class}, Score: {score*100:.0f}"
    cv2.putText(frame, label, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow('Debug window', frame)

def try_classify_object():
    grabbed, frame = CAMERA.read()
    if not grabbed: return False, None

    boxes, scores = get_boxes_and_scores(frame)
    (ymin, xmin, ymax, xmax), score = get_main_dims_and_score(boxes, scores)
    if not (ymin or xmin or ymax or xmax): return False, None

    frame_cropped = frame[ymin:ymax, xmin:xmax]
    avg_color = np.average(frame_cropped, axis=(0,1))
    obj_class = get_obj_class(avg_color)
    if ARGS.debug:
        #show_avg_color_box(frame, (xmin, ymin), (xmax, ymax), avg_color)
        show_class_and_score(frame, (xmin, ymin), (xmax, ymax), obj_class, score)
        if cv2.waitKey(1) == ord('q'): return False, None
    return True, obj_class

def classify_object():
    grabbed = False
    obj_class = None
    while not grabbed: grabbed, obj_class = try_classify_object()
    return obj_class

def continuosly_classify_object():
    grabbed = True
    while grabbed: grabbed, _ = try_classify_object()

def clean_up():
    cv2.destroyAllWindows()
    CAMERA.release()

if __name__ == "__main__":
    continuosly_classify_object()
    clean_up()