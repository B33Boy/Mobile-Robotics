#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Int32
from ar_track_alvar_msgs.msg import AlvarMarker
from visualization_msgs.msg import Marker
from multiprocessing import Process, Pipe
import thread, time

#flag used to ensure home goal is only sent once
packageOneFlag = False
packageTwoFlag = False
boxReference = {'ids': 0,1,2,3, 'width': 10,5,10,5, 'height': 5,5,5,5, 'depth': 5,10,5,10}

#ros return_home subscriber callback function
#Checks if data has been published to move_base/cancel topic and changes flag
def callback(data):
        if (data.id!=''):
		boxInfo[0] = data.id
		boxInfo[1] = data.pose.position.x
		boxInfo[2] = data.pose.position.y
		boxInfo[3] = data.pose.position.z
		boxInfo[4] = data.pose.orientation.x
		boxInfo[4] = data.pose.orientation.y
		boxInfo[4] = data.pose.orientation.z
		boxInfo[4] = data.pose.orientation.w
		global flag
		flag = True	

#function to send the robot the origin as a goal when exploration is complete
def box_locator():
    #initialize ros subscriber to move_base/cancel
    rospy.init_node('box_locator', anonymous=True)
    rospy.Subscriber('ar_pose_marker', AlvarMarker, callback)
    #initialize ros publisher to move_base_simple/goal
    pub = rospy.Publisher('visualization_marker', Marker, queue_size=100)
    rate = rospy.Rate(20)
    #loop to keep the nodes going
    while not rospy.is_shutdown():
    #check is mapping is complete (flag)
	if (boxInfo[0]==0 or boxInfo[0]==1)
		if (packageOneFlag==False)
			global packageOneFlag
			packageOneFlag = True
			newMarker = marker
			marker.header.stamp=rospy.get_rostime()
			marker.header.frame_id='map'
			
			
	if (boxInfo[0]==2 or boxInfo[0]==3)
		if (packageTwoFlag==False)
			global packageOneFlag
			packageTwoFlag = True
	rate.sleep()


if __name__ == '__main__':
    try:
        box_locator()
    except rospy.ROSInterruptException:
        pass
