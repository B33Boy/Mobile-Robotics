#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from actionlib_msgs.msg import GoalID
from sensor_msgs.msg import LaserScan # LaserScan type message is defined in sensor_msgs
from geometry_msgs.msg import Twist #
from std_msgs.msg import Int32

#flag used to ensure home goal is only sent once
flag = False
move = Twist() # Creates a Twist message type object
box_counter=0

#ros return_home subscriber callback function
#Checks if data has been published to move_base/cancel topic and changes flag
def callback_returnHome(data):
        if (data.id==''):
		global flag
		flag = True

def callback_roomba(msg):
	global move
	thr1 = 0.4 # Laser scan range threshold
	thr2 = 0.4
	if msg.ranges[0]>thr1 and msg.ranges[15]>thr2 and msg.ranges[345]>thr2: # Checks if there are obstacles in front and
                                                                         # 15 degrees left and right (Try changing the
									 # the angle values as well as the thresholds)
		move.linear.x = 0.15 # go forward (linear velocity)
		move.angular.z = 0.0 # do not rotate (angular velocity)
	else:
		move.linear.x = 0.0 # stop
		move.angular.z = 0.5 # rotate counter-clockwise
		if msg.ranges[0]>thr1 and msg.ranges[15]>thr2 and msg.ranges[345]>thr2:
			move.linear.x = 0.15
			move.angular.z = 0.0

def callback_counter(data_1):
	global box_counter
	box_counter = data_1.data

#function to send the robot the origin as a goal when exploration is complete
def return_home():
    #initialize ros subscriber to move_base/cancel
	rospy.init_node('search_and_return_home', anonymous=True)
	rospy.Subscriber('move_base/cancel', GoalID, callback_returnHome)
	#initialize ros publisher to move_base_simple/goal
	pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=100)
	pub_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)  # Publisher object which will publish "Twist" type messages
	sub = rospy.Subscriber("/scan", LaserScan, callback_roomba)  # Subscriber object which will listen "LaserScan" type messages
	sub_counter = rospy.Subscriber("/box_counter", Int32, callback_counter)

	rate = rospy.Rate(0.1)
    #loop to keep the nodes going
	while not rospy.is_shutdown():
    #check is mapping is complete (flag)
		global flag, move, box_counter
		if (flag==True and box_counter<2):
			pub_vel.publish(move) # publish the move object
		if (flag==True and box_counter>1):
			print("SEARCH COMPLETE")
			goal = PoseStamped()
			goal.header.stamp=rospy.get_rostime()
			goal.header.frame_id='map'
			goal.pose.position.x=0
			goal.pose.position.y=0
			goal.pose.position.z=0
			goal.pose.orientation.w=1.0
			rospy.loginfo(goal)
			pub.publish(goal)
			flag = False   	
	rate.sleep()

if __name__ == '__main__':
    try:
        return_home()
    except rospy.ROSInterruptException:
        pass
