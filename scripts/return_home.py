#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from actionlib_msgs.msg import GoalID

#flag used to ensure home goal is only sent once
flag = False

def callback(data):

	"""
	Sets flag to True when navigation is terminated

    Input
    :param data: message on move_base/cancel 
 
    Output
    :return: returns nothing
    """

	if (data.id==''):
		global flag
		flag = True	

# Function to send the robot the origin as a goal when exploration is complete
def return_home():
    # Initialize ros subscriber to move_base/cancel
	rospy.init_node('return_home', anonymous=True)
    
	# Create a subscriber to move_base/cancel topic
	rospy.Subscriber('move_base/cancel', GoalID, callback)
    
	# Initialize ROS publisher to move_base_simple/goal
	pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=100)
    
	rate = rospy.Rate(20)
    
	# Loop to keep the nodes going
	while not rospy.is_shutdown():

		global flag
	# Check is mapping is complete (flag)
		if (flag==True):
		# If mapping is complete, let user know and then return to home
			print("EXPLORATION STOPPED")
			goal = PoseStamped()
			goal.header.stamp=rospy.get_rostime()
			goal.header.frame_id='map'
			goal.pose.position.x=0
			goal.pose.position.y=0
			goal.pose.position.z=0
			goal.pose.orientation.w=1.0
			rospy.loginfo(goal)
			pub.publish(goal)
			
			global flag
			flag = False   	
		rate.sleep()

if __name__ == '__main__':
    try:
        return_home()
    except rospy.ROSInterruptException:
        pass
