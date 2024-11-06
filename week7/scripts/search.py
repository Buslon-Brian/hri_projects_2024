#!/usr/bin/env python

# imports
import rospy
import math
import tf2_ros
import geometry_msgs.msg
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from sensor_msgs.msg import LaserScan

global nearest 

# Odom class
class MoveOdom:
    def __init__(self):
        self.odom = Odometry()
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.sub = rospy.Subscriber("/odom", Odometry, self.odom_callback)
        self.near = rospy.Subscriber('base_scan', LaserScan, self.xcallback)
        rospy.sleep(rospy.Duration.from_sec(0.5))

    def odom_callback(self, msg):
        self.odom = msg

    def get_odom(self):
        return self.odom

    def get_yaw(self, msg):
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
        return yaw
    
    def xcallback(self, data):
        self.near = min(data.ranges)
    

def turn(odom, twist, rate, deg, clockwise):
    print('?')
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
        print(arcdist)

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
                print("end")
                twist.angular.z = 0.0
                odom.pub.publish(twist)
                break  

        rate.sleep()

# Main Statement
if __name__ == '__main__':
    rospy.init_node('move')
    rate = rospy.Rate(10)
    n = MoveOdom()
    t = Twist()
    
    while not rospy.is_shutdown():
        if n.near > .5:
            t.linear.x = 1.0
            n.pub.publish(t)

        else:
            t.linear.x = 0
            turn(n, t, rate, 10, True)
            n.pub.publish(t)


    rospy.spin()
