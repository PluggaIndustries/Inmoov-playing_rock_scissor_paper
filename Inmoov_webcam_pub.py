#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def publish_message():
  pub = rospy.Publisher('/video_frames', Image, queue_size=10) 
  rospy.init_node('Inmoov_webcam_pub', anonymous=True)
  rate = rospy.Rate(10) # 10hz rate con cui invia i frame
  cap = cv2.VideoCapture(0)
  # Converte tra ROS Image e OpenCV 
  br = CvBridge() 
  while not rospy.is_shutdown():
      ret, frame = cap.read()
      if ret == True: 
        pub.publish(br.cv2_to_imgmsg(frame))
      rate.sleep()

if __name__ == '__main__':
  try:
    publish_message()
  except rospy.ROSInterruptException:
    pass
