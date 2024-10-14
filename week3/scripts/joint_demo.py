#!/usr/bin/python3
# license removed for brevity
import rospy
from sensor_msgs.msg import JointState
import math

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
    
def LShoulder(pub, rate, js, p, r):
    js.position[js.name.index("LShoulderPitch")] = math.radians(p)
    js.position[js.name.index("LShoulderRoll")] = math.radians(r)
    rate.sleep()
    pub.publish(js)
    initialize(js)

def Head(pub, rate, js, p, y):
    js.position[js.name.index("HeadPitch")] = math.radians(p)
    js.position[js.name.index("HeadYaw")] = math.radians(y)
    rate.sleep()
    pub.publish(js)
    initialize(js)

def wave(pub, rate, js,):
    initialize(js)
    LShoulder(pub, rate, js, 0, 0)
    for i in range(0,-45, -5):
        LShoulder(pub, rate, js, i, 0)
    
    
    # js.position[js.name.index("LHand")] = math.radians(80)
   
    for i in range(0, 45, 5):
        LShoulder(pub, rate, js, -45, i)

    for i in range(45, 0, -5):        
        LShoulder(pub, rate, js, -45, i)
    
    for i in range(0, 45, 5):
        LShoulder(pub, rate, js, -45, i)
    
    for i in range(45, 0, -5):        
        LShoulder(pub, rate, js, -45, i)
    
    for i in range(-45, 0, 5):
        LShoulder(pub, rate, js, i, 0)
   
    # js.position[js.name.index("LHand")] = math.radians(0)

def head_shake(pub, rate, js):
    initialize(js)
    for i in range(0, 45, 5):
        Head(pub, rate, js, 0, i)
        
    for i in range (45, -45, -5):        
        Head(pub, rate, js, 0, i)

    for i in range(-45, 0, 5):
        Head(pub, rate, js, 0, i)

def head_nod(pub, rate, js):
    initialize(js)
    
    for i in range(0, 45 , 5):
        Head(pub, rate, js, i, 0)
    
    for i in range(45, 0, -5):
        Head(pub, rate, js, i, 0)
        
    for i in range(0, 45 , 5):
        Head(pub, rate, js, i, 0)
    
    for i in range(45, 0, -5):
        Head(pub, rate, js, i, 0)

if __name__ == '__main__':
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    js = JointState()
    
    try:
        wave(pub, rate, js)    
        head_shake(pub, rate, js)
        head_nod(pub, rate, js)
        
        
    except rospy.ROSInterruptException:
        pass