import rospy
import RPi.GPIO as GPIO
from time import sleep
from std_msgs.msg import Int32

angle = 180

def angleCallback(data):
    global angle
    angle = data

def SetAngle():
    global angle
    duty = angle/18+2
    GPIO.output(24, True)
    p.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(24, False)
    p.ChangeDutyCycle(0)

if __name__ == '__main__':
    try:
        rospy.init_node('servo_control', anonymous=True)
        rospy.Subscriber('servo_angle', Int32, angleCallback)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(24, GPIO.OUT)
        p = GPIO.PWM(24, 50)
        #p.start(0)
        SetAngle()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass