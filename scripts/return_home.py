#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Int32
from geometry_msgs.msg import PoseStamped
from actionlib_msgs.msg import GoalID
from move_base_msgs.msg import MoveBaseActionGoal
from multiprocessing import Process, Pipe
import thread, time

flag = False

def callback(data):
        if (data.id==''):
		global flag
		flag = True	

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('move_base/cancel', GoalID, callback)
    pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=100)
    rate = rospy.Rate(20)
    # spin() simply keeps python from exiting until this node is stopped
    while not rospy.is_shutdown():
    # do whatever you want here
	if (flag==True):
		print("EXPLORATION STOPPED")
		goal = PoseStamped()
		goal.header.stamp=rospy.get_rostime()
		goal.header.frame_id='map'
		goal.pose.position.x=0.5
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
        listener()
    except rospy.ROSInterruptException:
        pass
