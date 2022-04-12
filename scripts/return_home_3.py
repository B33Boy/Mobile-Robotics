#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from actionlib_msgs.msg import GoalID
from std_msgs.msg import Int32
import actionlib
import actionlib_msgs

#flag used to ensure home goal is only sent once
explorationFlag = False
counterFlag = False
flag = True
counter = 0

def callback(data):
	"""
	Sets explorationFlag to True when exploration is terminated

    Input
    :param data: message on move_base/cancel 
 
    Output
    :return: returns nothing
    """

	if (data.id==''):
		global explorationFlag
		explorationFlag = True	

def counterback(data):
	"""
	Sets counterFlag to True when 2 boxes have been detected

    Input
    :param data: message on box_counter 
 
    Output
    :return: returns nothing
	"""
	
	if (data.data>=2):
		global counterFlag
		counterFlag = True

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
	rospy.Subscriber('move_base/cancel', GoalID, callback)
	rospy.Subscriber('box_counter', Int32, counterback)
    
	# Initialize ROS publisher to move_base_simple/goal
	pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=20)
    
	# Set node publish rate
	rate = rospy.Rate(20)
    
	# Loop to keep the nodes going
	while not rospy.is_shutdown():

		global flag, explorationFlag,counterFlag, counter
	# Check is mapping and box exploration are complete
		if (flag==True and explorationFlag==True and counterFlag==True):
		# If everything is complete, let user know and then publish home goal
			print("Returning Home")
			goal = PoseStamped()
			goal.header.stamp=rospy.get_rostime()
			goal.header.frame_id='map'
			goal.pose.position.x=0
			goal.pose.position.y=0
			goal.pose.position.z=0
			goal.pose.orientation.w=1.0
			rospy.loginfo(goal)
			pub.publish(goal)
			
			# Counter to publish goal 100 times to ensure it overrides the path planning algorithm
			counter+=1
			if(counter>=100):
				flag = False  	
		rate.sleep()

if __name__ == '__main__':
    try:
        return_home()
    except rospy.ROSInterruptException:
        pass
