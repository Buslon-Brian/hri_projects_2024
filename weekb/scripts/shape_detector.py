#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
import math
from sensor_msgs.msg import LaserScan
from people_msgs.msg import PositionMeasurementArray
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from operator import attrgetter


class MoveOdom:
    def __init__(self):
        self.odom = Odometry()

        self.pub = rospy.Publisher("robot_0/cmd_vel", Twist, queue_size=10)
        self.sub = rospy.Subscriber("robot_0/odom", Odometry, self.odom_callback)
        self.sub = rospy.Subscriber('people_tracker_measurements', PositionMeasurementArray, self.tracker_callback)
        self.laser = rospy.Subscriber('robot_0/base_scan', LaserScan, self.laser_callback)
        rospy.sleep( rospy.Duration.from_sec(0.5) )

    def odom_callback(self, msg):
        self.odom = msg

    def get_odom(self):
        return self.odom

    def get_yaw (self, msg):
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
        return yaw
    
    def tracker_callback(self, msg):
        self.tracker = msg

    def detect_person(self):
        return self.tracker
    
    def laser_callback(self, msg):
        self.laser = msg

    def get_nearest(self):
        return min(self.laser.ranges)


if __name__ == '__main__':
    rospy.init_node('move')
    
    rate = rospy.Rate(10)
    t = Twist()
    n = MoveOdom()
    
    while not rospy.is_shutdown():

        people = n.detect_person().people
        for person in people:
            x = person.pos.x
            y = person.pos.y
            print(f"{x} {y}")

        print("////////")
            



        rate.sleep()