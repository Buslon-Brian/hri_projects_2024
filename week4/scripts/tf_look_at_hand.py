#!/usr/bin/python3
import rospy

import math
import tf2_ros
from sensor_msgs.msg import JointState
import geometry_msgs.msg

# this is based on the ROS tf2 tutorial: http://wiki.ros.org/tf2/Tutorials/Writing%20a%20tf2%20listener%20%28Python%29
 
prev_pitch = 0

def callback(data):
    overwrite = JointState()
    overwrite.header = data.header
    overwrite.name = list(data.name)
    overwrite.position = list(data.position)
    # pub.publish(overwrite) #probably causes head stuttering
    # rate.sleep() #section can be delayed unless Rate is large
    # print("why so delayed?") 

    try:
        trans = tfBuffer.lookup_transform('Head', 'LFinger13_link', rospy.Time(0))
        hf_pitch = math.atan2(trans.transform.translation.x, trans.transform.translation.z)
        hf_yaw = math.atan2(trans.transform.translation.y, trans.transform.translation.x)
        overwrite.position[overwrite.name.index("HeadPitch")] = math.radians(hf_pitch*40)
        overwrite.position[overwrite.name.index("HeadYaw")] = math.radians(hf_yaw*40)

        pub.publish(overwrite)
        print(overwrite)
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
    rate = rospy.Rate(100)

    init = JointState() #doesn't fix transform issue
    pub.publish(init)
    rate.sleep()
    
    rospy.spin()
