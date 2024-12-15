#!/usr/bin/python3
# license removed for brevity
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import String
from ros_vosk.msg import speech_recognition
import math
import pyttsx3 

class Pirate():
    def __init__(self):
        self.listen = rospy.Subscriber('speech_recognition/vosk_result', speech_recognition, self.words) 
        self.response = rospy.Publisher('joint_states', JointState, queue_size=10)
        self.last_phrase = ""

        self.state = JointState()
        self.state.header.stamp = rospy.get_rostime()
        self.state.header.frame_id = "Torso"

        joint_names = [
            "HeadYaw", "HeadPitch", "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll",
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", 
            "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll",
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"
        ]
        joint_positions = [0] * len(joint_names)  

        self.state.name = joint_names
        self.state.position = joint_positions

    def lshoulder(self, pitch, roll):
        self.state.header.stamp = rospy.get_rostime()
        self.state.header.frame_id="Torso"
        self.state.position[self.state.name.index("LShoulderPitch")] = math.radians(pitch)
        self.state.position[self.state.name.index("LShoulderRoll")] = math.radians(roll)
        self.response.publish(self.state)
        rate.sleep()
    
    def head(self, pitch, yaw):
        self.state.header.stamp = rospy.get_rostime()
        self.state.header.frame_id="Torso"
        self.state.position[self.state.name.index("HeadPitch")] = math.radians(pitch)
        self.state.position[self.state.name.index("HeadYaw")] = math.radians(yaw)
        self.response.publish(self.state)
        rate.sleep()

    def wave(self):
        
        #first is always skipped
        self.lshoulder(0, 0)
        self.lshoulder(0, 0)
        
        for deg in range(0, -60, -5):
            self.lshoulder(deg, 0)

        for deg in range(0, 60, 5):
            self.lshoulder(-60, deg)
        
        for deg in range(60, 0, -5):
            self.lshoulder(-60, deg)

        for deg in range(-60, 0, 5):
            self.lshoulder(deg, 0)    
        
    def shake(self):
        
        #first is always skipped
        self.head(0,0)
        self.head(0,0)
        
        for deg in range(0, 50, 5):
            self.head(0, deg)
            
        for deg in range(50, -50, -5):
            self.head(0, deg)

        for deg in range(-50, 0, 5):
            self.head(0, deg)
    
    def nod(self):
        
        #first is always skipped
        self.head(0,0)
        self.head(0,0)
            
        for deg in range(0, 50, 5):
            self.head(deg, 0)

        for deg in range(50, 0, -5):
            self.head(deg, 0)

    def words(self, msg):
        self.words = msg

        try: 
            self.words.isSpeech_recognized
        
        except AttributeError:
            print("")
       
        else:
            same_phrase = True if self.last_phrase == self.words.time_recognized.secs else False
             
            if self.words.isSpeech_recognized == True and same_phrase == False:
                self.last_phrase = self.words.time_recognized.secs
                print(self.words.final_result)
                
                if 'yes' in self.words.final_result:
                    self.nod()
            
                elif 'no' in self.words.final_result:
                    self.shake()

                elif 'hello' in self.words.final_result:
                    self.wave()

            else: 
                print("")

class Parrot:
    def __init__(self):
        self.listen = rospy.Subscriber('speech_recognition/vosk_result', speech_recognition, self.words) 
        self.repeat = rospy.Publisher('tts/phrase', String, queue_size=0)
        self.tts = pyttsx3.init()
        self.last_phrase = 0

    def words(self,msg):
        self.words = msg

    def speak(self):
        
        self.tts.setProperty('rate', 120)

        try: 
            self.words.isSpeech_recognized
        
        except AttributeError:
            return ""
       
        else:
            same_phrase = True if self.last_phrase == self.words.time_recognized.secs else False
             
            if self.words.isSpeech_recognized == True and same_phrase == False:
                self.last_phrase = self.words.time_recognized.secs
                self.tts.say(self.words.final_result)
                self.tts.runAndWait()
                self.repeat.publish(self.words.final_result)
                return self.words.final_result
            
            else: 
                return ""

if __name__ == '__main__':
    rospy.init_node('pirate', anonymous=True)
    rate = rospy.Rate(5) # 10hz
    Blackbeard = Pirate()
    polly = Parrot()
    
    while not rospy.is_shutdown():
        print(polly.speak())
        rate.sleep()



