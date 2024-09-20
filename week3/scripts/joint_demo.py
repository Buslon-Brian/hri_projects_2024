#!/usr/bin/python3
# license removed for brevity
import rospy
import math
from sensor_msgs.msg import JointState


def initialize(js):
    js.header.stamp = rospy.get_rostime()
    js.header.frame_id="Torso"

    js.name.append("HeadYaw") #0
    js.name.append("HeadPitch") #1
    js.name.append("LHipYawPitch") #2
    js.name.append("LHipRoll") #3
    js.name.append("LHipPitch") #5
    js.name.append("LKneePitch") #6
    js.name.append("LAnklePitch") #7
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
    

def talker(pub, rate, js):
    rate.sleep()
    pub.publish(js)
    
def LArmPitch(pub, rate, js, deg):
    js.position[js.name.index("LShoulderPitch")] = math.radians(deg)
    rate.sleep()
    pub.publish(js)

if __name__ == '__main__':
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    js = JointState()
    
    try:
        initialize(js)
        LArmPitch(pub, rate, js, 0)
        LArmPitch(pub, rate, js, 90)

        
        
    except rospy.ROSInterruptException:
        pass