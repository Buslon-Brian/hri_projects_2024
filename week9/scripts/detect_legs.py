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

        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.sub = rospy.Subscriber("/odom", Odometry, self.odom_callback)
        self.sub = rospy.Subscriber('people_tracker_measurements', PositionMeasurementArray, self.tracker_callback)
        self.laser = rospy.Subscriber('base_scan', LaserScan, self.laser_callback)
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
    

#clockwise is a boolean true or false
def turn(odom, twist, rate, deg, clockwise):
    if clockwise == True:
        c = -1

    else: 
        c = 1
        deg = abs(360 - deg)
        print(deg)
        
        

    start = odom.get_yaw(odom.get_odom())
    twist.angular.z = 0.5 * c
    odom.pub.publish(twist)
    radians = math.radians(deg)

    while not rospy.is_shutdown():

        odom.pub.publish(twist)
        cur = odom.get_yaw(n.get_odom())
        arcdist = math.fabs(cur - start)

        if clockwise == True:
            if arcdist > radians:
                twist.angular.z = 0.0
                odom.pub.publish(twist)
                break

        else:
            #causes it to turn jsut a but too much, counteract it later?
            if arcdist == 0:
                odom.pub.publish(twist)

            elif arcdist < radians:
                twist.angular.z = 0.0
                odom.pub.publish(twist)
                break  

        rate.sleep()

def search(odom, twist, rate,):
    person_detected = True
    
    while person_detected == False:
        turn(odom, twist, rate, 360)
    

if __name__ == '__main__':
    rospy.init_node('move')
    
    rate = rospy.Rate(10)
    t = Twist()
    n = MoveOdom()
    
    while not rospy.is_shutdown():
    
        #if people found,
        while len(n.detect_person().people) > 0:
            
            #choose most reliable 
            target = max(n.detect_person().people,  key = attrgetter('reliability'))
    
            #calculate difference in angle
            target_angle = math.atan2(target.pos.y, target.pos.x)
            print(math.degrees(target_angle))
            
            #start moving unless object nearby
            if n.get_nearest() > 0.5:
                t.linear.x = 1
                
                if abs(math.degrees(target_angle)) > 10:
                    t.angular.z = math.copysign(1, target_angle)
            
                else:
                    t.angular.z = 0

                n.pub.publish(t)
                    

            else:
                t.linear.x = 0
                t.angular.z = 0
                n.pub.publish(t)

        
        print("person not detected")
        t.linear.x = 0
        t.angular.z = 0
        n.pub.publish(t)