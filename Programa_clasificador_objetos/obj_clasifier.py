from arg_parser import parse_args

pkg = importlib.util.find_spec('tflite_runtime')
if pkg: from tflite_runtime.interpreter import Interpreter
else: from tensorflow.lite.python.interpreter import Interpreter

args = parse_args()

MODEL_FILE = "detect.tflite"

interpreter = Interpreter(model_path=MODEL_FILE)