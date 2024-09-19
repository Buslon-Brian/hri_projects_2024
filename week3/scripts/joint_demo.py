#!/usr/bin/python3
# license removed for brevity
import rospy
import math

from sensor_msgs.msg import JointState

def talker():
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 10hz

    # set initial angle
    angle = 0


    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        js = JointState()
        
        # header info
        js.header.stamp = rospy.get_rostime()
        js.header.frame_id="Torso"


        # put in some joints that we'll edit
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
        js.name.append("LElbbowYaw")
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


        #default positions for limbs
        #js.position.append(math.radians(angle))
        js.position.append(math.radians(angle))
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
        
        #comment this out once it gets noisy
        rospy.loginfo(js)
        
        pub.publish(js)
        angle = angle + 1
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass