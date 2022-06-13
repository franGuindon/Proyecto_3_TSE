import cv2
import numpy as np

from tflite_runtime.interpreter import Interpreter

MODEL_FILE = "detect.tflite"

print("Creating interpreter")
INTERPRETER = Interpreter(model_path=MODEL_FILE)
print("Allocating tensors")
INTERPRETER.allocate_tensors()

print("Getting input and output details")
INPUT_DETAILS = INTERPRETER.get_input_details()[0]
BOXES_DETAILS = INTERPRETER.get_output_details()[0]
SCORES_DETAILS = INTERPRETER.get_output_details()[2]

HEIGHT = INPUT_DETAILS['shape'][1]
WIDTH = INPUT_DETAILS['shape'][2]

FLOATING_MODEL = (INPUT_DETAILS['dtype'] == np.float32)

print("Setting up video capture")
CAMERA = cv2.VideoCapture(0)
print("Setting up video format to MJPG")
CAMERA.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
CAM_HEIGHT = CAMERA.get(cv2.CAP_PROP_FRAME_HEIGHT)
CAM_WIDTH = CAMERA.get(cv2.CAP_PROP_FRAME_WIDTH)

def setup(args):
    global ARGS
    ARGS = args
    # CAMERA.set(cv2.CAP_PROP_FRAME_WIDTH, ARGS.width)
    # CAMERA.set(cv2.CAP_PROP_FRAME_HEIGHT, ARGS.height)

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
    dist3 = np.linalg.norm(color - np.array([208, 207, 212]))
    dists = list(enumerate((dist0, dist1, dist2, dist3)))
    dists.sort(key=lambda element: element[1])
    obj_class, _ = dists[0]
    if obj_class == 3: obj_class = 2
    return obj_class

def show_avg_color_box(frame, top_left, bot_right, avg_color):
    cv2.rectangle(frame, top_left, bot_right, avg_color, cv2.FILLED)
    cv2.imshow('Debug window', frame)

def show_class_and_score(frame, top_left, bot_right, obj_class, score):
    cv2.rectangle(frame, top_left, bot_right, (10, 255, 0), 2)
    label = f"Class: {obj_class}, Score: {score*100:.0f}"
    cv2.putText(frame, label, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow('Debug window', frame)

def show_class(frame, obj_class):
    label = f"Class: {obj_class}"
    cv2.putText(frame, label, (int(CAM_HEIGHT*0.5),int(CAM_WIDTH*0.5)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow('Debug window', frame)

def grab_fame():
    ret = True
    while ret:
        ret, frame = CAMERA.read()
        cv2.imshow("", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cv2.destroyAllWindows()
    CAMERA.release()

def try_classify_object():
    grabbed, frame = CAMERA.read()
    if not grabbed: return False, None
    """
    boxes, scores = get_boxes_and_scores(frame)
    (ymin, xmin, ymax, xmax), score = get_main_dims_and_score(boxes, scores)
    if not (ymin or xmin or ymax or xmax): return False, None
    """
    print("cropping img")
    ymin, ymax, xmin, xmax = int((0.5 - 0.1)*CAM_HEIGHT), int((0.5 + 0.1)*CAM_HEIGHT), int((0.5 - 0.1)*CAM_WIDTH), int((0.5 + 0.1)*CAM_WIDTH)
    frame_cropped = frame[ymin:ymax, xmin:xmax]
    avg_color = np.average(frame_cropped, axis=(0,1))
    obj_class = get_obj_class(avg_color)
    
    if ARGS.debug:
        #show_avg_color_box(frame, (xmin, ymin), (xmax, ymax), avg_color)
        #show_class_and_score(frame, (xmin, ymin), (xmax, ymax), obj_class, score)
        show_class(frame, obj_class)
        cv2.imshow("", frame)
        if cv2.waitKey(1) == ord('q'): return False, "break"
    return True, obj_class

def classify_object(attempts):
    array = []
    while len(array) < attempts:
        grabbed, obj_class = try_classify_object()
        if grabbed: array.append(obj_class)
    obj_class = np.average(array)
    return int(round(obj_class, 0))

def continuosly_classify_object():
    while True:
        grabbed, obj_class = try_classify_object()
        print(obj_class)
        if obj_class == "break": break

def cleanup():
    cv2.destroyAllWindows()
    CAMERA.release()

if __name__ == "__main__":
    from arg_parser import parse_args
    args = parse_args()
    setup(args)
    continuosly_classify_object()
    cleanup()
