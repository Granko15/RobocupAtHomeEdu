#!/usr/bin/env python
import rospy
# import detect_obstacles
from geometry_msgs.msg import Twist

class MoveAround():

    def __init__(self):
        rospy.init_node('forwardPublisher', anonymous=False)
        rospy.on_shutdown(self.shutdown)
        rospy.loginfo("To stop Jupyter press CTRL + C")
        self.cmd_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)
        self.move = Twist()
        # self.freePathsListener = rospy.Subscriber('freePaths', DetectedObstacles, self.freePathCallback)
        rate = rospy.Rate(2)

        while not rospy.is_shutdown():
            # self.turnLeft()
            self.turnRight()
            
    
    def shutdown(self):
        rospy.loginfo("Stop Jupyter")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

    def moveForward(self):
        self.move.linear.x = 0.1
        self.cmd_vel.publish(self.move)

    def moveBackward(self):
        self.move.linear.x = 0.1
        self.cmd_vel.publish(self.move)

    def turnLeft(self):
        self.move.linear.x = 0.05
        self.move.angular.z = 1
        self.cmd_vel.publish(self.move)

    def turnRight(self):
        self.move.linear.x = 0.05
        self.move.angular.z = -1
        self.cmd_vel.publish(self.move)

    def freePathCallback(self):
        # TODO
        print("not done")

if __name__ == '__main__':
    MoveAround()
    # try:
    #     MoveAround()
    # except:
    #     rospy.loginfo("MoveForward node terminated.")