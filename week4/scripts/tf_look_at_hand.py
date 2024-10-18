#!/usr/bin/python3
import rospy

import math
import tf2_ros
from sensor_msgs.msg import JointState
import geometry_msgs.msg

# this is based on the ROS tf2 tutorial: http://wiki.ros.org/tf2/Tutorials/Writing%20a%20tf2%20listener%20%28Python%29
 


def callback(data):
    overwrite = JointState()
    overwrite.header = data.header
    overwrite.name = list(data.name)
    overwrite.position = list(data.position)

    try:
        trans = tfBuffer.lookup_transform('Head', 'LForeArm', rospy.Time(0))    
        hf_pitch = math.atan2(trans.transform.translation.z, trans.transform.translation.x)
        hf_yaw = math.atan2(trans.transform.translation.x, trans.transform.translation.y)
        diffp = math.degrees(overwrite.position[overwrite.name.index("HeadPitch")] - hf_pitch )
        diffa = math.degrees(overwrite.position[overwrite.name.index("HeadYaw")] - hf_yaw)


        # if the differenece of angles between pitch and yaw are near identical, do nothing
        if abs(diffa) < 1 and abs(diffp) < 1:
            print("skip")
            return
        
        else:
            print("overwrite")
            overwrite.position[overwrite.name.index("HeadPitch")] = hf_pitch
            overwrite.position[overwrite.name.index("HeadYaw")] = hf_yaw

        pub.publish(overwrite)
        rate.sleep()
        
    except (tf2_ros.LookupException):
        print("Failed to get transform, skipping")
        pub.publish(overwrite)
        return    


if __name__ == '__main__':
    rospy.init_node('tf2_look_at_hand')
    
    
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)  
    rospy.Subscriber('joint_states_input', JointState, callback)    
    rate = rospy.Rate(10)

    init = JointState() #doesn't fix transform issue
    pub.publish(init)
    rate.sleep()
    
    rospy.spin()


