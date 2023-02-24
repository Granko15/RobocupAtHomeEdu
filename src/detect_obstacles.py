#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan 
from math import *


class DetectObstacles:

    def __init__(self):
        rospy.init_node('obstaclePublisher', anonymous=False)
        rospy.loginfo("To stop Jupyter press CTRL + C")
        rospy.on_shutdown(self.shutdown)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.callback)
        self.rate = rospy.Rate(5)
        self.detectionRange = 0.5
        # directionRanges = [front, frontRight, right, backRight, back, backLeft, left, frontLeft]
        self.directionRanges = [[] for _ in range(8)]
        self.directionObstacles = {
            "Front" : False,
            "FrontRight" : False,
            "Right" : False,
            "BackRight" : False,
            "Back" : False,
            "BackLeft" : False,
            "Left" : False,
            "FrontLeft" : False
        }
        while not rospy.is_shutdown():
            # for direction, obstacle in self.directionObstacles.items():
            #     print(direction, " > ", obstacle)
            print(self.possiblePaths())
            # rospy.spin()
            rospy.sleep(5)
    
    def shutdown(self):
        rospy.loginfo('Stop jupyter')
        rospy.sleep(10)

    def callback(self, msg):
        self.directionRanges[0] = msg.ranges[355:359] + msg.ranges[0:4]
        angle = 45
        for i in range(len(self.directionRanges) - 1):
            self.directionRanges[i+1] = msg.ranges[angle - 5 : angle + 5]
            angle += 45
        self.checkDistances()

    def checkDistances(self):
        obstacle = False
        # Front
        for i in self.directionRanges[0]:
            if not isinf(i):
                if i <= self.detectionRange:
                    obstacle = True
                    break
        self.directionObstacles['Front'] = obstacle
        obstacle = False
            
        # FrontRight
        for i in self.directionRanges[1]:
            if not isinf(i):
                if i <= self.detectionRange:
                    obstacle = True
                    break
        self.directionObstacles['FrontRight'] = obstacle
        obstacle = False

        # Right
        for i in self.directionRanges[2]:
            if not isinf(i):
                if i <= self.detectionRange:
                    obstacle = True
                    break
        self.directionObstacles['Right'] = obstacle
        obstacle = False

        # BackRight
        for i in self.directionRanges[3]:
            if not isinf(i):
                if i <= self.detectionRange:
                    obstacle = True
                    break
        self.directionObstacles['BackRight'] = obstacle
        obstacle = False

        # Back
        for i in self.directionRanges[4]:
            if not isinf(i):
                if i <= self.detectionRange:
                    obstacle = True
                    break
        self.directionObstacles['Back'] = obstacle
        obstacle = False

        # BackLeft
        for i in self.directionRanges[5]:
            if not isinf(i):
                if i <= self.detectionRange:
                    obstacle = True
                    break
        self.directionObstacles['BackLeft'] = obstacle
        obstacle = False

        # Left
        for i in self.directionRanges[6]:
            if not isinf(i):
                if i <= self.detectionRange:
                    obstacle = True
                    break
        self.directionObstacles['Left'] = obstacle
        obstacle = False

        # FrontLeft
        for i in self.directionRanges[7]:
            if not isinf(i):
                if i <= self.detectionRange:
                    obstacle = True
                    break
        self.directionObstacles['FrontLeft'] = obstacle

    def possiblePaths(self):
        return [i[0] for i in self.directionObstacles.items() if not i[1]]


if __name__ == '__main__':
    try:
        DetectObstacles()
    except:
        rospy.loginfo("obstaclePublisher node terminated.")