#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from actionlib_msgs.msg import GoalID
from std_msgs.msg import UInt16, Int32
import actionlib
import actionlib_msgs
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from ar_track_alvar_msgs.msg import AlvarMarkers

#flag used to ensure home goal is only sent once
counterFlag = False
collectionFlag = True
counter = 0
Q = [0,0,0,0]
boxInfo = [5,5,5,5]

def counterback(data):
	"""
	Sets counterFlag to True when 2 boxes have been detected

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

def return_home():
	"""
    Function to create ROS node that sends the robot origin as a goal.
	This happens when mapping and box exploration are complete

    Output
    :return: returns nothing
    """
    # Initialize ros node
	rospy.init_node('return_home', anonymous=True)
    
	# Create a subscriber to move_base/cancel topic and box_counter topic
	rospy.Subscriber('box_counter', Int32, counterback)
	rospy.Subscriber('ar_pose_marker', AlvarMarkers, callback)
    
	# Initialize ROS publisher to move_base_simple/goal
	pubServo = rospy.Publisher('servoPos', UInt16, queue_size=20)
    
	# Set node publish rate
	rate = rospy.Rate(20)
    
	# Loop to keep the nodes going
	while not rospy.is_shutdown():

		global counterFlag, counter, collectionFlag
	# Check is mapping and box exploration are complete
		if (explorationFlag==True and counterFlag==True and collectionFlag==True):
			client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
			client.wait_for_server()
			goal = MoveBaseGoal()
			goal.target_pose.header.frame_id = "map"
			goal.target_pose.header.stamp = rospy.Time.now()
			goal.target_pose.pose.position.x = boxInfo[1]
			goal.target_pose.pose.position.y = boxInfo[2]
			goal.target_pose.pose.orientation.w = 1.0

			client.send_goal(goal)
			wait = client.wait_for_result()
			collectionFlag  = False
			pubServo.publish(5)
			if not wait:
				rospy.logerr("Action server not available!")
				rospy.signal_shutdown("Action server not available!")
			else:
				return client.get_result()
		
		if (explorationFlag==True and counterFlag==True and collectionFlag==False):
			client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
			client.wait_for_server()
			goal = MoveBaseGoal()
			goal.target_pose.header.frame_id = "map"
			goal.target_pose.header.stamp = rospy.Time.now()
			goal.target_pose.pose.position.x = 0.0
			goal.target_pose.pose.position.y = 0.0
			goal.target_pose.pose.orientation.w = 1.0

			client.send_goal(goal)
			wait = client.wait_for_result()
			pubServo.publish(175)
			if not wait:
				rospy.logerr("Action server not available!")
				rospy.signal_shutdown("Action server not available!")
			else:
				return client.get_result()
				
		rate.sleep()

if __name__ == '__main__':
    try:
        return_home()
    except rospy.ROSInterruptException:
        pass
