#!/usr/bin/env python
import rospy
import detect_obstacles
from geometry_msgs.msg import Twist

class MoveForward():

    def __init__(self):
        rospy.init_node('forwardPublisher', anonymous=False)
        rospy.on_shutdown(self.shutdown)
        rospy.loginfo("To stop Jupyter press CTRL + C")
        self.cmd_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)
        rate = rospy.Rate(5)
        move = Twist()
        move.linear.x = 0.1
        # move.angular.z = -0.6
        obstacleDetector = detect_obstacles()

        while not rospy.is_shutdown():
            self.cmd_vel.publish(move)
            print(obstacleDetector.possiblePaths())
            rate.sleep()
    
    def shutdown(self):
        rospy.loginfo("Stop Jupyter")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    MoveForward()
    # try:
    #     MoveForward()
    # except:
    #     rospy.loginfo("MoveForward node terminated.")