#!/usr/bin/python3
# license removed for brevity
import rospy
import math
import time
from sensor_msgs.msg import JointState


def initialize(js):
    js.header.stamp = rospy.get_rostime()
    js.header.frame_id="Torso"

    js.name.append("HeadYaw")
    js.name.append("HeadPitch")
    js.name.append("LHipYawPitch")
    js.name.append("LHipRoll")
    js.name.append("LHipPitch")
    js.name.append("LKneePitch")
    js.name.append("LAnklePitch")
    js.name.append("LAnkleRoll")
    js.name.append("LShoulderPitch")
    js.name.append("LShoulderRoll")
    js.name.append("LElbowYaw")
    js.name.append("LElbowRoll")
    js.name.append("LWristYaw")
    js.name.append("LHand")
    js.name.append("RHipYawPitch")
    js.name.append("RHipRoll")
    js.name.append("RHipPitch")
    js.name.append("RKneePitch")
    js.name.append("RAnklePitch")
    js.name.append("RAnkleRoll")
    js.name.append("RShoulderPitch")
    js.name.append("RShoulderRoll")
    js.name.append("RElbowYaw")
    js.name.append("RElbowRoll")
    js.name.append("RWristYaw")
    js.name.append("RHand")

    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)

def headback(js):
    js.position[0] = math.radians(180)

def headleft(js):
    js.position[0] = math.radians(90)

def talker(pub, rate, js):
    headleft(js)
    rate.sleep()
    pub.publish(js)
    

def talker2(pub, rate, js):
    headback(js)
    rate.sleep()
    pub.publish(js)
    

if __name__ == '__main__':
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    js = JointState()
    
    try:
        initialize(js)
        talker(pub, rate, js)
        talker2(pub, rate, js)
    except rospy.ROSInterruptException:
        pass