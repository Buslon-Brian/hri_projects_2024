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
        hf_angle = math.atan2(trans.transform.translation.x, trans.transform.translation.z)

        pitch_index = overwrite.name.index("HeadPitch")
        current_pitch = overwrite.position[pitch_index]
        angle_difference = hf_angle - current_pitch
    
        print("initial pitch:" + str(math.degrees(overwrite.position[overwrite.name.index("HeadPitch")])))
        print("initial angle:" + str(math.degrees(hf_angle)))
        print("initial angle difference:" + str(math.degrees(angle_difference)))
        print(" ")

        if abs(angle_difference) > math.radians(1): #skip overwriting for mall angle differences
            print("overwriting")
            print(" ")
            overwrite.position[pitch_index] += angle_difference
            pub.publish(overwrite)
        
        else:
            print("skipping")
            print(" ")
            pub.publish(overwrite)
        
        rate.sleep()
        
        hf_angle = math.atan2(trans.transform.translation.x, trans.transform.translation.z)
        angle_difference = hf_angle - overwrite.position[overwrite.name.index("HeadPitch")]
        
        print("final pitch:" + str(math.degrees(overwrite.position[overwrite.name.index("HeadPitch")])))
        print("final angle:" + str(math.degrees(hf_angle)))
        print("final angle difference:" + str(math.degrees(angle_difference)))
        print("////")
        print(" ")
        

        
        
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


