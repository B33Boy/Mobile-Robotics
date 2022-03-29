#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from actionlib_msgs.msg import GoalID
from std_msgs.msg import Int32
import actionlib
import actionlib_msgs

#flag used to ensure home goal is only sent once
explorationFlag = False
counterFlag = True
flag = True

def callback(data):

    """
	Sets flag to True when navigation is terminated

    Input
    :param data: message on move_base/cancel 
 
    Output
    :return: returns nothing
    """

    if (data.id==''):
        global explorationFlag
        explorationFlag = True


def counterback(data):
    if (data.data>=2):
        global counterFlag
        counterFlag = True

# Function to send the robot the origin as a goal when exploration is complete
def return_home_third():
    # Initialize ros subscriber to move_base/cancel
    rospy.init_node('return_home', anonymous=True)
    
	# Create a subscriber to move_base/cancel topic
    rospy.Subscriber('move_base/cancel', GoalID, callback)
    rospy.Subscriber('box_counter', Int32, counterback)
    
	# Initialize ROS publisher to move_base_simple/goal
    pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=20)
    #pubCancel = rospy.Publisher('move_base/cancel', GoalID, queue_size = 20)
    
    rate = rospy.Rate(20)
    
	# Loop to keep the nodes going
    while not rospy.is_shutdown():
    
	# Check is mapping is complete (flag)
        global explorationFlag, counterFlag, flag

        if (explorationFlag==True and flag==True):# and counterFlag==True):
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
        return_home_third()
    except rospy.ROSInterruptException:
        pass
