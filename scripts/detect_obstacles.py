#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

# nefunguje z nejakeho dovodu
from matus_showcase.msg import DetectedObstacles

from math import *


class DetectObstacles:

    def __init__(self):
        rospy.init_node('obstaclePublisher', anonymous=False)
        rospy.loginfo("To stop Jupyter press CTRL + C")
        rospy.on_shutdown(self.shutdown)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.callback)
        
        # init publishera ktory dava custom message
        self.pub = rospy.Publisher('freePaths', DetectedObstacles)

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
            # volam publishovanie custom messagu
            self.publisPathsMessage()

            print(self.possiblePaths())
            rospy.sleep(1)
    
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
    
    #publishujem svoj custom message
    def publisPathsMessage(self):
        msg = DetectedObstacles
        msg.front = 1 if self.directionObstacles["Front"] else 0
        msg.frontRight = 1 if self.directionObstacles["FrontRight"] else 0
        msg.right = 1 if self.directionObstacles["Right"] else 0
        msg.backRight = 1 if self.directionObstacles["BackRight"] else 0
        msg.back = 1 if self.directionObstacles["Back"] else 0
        msg.backLeft = 1 if self.directionObstacles["BackLeft"] else 0
        msg.left = 1 if self.directionObstacles["Left"] else 0
        msg.frontLeft = 1 if self.directionObstacles["FrontLeft"] else 0
        self.pub.publish(msg)

if __name__ == '__main__':
    DetectObstacles()
    # try:
    #     DetectObstacles()
    # except:
    #     rospy.loginfo("obstaclePublisher node terminated.")