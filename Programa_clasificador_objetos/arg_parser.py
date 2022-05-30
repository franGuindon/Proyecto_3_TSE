import argparse

import numpy as np

def add_general_arguments(parser):
    parser.add_argument(
        "-d", "--debug",
        help="Display debug info.",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--dir_pal",
        help="Dirección paleta",
        default=1
    )

def add_classifier_arguments(parser):
    parser.add_argument(
        "-t", "--threshold",
        help="Minimum confidence threshold for object detection.",
        default=0.5
    )
    parser.add_argument(
        "-r", "--resolution",
        help="Desired webcam resolution in WxH."
            "Webcam paired with non-supported resolutions may cause errors.",
        default="1280x720"
    )
    parser.add_argument(
        "-0", "--color0",
        help="Color for class 0 in 'R,G,B' format.",
        default="255,0,0"
    )
    parser.add_argument(
        "-1", "--color1",
        help="Color for class 1 in 'R,G,B' format.",
        default="0,255,0"
    )
    parser.add_argument(
        "-2", "--color2",
        help="Color for class 2 in 'R,G,B' format.",
        default="0,0,255"
    )

def parse_general_arguments(args):
    args.dir_pal = int(args.dir_pal)

def parse_classifier_arguments(args):
    args.threshold = float(args.threshold)

    width_str, height_str = args.resolution.split("x")
    args.width, args.height = int(width_str), int(height_str)

    r0_str, g0_str, b0_str = args.color0.split(",")
    args.color0 = np.array((int(b0_str), int(g0_str), int(r0_str)))

    r1_str, g1_str, b1_str = args.color1.split(",")
    args.color1 = np.array((int(b1_str), int(g1_str), int(r1_str)))

    r2_str, g2_str, b2_str = args.color2.split(",")
    args.color2 = np.array((int(b2_str), int(g2_str), int(r2_str)))

def parse_args():
    parser = argparse.ArgumentParser()
    add_general_arguments(parser)
    #add_classifier_arguments(parser)
    args = parser.parse_args()
    parse_general_arguments(args)
    #parse_classifier_arguments(args)
    return args
