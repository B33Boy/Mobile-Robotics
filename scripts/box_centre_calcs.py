#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import String, Int32
from ar_track_alvar_msgs.msg import AlvarMarkers
from visualization_msgs.msg import Marker

# Flag used to ensure home goal is only sent once
packageOneFlag = False
packageTwoFlag = False
Q = [0,0,0,0]
boxInfo = [5,5,5,5]
#boxReference = {'ids': 0,1,2,3, 'width': 10,5,10,5, 'height': 5,5,5,5, 'depth': 5,10,5,10}

def callback(data):
    """
    Callback function to check and parse the aruco markers' pose with respect to the camera
 
    Input
    :param data: data of the message received on a topic that is of hierarchial structure
 
    Output
    :return: 
    """

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

def publish_marker_wrt_map(boxInfo, Q, boxTopID, boxSideID, pub_topic, color=[0,0,0,1]):

	marker=Marker()
	marker.header.stamp=rospy.get_rostime()

	# Ensure that the marker is plotted wrt to map frame
	marker.header.frame_id='map'

	# Indicates marker is a cube
	marker.type=1

	# Indicates that we want to add/modify object
	marker.action=0
	# Set position of box
	marker.pose.position.x = boxInfo[1]
	marker.pose.position.y = boxInfo[2]
	marker.pose.position.z = boxInfo[3]

	# Scale box side lengths depending on top or side marker 
	if (boxInfo[0]==boxTopID):
		marker.scale.x=0.10
		marker.scale.y=0.05
		marker.scale.z=0.05

	if (boxInfo[0]==boxSideID):
		marker.scale.x=0.05
		marker.scale.y=0.05
		marker.scale.z=0.10

	# Set orientation of box
	marker.pose.orientation.x=Q[0]
	marker.pose.orientation.y=Q[1]
	marker.pose.orientation.z=Q[2]
	marker.pose.orientation.w=Q[3]

	marker.color.g=color[0]
	marker.color.r=color[1]
	marker.color.b=color[2]
	marker.color.a=color[3]

	pub_topic.publish(marker)


#function to send the robot the origin as a goal when exploration is complete
def box_locator():

    """
    Function to create ROS nodes to utilize AlvarMarkers to check and parse the aruco markers' pose with respect to the camera

    Output
    :return: returns nothing
    """

    # Initialize ROS node called box_locator
	rospy.init_node('box_locator', anonymous=True)

	# Initialize subscriber to ar_pose_marker topic and call the callback function when data arrives
	rospy.Subscriber('ar_pose_marker', AlvarMarkers, callback)
	
	# Initialize ROS publisher to publish pose of markers
	pub1 = rospy.Publisher('visualization_marker_1', Marker, queue_size=100)
	pub2 = rospy.Publisher('visualization_marker_2', Marker, queue_size=100)
	
	# Initialize ROS publisher to publish number of boxes detected
	pub_counter = rospy.Publisher('box_counter', Int32, queue_size=10)
	
	rate = rospy.Rate(30)
    
	# Loop to keep the nodes going until crtl-c is pressed
	while not rospy.is_shutdown():
		global boxInfo

		# Check if the 0 or 1 marker ID (corresponding to 1st package) is detected 
		if (boxInfo[0]==0 or boxInfo[0]==1):
			global packageOneFlag

			# Set the packageOneFlag to True to ensure detection only happens once 
			if (packageOneFlag==False):
				packageOneFlag = True
				
<<<<<<< Updated upstream
				# Declare a new Marker object
				marker1=Marker()
				marker1.header.stamp=rospy.get_rostime()

				# Ensure that the marker is plotted wrt to map frame
				marker1.header.frame_id='map'
				
				# Indicates marker is a cube
				marker1.type=1

				# Indicates that we want to add/modify object
				marker1.action=0
				
				# Set position of box
				marker1.pose.position.x = boxInfo[1]
				marker1.pose.position.y = boxInfo[2]
				marker1.pose.position.z = boxInfo[3]
				
				# Scale box side lengths depending on top or side marker 
				if (boxInfo[0]==0):
					marker1.scale.x=0.10
					marker1.scale.y=0.05
					marker1.scale.z=0.05
				if (boxInfo[0]==1):
					marker1.scale.x=0.05
					marker1.scale.y=0.05
					marker1.scale.z=0.10
				
				# Set orientation of box
				marker1.pose.orientation.x=Q[0]
				marker1.pose.orientation.y=Q[1]
				marker1.pose.orientation.z=Q[2]
				marker1.pose.orientation.w=Q[3]
				
				# Set colour and transparency
				marker1.color.g=0
				marker1.color.r=0
				marker1.color.b=1
				marker1.color.a=1

				pub1.publish(marker1)
=======
				publish_marker_wrt_map(boxInfo, Q, 0, 1, pub1, [0,0,1,1])
>>>>>>> Stashed changes
			
		# Check if the 2 or 3 marker ID (corresponding to 2nd package) is detected 	
		elif (boxInfo[0]==2 or boxInfo[0]==3):
			global packageTwoFlag

			# Set the packageTwoFlag to True to ensure detection only happens once 
			if (packageTwoFlag==False):
				packageTwoFlag = True

				# Declare a new Marker object
				marker2=Marker()
				marker2.header.stamp=rospy.get_rostime()
	
				# Ensure that the marker is plotted wrt to map frame
				marker2.header.frame_id='map'

				# Indicates marker is a cube
				marker2.type=1
				
				# Indicates that we want to add/modify object
				marker2.action=0
				
				# Set position of box
				marker2.pose.position.x = boxInfo[1]
				marker2.pose.position.y = boxInfo[2]
				marker2.pose.position.z = boxInfo[3]
				
<<<<<<< Updated upstream
				# Scale box side lengths depending on top or side marker 				
				if (boxInfo[0]==2):
					marker2.scale.x=0.10
					marker2.scale.y=0.05
					marker2.scale.z=0.05
				if (boxInfo[0]==3):
					marker2.scale.x=0.05
					marker2.scale.y=0.05
					marker2.scale.z=0.10

				# Set orientation of box
				marker2.pose.orientation.x=Q[0]
				marker2.pose.orientation.y=Q[1]
				marker2.pose.orientation.z=Q[2]
				marker2.pose.orientation.w=Q[3]

				# Set colour and transparency
				marker2.color.g=0
				marker2.color.r=1
				marker2.color.b=0
				marker2.color.a=1

				pub2.publish(marker2)
=======
				publish_marker_wrt_map(boxInfo, Q, 2, 3, pub2, [1,0,0,1])
>>>>>>> Stashed changes


		counter=0
		# Set counter depending on how many packages are found
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
