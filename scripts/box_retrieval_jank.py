#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32, Int32
from ar_track_alvar_msgs.msg import AlvarMarkers
from actionlib_msgs.msg import GoalStatusArray
from time import sleep

#flag used to ensure home goal is only sent once
status_goal = 10
counterFlag = False
collectionFlag = True
flag = True
counter = 0
Q = [0,0,0,0]
boxInfo = [5,5,5,5]

def counterback(data):
	"""
	Sets counterFlag to True when 1 box has been detected

    Input
    :param data: message on box_counter 
 
    Output
    :return: returns nothing
	"""
	
	if (data.data>=1):
		global counterFlag
		counterFlag = True

def callback(data):
	"""
    Callback function to check and parse the aruco markers' pose with respect to the camera
 
    Input
    :param data: data of the message received on a topic that is of hierarchial structure
 
    Output
    :return: 
    """

	if(data.markers[0].id!=''):
		global boxInfo
		boxInfo[0] = data.markers[0].id
		boxInfo[1] = data.markers[0].pose.pose.position.x
		boxInfo[2] = data.markers[0].pose.pose.position.y
		boxInfo[3] = data.markers[0].pose.pose.position.z
		global Q
		Q[0] = data.markers[0].pose.pose.orientation.x
		Q[1] = data.markers[0].pose.pose.orientation.y
		Q[2] = data.markers[0].pose.pose.orientation.z
		Q[3] = data.markers[0].pose.pose.orientation.w

def status_callback(data):
	if (data!=None):
		global status_goal
		status_goal = data.status_list[len(data.status_list)-1].status

def return_home():
	"""
    Function to create ROS node that retrieves a package and then sends the robot to start pose.
	This happens when a package is detected

    Output
    :return: returns nothing
    """
    # Initialize ros node
	rospy.init_node('box_retrieval', anonymous=True)
    
	# Create a subscriber to box_counter, ar_pose_marker and move_base/status topics
	rospy.Subscriber('box_counter', Int32, counterback)
	rospy.Subscriber('ar_pose_marker', AlvarMarkers, callback)
	rospy.Subscriber('move_base/status', GoalStatusArray, status_callback)
    
	# Initialize ROS publisher to servo_angle and move_base_simple/goal topics
	pubServo = rospy.Publisher('servo_angle', Float32, queue_size=20)
	pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=20)
    
	# Set node publish rate
	rate = rospy.Rate(20)
    
	# Loop to keep the nodes going
	while not rospy.is_shutdown():
		global flag, counterFlag, counter, collectionFlag

		# Check if box has been detected and needs to be retrieved
		if (counterFlag==True and collectionFlag==True and flag==True):
			# Publish box pose as goal
			goal = PoseStamped()
			goal.header.stamp=rospy.get_rostime()
			goal.header.frame_id='map'
			goal.pose.position.x=boxInfo[1]
			goal.pose.position.y=boxInfo[2]
			goal.pose.orientation.w=1.0
			rospy.loginfo(goal)
			pub.publish(goal)
			
			# Counter to publish goal 20 times to ensure it overrides the path planning algorithm
			counter+=1
			if(counter>=20):
				flag = False
		# If at box pose, lift package retrieval system
		if (status_goal==3 and collectionFlag==True and flag==False):
			collectionFlag  = False
			flag = True
			pubServo.publish(-0.2)
			counter = 0
		
		# Check if box has been retrieved
		if (counterFlag==True and collectionFlag==False and flag==True):
			# If so, go to start pose with package
			goal = PoseStamped()
			goal.header.stamp=rospy.get_rostime()
			goal.header.frame_id='map'
			goal.pose.position.x=0
			goal.pose.position.y=0
			goal.pose.position.z=0
			goal.pose.orientation.w=1.0
			rospy.loginfo(goal)
			pub.publish(goal)
			
			# Counter to publish goal 20 times to ensure it overrides the path planning algorithm
			counter+=1
			if(counter>=20):
				flag = False
		# If at start pose, lower package retrieval system
		if (status_goal==3 and collectionFlag==False and flag==False):
			pubServo.publish(0.2)
				
		rate.sleep()

if __name__ == '__main__':
    try:
        return_home()
    except rospy.ROSInterruptException:
        pass
