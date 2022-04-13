#!/usr/bin/python
import rospy
from gpiozero import Servo
from time import sleep
from std_msgs.msg import Float32

servo = Servo(24)
angle = 1

def angleCallback(data):
    global angle
    angle = round(data.data, 1)

def SetAngle():
    global angle
    servo.value = angle

if __name__ == '__main__':
    try:
        rospy.init_node('servo_control', anonymous=True)
        rospy.Subscriber('servo_angle', Float32, angleCallback)
        rate = rospy.Rate(20)
        while not rospy.is_shutdown():
            SetAngle()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass