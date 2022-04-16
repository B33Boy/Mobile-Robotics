#include "CleaningPathPlanner.h"
#include <boost/shared_ptr.hpp>
#include <costmap_2d/costmap_2d_ros.h>
#include "actionlib_msgs/GoalID.h"
#include "std_msgs/Int32.h"

namespace cm = costmap_2d;
namespace rm = geometry_msgs;

using std::vector;
using rm::PoseStamped;
using std::string;
using cm::Costmap2D;
using cm::Costmap2DROS;

bool mappingFinished = true;
bool counterFlag = true;

//Function to set variable false when mapping is complete
void movecallback(const actionlib_msgs::GoalID moveCancelled){
  if(moveCancelled.id == ""){
    mappingFinished = false;
  }
}

//Function to set variable false when 2 boxes have been detected
void counterback(const std_msgs::Int32 numBoxesDetected){  
	if (numBoxesDetected.data >= 2){
    counterFlag = false;
  }
}

int main(int argc, char** argv) {
  ros::init(argc, argv, "path_planning_node");//hjr
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("move_base/cancel", 10, movecallback);
  ros::Subscriber sub1 = n.subscribe("box_counter", 10, counterback);
  // Suppress search algorithm until mapping is finished
  while (mappingFinished){
		ros::spinOnce();
  }
  tf::TransformListener tf(ros::Duration(10));
  //Run once this activates.
           
  costmap_2d::Costmap2DROS lcr("cleaning_costmap", tf);
  //planner_costmap_ros_->pause();

  ros::Duration(5).sleep();
  CleaningPathPlanning clr(&lcr);
  clr.GetPathInROS();
  //clr.GetBorderTrackingPathInROS();
  ros::Rate r(1);
  // Search until two boxes found
  while(ros::ok() and counterFlag){    
    clr.PublishCoveragePath();
    ros::spinOnce();
    r.sleep();
  }
  ros::shutdown();
  return 0;
}

