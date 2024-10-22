#!/usr/bin/python3
import rospy

import math
import tf2_ros
import tf
from sensor_msgs.msg import JointState
import geometry_msgs.msg

# this is based on the ROS tf2 tutorial: http://wiki.ros.org/tf2/Tutorials/Writing%20a%20tf2%20listener%20%28Python%29

hf_pitch = 0

def callback(data):
    overwrite = JointState()
    overwrite.header = data.header
    overwrite.name = list(data.name)
    overwrite.position = list(data.position)

    try:
        # br.sendTransform((1.0, 0.0, 0.0), (0.0, 0.0, 0.0, 1.0), rospy.Time.now(), "l_point", "LForeArm")
        trans = tfBuffer.lookup_transform('torso', 'l_gripper', rospy.Time(0))    
        trans2 = tfBuffer.lookup_transform('torso', 'l_gripper', rospy.Time(0))    
        hf_pitch = math.radians(45)
        hf_yaw = 0

        #Absoulte angle 180 is with reference to the torso, because it never moves
        # pitch and yaw + .05 should add up to a meter ahead? 
        if len(overwrite.position) != 0:
            hf_yaw = math.atan2(trans.transform.translation.y -.05, trans.transform.translation.x + .05) 
        hf_pitch += math.atan2(-trans2.transform.translation.z -.05, trans2.transform.translation.x + .05)
    
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
    br = tf.TransformBroadcaster()
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)  
    rospy.Subscriber('joint_states_input', JointState, callback)    
    rate = rospy.Rate(10)

    init = JointState() #doesn't fix transform issue
    pub.publish(init)
    rate.sleep()
    
    rospy.spin()
