#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import String, Int32
from ar_track_alvar_msgs.msg import AlvarMarkers
from visualization_msgs.msg import Marker
from multiprocessing import Process, Pipe
import thread, time

#flag used to ensure home goal is only sent once
packageOneFlag = False
packageTwoFlag = False
Q = [0,0,0,0]
boxInfo = [5,5,5,5]
#boxReference = {'ids': 0,1,2,3, 'width': 10,5,10,5, 'height': 5,5,5,5, 'depth': 5,10,5,10}

#ros return_home subscriber callback function
#Checks if data has been published to move_base/cancel topic and changes flag

def callback(data):
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

#function to send the robot the origin as a goal when exploration is complete
def box_locator():
    #initialize ros subscriber to move_base/cancel
	rospy.init_node('box_locator', anonymous=True)
	rospy.Subscriber('ar_pose_marker', AlvarMarkers, callback)
    #initialize ros publisher to move_base_simple/goal
	pub1 = rospy.Publisher('visualization_marker_1', Marker, queue_size=100)
	pub2 = rospy.Publisher('visualization_marker_2', Marker, queue_size=100)
	pub_counter = rospy.Publisher('box_counter', Int32, queue_size=10)
	rate = rospy.Rate(30)
    #loop to keep the nodes going
	while not rospy.is_shutdown():
    #check is mapping is complete (flag)
		global boxInfo
		if (boxInfo[0]==0 or boxInfo[0]==1):
			global packageOneFlag
			if (packageOneFlag==False):
				packageOneFlag = True
				marker1=Marker()
				marker1.header.stamp=rospy.get_rostime()
				marker1.header.frame_id='map'
				marker1.type=1
				marker1.action=0
				marker1.pose.position.x = boxInfo[1]
				marker1.pose.position.y = boxInfo[2]
				marker1.pose.position.z = boxInfo[3]
				if (boxInfo[0]==0):
					marker1.scale.x=0.10
					marker1.scale.y=0.05
					marker1.scale.z=0.05
				if (boxInfo[0]==1):
					marker1.scale.x=0.05
					marker1.scale.y=0.05
					marker1.scale.z=0.10
				marker1.pose.orientation.x=Q[0]
				marker1.pose.orientation.y=Q[1]
				marker1.pose.orientation.z=Q[2]
				marker1.pose.orientation.w=Q[3]
				marker1.color.g=0
				marker1.color.r=0
				marker1.color.b=1
				marker1.color.a=1
				pub1.publish(marker1)
			
			
		elif (boxInfo[0]==2 or boxInfo[0]==3):
			global packageTwoFlag
			if (packageTwoFlag==False):
				packageTwoFlag = True
				marker2=Marker()
				marker2.header.stamp=rospy.get_rostime()
				marker2.header.frame_id='map'
				marker2.type=1
				marker2.action=0
				marker2.pose.position.x = boxInfo[1]
				marker2.pose.position.y = boxInfo[2]
				marker2.pose.position.z = boxInfo[3]
				if (boxInfo[0]==2):
					marker2.scale.x=0.10
					marker2.scale.y=0.05
					marker2.scale.z=0.05
				if (boxInfo[0]==3):
					marker2.scale.x=0.05
					marker2.scale.y=0.05
					marker2.scale.z=0.10
				marker2.pose.orientation.x=Q[0]
				marker2.pose.orientation.y=Q[1]
				marker2.pose.orientation.z=Q[2]
				marker2.pose.orientation.w=Q[3]
				marker2.color.g=0
				marker2.color.r=1
				marker2.color.b=0
				marker2.color.a=1
				pub2.publish(marker2)

		counter=0
		if (packageOneFlag==False and packageTwoFlag==False):
			counter = 0	
		if (packageOneFlag==True or packageTwoFlag==True):
			counter = 1
		if (packageOneFlag==True and packageTwoFlag==True):
			counter = 2
		pub_counter.publish(counter)

		rate.sleep()


if __name__ == '__main__':
    try:
        box_locator()
    except rospy.ROSInterruptException:
        pass
