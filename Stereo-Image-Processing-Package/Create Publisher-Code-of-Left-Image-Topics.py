#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import sys

from cv_bridge import CvBridge
from sensor_msgs.msg import Image, CameraInfo

bridge = CvBridge()

leftCamInfo = CameraInfo()

leftCamInfo.D = [0.1569170822003126, -0.22889902463879086, 0.007650152321982646, 0.0048957099451039324, 0.0]
leftCamInfo.K = [336.5758268477813, 0.0, 247.44670033531492, 0.0, 331.3262582465451, 262.0510590778803, 0.0, 0.0, 1.0]
leftCamInfo.R = [0.9987845570311966, -0.013670814378410176, -0.04735522642990731, 0.01394021992417426, 0.9998884456533916,
0.0053634426733278435, 0.04727662111934815, -0.006017065985633907, 0.998863712431512]
leftCamInfo.P = [372.1279396837233, 0.0, 276.3964099884033, 0.0, 0.0, 372.1279396837233, 262.72875595092773, 0.0, 0.0, 0.0, 1.0, 0.0]
leftCamInfo.distortion_model = "plumb_bob"
leftCamInfo.width = 300
leftCamInfo.height = 300
leftCamInfo.binning_x = 0
leftCamInfo.binning_y =0

sensor_id=0,
sensor_mode=3,
capture_width=1280,
capture_height=720,
display_width=1280,
display_height=720,
framerate=30,
flip_method=0,

gst_pipeline = (
    "nvarguscamerasrc sensor-id=1 sensor-mode=0 ! "
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
  rospy.init_node("left")
  rospy.loginfo("left node started")

if __name__ == "__main__":
  try:
    start_node()
    pub = rospy.Publisher("stereo/left/image_raw", Image, queue_size=1)
    pubInfo = rospy.Publisher("stereo/left/camera_info", CameraInfo, queue_size=1)
    while not rospy.is_shutdown():
      ret, frame = cam.read()
      resized = frame[:, 100:700]
      resized = cv2.resize(resized, (300, 300))
      #cv2.imshow("frame", frame)
      imgMsg = bridge.cv2_to_imgmsg(resized, "bgr8")
      pubInfo.publish(leftCamInfo)
      pub.publish(imgMsg)
      #cv2.waitKey(1)
      rospy.Rate(65)
  except rospy.ROSInterruptException:
      pass
