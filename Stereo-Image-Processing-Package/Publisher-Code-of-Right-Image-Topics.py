#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import sys

from cv_bridge import CvBridge
from sensor_msgs.msg import Image, CameraInfo

bridge = CvBridge()

rightCamInfo = CameraInfo()

rightCamInfo.D = [0.14848297651863696, -0.23211504638261077, 0.00554448411281769, 0.004904811820679364, 0.0]
rightCamInfo.K = [334.3432506979186, 0.0, 258.96387838003477, 0.0, 329.156146359108, 257.21497195869205, 0.0, 0.0, 1.0]
rightCamInfo.R = [0.999662592692041, 0.01954381929425834, -0.017109643468520532, -0.019640898676970494, 0.9997918363216206, -0.0055244116250247315, 0.016998113759693796, 0.005858596421934612, 0.9998383574241275]
rightCamInfo.P = [372.1279396837233, 0.0, 276.3964099884033, 135.43805496802958, 0.0, 372.1279396837233, 262.72875595092773, 0.0, 0.0, 0.0, 1.0, 0.0]
rightCamInfo.distortion_model = "plumb_bob"
rightCamInfo.width = 300
rightCamInfo.height = 300
rightCamInfo.binning_x = 0
rightCamInfo.binning_y =0

sensor_id=0,
sensor_mode=3,
capture_width=1280,
capture_height=720,
display_width=1280,
display_height=720,
framerate=30,
flip_method=0,

"""3264 x 2464 FR = 21.000000 fps Duration = 47619048 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;"""

gst_pipeline = (
    "nvarguscamerasrc sensor-id=0 sensor-mode=0 ! "
    "video/x-raw(memory:NVMM), "
    "width=(int)3264, height=(int)2464, "
    "format=(string)NV12, framerate=(fraction)21/1 ! "
    "nvvidconv flip-method=0 ! "
    "video/x-raw, width=(int)800, height=(int)600, format=(string)BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=(string)BGR ! appsink"
)

cam = cv2.VideoCapture(
    gst_pipeline, cv2.CAP_GSTREAMER
)

def start_node():
  rospy.init_node("right")
  rospy.loginfo("right node started")
if __name__ == "__main__":
  try:
    start_node()
    pub = rospy.Publisher("stereo/right/image_raw", Image, queue_size=1)
    pubInfo = rospy.Publisher("stereo/right/camera_info", CameraInfo, queue_size=1)
    while not rospy.is_shutdown():
      ret, frame = cam.read()
      resized = frame[:, 100:700]
      resized = cv2.resize(resized, (300, 300))
      imgMsg = bridge.cv2_to_imgmsg(resized, "bgr8")
      pubInfo.publish(rightCamInfo)
      pub.publish(imgMsg)
      rospy.Rate(65)
  except rospy.ROSInterruptException:
      pass
