#!/usr/bin/env python
import rospy, math
from std_msgs.msg import String, Int32
from visualization_msgs.msg import Marker
from ar_track_alvar_msgs.msg import AlvarMarkers
from sensor_msgs.msg import LaserScan
import thread, time

#flag used to ensure home goal is only sent once
box=[0,19,6]
time=[0.0,0.0]
#ros return_home subscriber callback function
#Checks if data has been published to move_base/cancel topic and changes flag
def callback1(data):
	global box, time
	box[0]=math.atan2(data.markers[0].pose.pose.position.y,data.markers[0].pose.pose.position.x)
	box[1]=math.sqrt(data.markers[0].pose.pose.position.x*data.markers[0].pose.pose.position.x+data.markers[0].pose.pose.position.y*data.markers[0].pose.pose.position.y)
	box[2]=data.markers[0].id
	time[0]=data.markers[0].header.stamp.secs
	time[1]=data.markers[0].header.stamp.nsecs
	

#function to send the robot the origin as a goal when exploration is complete
def costmap_updater():
    #initialize ros subscriber to move_base/cancel
	rospy.init_node('costmap_updater', anonymous=True)
	rospy.Subscriber('box_local_marker', AlvarMarkers, callback1)
    #initialize ros publisher to move_base_simple/goal
	pub1 = rospy.Publisher('scan_1', LaserScan, queue_size=100)
	rate = rospy.Rate(100)
    #loop to keep the nodes going
	while not rospy.is_shutdown():
    #check is mapping is complete (flag)
		global box, time
		#if (box[2]==0 or box[2]==1 or box[2]==2 or box[2]==3):
		box1_scan=LaserScan()
		box1_scan.header.stamp.secs=time[0]
		box1_scan.header.stamp.nsecs=time[1]
		box1_scan.header.frame_id='base_scan'
		box1_scan.angle_min=box[0]
		box1_scan.angle_max=box[0]
		box1_scan.range_min=0
		box1_scan.range_max=20
		box1_scan.angle_increment=0
		box1_scan.time_increment
		box1_scan.ranges=[box[1]]
		pub1.publish(box1_scan)
			
	rate.sleep()

if __name__ == '__main__':
    try:
        costmap_updater()
    except rospy.ROSInterruptException:
        pass
