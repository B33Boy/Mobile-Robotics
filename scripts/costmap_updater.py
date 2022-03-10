#!/usr/bin/env python
import rospy, math
from std_msgs.msg import String, Int32
from visualization_msgs.msg import Marker
from sensor_msgs.msg import LaserScan
import thread, time

#flag used to ensure home goal is only sent once
flag1 = False
flag2 = False
box1=[0,0]
box2=[0,0]
#ros return_home subscriber callback function
#Checks if data has been published to move_base/cancel topic and changes flag
def callback1(data):
	global flag1
	flag1 = True
	global box1
	box1[0]=math.atan(data.pose.position.y/data.pose.position.x)
	box1[1]=math.sqrt(data.pose.position.x*data.pose.position.x+data.pose.position.y*data.pose.position.y)

def callback2(data):
	global flag2
	flag2 = True
	global box2
	box2[0]=math.atan(data.pose.position.y/data.pose.position.x)
	box2[1]=math.sqrt(data.pose.position.x*data.pose.position.x+data.pose.position.y*data.pose.position.y)	

#function to send the robot the origin as a goal when exploration is complete
def costmap_updater():
    #initialize ros subscriber to move_base/cancel
	rospy.init_node('costmap_updater', anonymous=True)
	rospy.Subscriber('visualization_marker_1', Marker, callback1)
	rospy.Subscriber('visualization_marker_2', Marker, callback2)
    #initialize ros publisher to move_base_simple/goal
	pub1 = rospy.Publisher('scan_1', LaserScan, queue_size=100)
	pub2 = rospy.Publisher('scan_2', LaserScan, queue_size=100)
	rate = rospy.Rate(10)
    #loop to keep the nodes going
	while not rospy.is_shutdown():
    #check is mapping is complete (flag)
		global box1, box2, flag1, flag2
		if (flag1==True):
			box1_scan=LaserScan()
			box1_scan.header.stamp=rospy.get_rostime()
			box1_scan.header.frame_id='map'
			box1_scan.angle_min=box1[0]
			box1_scan.angle_max=box1[0]
			box1_scan.range_min=0
			box1_scan.range_max=20
			box1_scan.ranges=[box1[1]]
			pub1.publish(box1_scan)
			print("PUBLISHED")
			
		if (flag2==True):
			box2_scan=LaserScan()
			box2_scan.header.stamp=rospy.get_rostime()
			box2_scan.header.frame_id='map'
			box2_scan.angle_min=box2[0]
			box2_scan.angle_max=box2[0]
			box2_scan.range_min=0
			box2_scan.range_max=20
			box2_scan.ranges=[box2[1]]
			pub2.publish(box2_scan)
			print("PUBLISHED")
			
	rate.sleep()

if __name__ == '__main__':
    try:
        costmap_updater()
    except rospy.ROSInterruptException:
        pass
