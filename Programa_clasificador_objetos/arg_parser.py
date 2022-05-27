import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--threshold',
        help='Minimum confidence threshold for displaying detected objects',
        default=0.5
    )
    parser.add_argument(
        '--resolution',
        help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
        default='1280x720'
    )
                   
    args = parser.parse_args()

    return args