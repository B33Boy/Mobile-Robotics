#!/usr/bin/python
import rospy
from gpiozero import Servo
from time import sleep
from std_msgs.msg import Int32

servo = Servo(24)
angle = -0.5

def angleCallback(data):
    global angle
    angle = data

def SetAngle():
    global angle
    servo.value = angle

if __name__ == '__main__':
    try:
        rospy.init_node('servo_control', anonymous=True)
        rospy.Subscriber('servo_angle', Int32, angleCallback)
        #p.start(0)
        SetAngle()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass