#!/usr/bin/env python

#imports
import rospy
import math
import tf2_ros
import geometry_msgs.msg
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler

#Odom class
class MoveOdom:
    def __init__(self):
        self.odom = Odometry()

        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.sub = rospy.Subscriber("/odom", Odometry, self.odom_callback)
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
    
#Move function 1 meter
def move(odom, twist, rate, distance):
    start = odom.get_odom()
    twist.linear.x = 1.0
    odom.pub.publish(twist)

    while not rospy.is_shutdown():
        odom.pub.publish(twist)
        cur = n.get_odom()

        dx = cur.pose.pose.position.x - start.pose.pose.position.x
        dy = cur.pose.pose.position.y - start.pose.pose.position.y
        displacement = math.sqrt( dx*dx + dy*dy )
        
        print(displacement)

        if displacement > distance:
            twist.linear.x = 0.0
            n.pub.publish(twist)
            break
    
        rate.sleep()

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
        print(arcdist)

        if clockwise == True:
            if arcdist > radians:
                twist.angular.z = 0.0
                odom.pub.publish(twist)
                break

        else:
            if arcdist == 0:
                odom.pub.publish(twist)

            elif arcdist < radians:
                print("end")
                twist.angular.z = 0.0
                odom.pub.publish(twist)
                break  

        rate.sleep()
    

#Main Statement
if __name__ == '__main__':
    
    rospy.init_node('move')
    rate = rospy.Rate(10.0)
    
    t = Twist()
    n = MoveOdom()

    # move(n, t , rate, 1)
    turn(n, t , rate, 180, True)
