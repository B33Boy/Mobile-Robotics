#!/usr/bin/python
import rospy
from gpiozero import Servo
from time import sleep
from std_msgs.msg import Float32

# Initialize servo to gpio 24
servo = Servo(24)
# Servo angle is set between -1 and 1 (0 - 180)
angle = 0.2 #108 degrees

def angleCallback(data):
    """
    Callback function save the servo angle sent on servo_angle topic
 
    Input
    :param data: data of the message received on the servo_angle topic (Float32)
 
    Output
    :return: 
    """
    global angle
    # Round the value to 1 decimal place
    angle = round(data.data, 1)

def SetAngle():
    """
    Function to set/maintain the desired servo angle
 
    Input
    :none: Uses global variable angle
 
    Output
    :return: 
    """
    global angle
    servo.value = angle

if __name__ == '__main__':
    try:
        # Initialize ROS node
        rospy.init_node('servo_control', anonymous=True)
        # Setup subscriber to servo_angle topic
        rospy.Subscriber('servo_angle', Float32, angleCallback)
        # Set node rate
        rate = rospy.Rate(20)

        while not rospy.is_shutdown():
            # Set/maintain angle each loop
            SetAngle()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass