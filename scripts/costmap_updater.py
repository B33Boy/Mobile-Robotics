#!/usr/bin/env python
import rospy, math
from visualization_msgs.msg import Marker
from ar_track_alvar_msgs.msg import AlvarMarkers
from sensor_msgs.msg import LaserScan


box=[0,19,6]
time=[0.0,0.0]

# Callback to save package boundaries and timestamp of scan
def callback(data):
	global box, time
	box[0]=math.atan2(data.markers[0].pose.pose.position.y,data.markers[0].pose.pose.position.x)
	box[1]=math.sqrt(data.markers[0].pose.pose.position.x*data.markers[0].pose.pose.position.x+data.markers[0].pose.pose.position.y*data.markers[0].pose.pose.position.y)
	box[2]=data.markers[0].id
	time[0]=data.markers[0].header.stamp.secs
	time[1]=data.markers[0].header.stamp.nsecs
	

# Function to update costmap 
def costmap_updater():
    # Initialize a node to update costmap
	rospy.init_node('costmap_updater', anonymous=True)
	
	# Initialize subscriber to box_local_marker topic
	rospy.Subscriber('box_local_marker', AlvarMarkers, callback)

    # Initialize publisher to scan_1 topic
	pub1 = rospy.Publisher('scan_1', LaserScan, queue_size=100)
	
	rate = rospy.Rate(3)
    
	while not rospy.is_shutdown():
		global box, time
		
		# Create a LaserScan message and publish to box1_scan topic
		box1_scan=LaserScan()
		box1_scan.header.stamp.secs=time[0]
		box1_scan.header.stamp.nsecs=time[1]
		box1_scan.header.frame_id='map'
		box1_scan.angle_min=box[0]
		box1_scan.angle_max=box[0]+0.0001
		box1_scan.range_min=0
		box1_scan.range_max=20
		box1_scan.angle_increment=0.0001
		box1_scan.time_increment=0.0001
		box1_scan.ranges=[box[1],box[1]]

		pub1.publish(box1_scan)
			
	rate.sleep()

if __name__ == '__main__':
    try:
        costmap_updater()
    except rospy.ROSInterruptException:
        pass
