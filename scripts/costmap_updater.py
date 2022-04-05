#!/usr/bin/env python
from operator import truediv
import rospy, math
from visualization_msgs.msg import Marker
from ar_track_alvar_msgs.msg import AlvarMarkers
from sensor_msgs.msg import LaserScan


box1=[0,19,6]
time1=[0.0,0.0]
box2=[0,19,6]
time2=[0.0,0.0]
flag1 = True
flag2 = True

# Callback to save package boundaries and timestamp of scan
def callback(data):
	global box1, time1, box2, time2, flag1, flag2
	if (data.markers[0].id==0 or data.markers[0].id==1):
		box1[0]=math.atan2(data.markers[0].pose.pose.position.y,data.markers[0].pose.pose.position.x)
		box1[1]=math.sqrt(data.markers[0].pose.pose.position.x*data.markers[0].pose.pose.position.x+data.markers[0].pose.pose.position.y*data.markers[0].pose.pose.position.y)
		box1[2]=data.markers[0].id
	if (data.markers[0].id==2 or data.markers[0].id==3):
		box2[0]=math.atan2(data.markers[0].pose.pose.position.y,data.markers[0].pose.pose.position.x)
		box2[1]=math.sqrt(data.markers[0].pose.pose.position.x*data.markers[0].pose.pose.position.x+data.markers[0].pose.pose.position.y*data.markers[0].pose.pose.position.y)
		box2[2]=data.markers[0].id

# Function to update costmap 
def costmap_updater():
    # Initialize a node to update costmap
	rospy.init_node('costmap_updater', anonymous=True)
	
	# Initialize subscriber to box_local_marker topic
	#rospy.Subscriber('box_local_marker', AlvarMarkers, callback)
	rospy.Subscriber('ar_pose_marker', AlvarMarkers, callback)

    # Initialize publisher to scan_1 topic
	pub1 = rospy.Publisher('scan_1', LaserScan, queue_size = 10)
	pub2 = rospy.Publisher('scan_2', LaserScan, queue_size = 10)
	
	rate = rospy.Rate(1)
    
	while not rospy.is_shutdown():
		global box1, time1, box2, time2
		
		# Create a LaserScan message and publish to box1_scan topic
		box1_scan=LaserScan()
		box1_scan.header.stamp=rospy.get_rostime()
		box1_scan.header.frame_id='map'
		box1_scan.angle_min=box1[0]
		box1_scan.angle_max=box1[0]+0.0001
		box1_scan.range_min=0
		box1_scan.range_max=20
		box1_scan.angle_increment=0.0001
		box1_scan.time_increment=0.0001
		box1_scan.ranges=[box1[1]+0.025,box1[1]+0.025]
		pub1.publish(box1_scan)

		box2_scan=LaserScan()
		box2_scan.header.stamp=rospy.get_rostime()
		box2_scan.header.frame_id='map'
		box2_scan.angle_min=box2[0]
		box2_scan.angle_max=box2[0]+0.0001
		box2_scan.range_min=0
		box2_scan.range_max=20
		box2_scan.angle_increment=0.015
		box2_scan.time_increment=0.0001
		box2_scan.ranges=[box2[1]+0.025,box2[1]+0.025]
		pub2.publish(box2_scan)
			
	rate.sleep()

if __name__ == '__main__':
    try:
        costmap_updater()
    except rospy.ROSInterruptException:
        pass
