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

//Flags to suppress the path planning node until exploration complete
bool mappingFinished = true;

//Function to change mappingFinished flag to false once mapping is finished
void movecallback(const actionlib_msgs::GoalID moveCancelled){
  if(moveCancelled.id == ""){
    mappingFinished = false;
  }
}


int main(int argc, char** argv) {
  ros::init(argc, argv, "path_planning_node");
  //Stay in the while loop until mapping is finished. Suppresses path planning until mapping finished
  while (mappingFinished){
    ros::NodeHandle n;
    ros::Subscriber sub = n.subscribe("move_base/cancel", 10, movecallback);
  }
  tf::TransformListener tf(ros::Duration(10));      
  costmap_2d::Costmap2DROS lcr("cleaning_costmap", tf);

  ros::Duration(5).sleep();
  CleaningPathPlanning clr(&lcr);
  clr.GetPathInROS();

  ros::Rate r(1);
  while(ros::ok()){    
    clr.PublishCoveragePath();
    ros::spinOnce();
    r.sleep();
  }
  ros::shutdown();
  return 0;
}

