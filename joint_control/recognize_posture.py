'''In this exercise you need to use the learned classifier to recognize current posture of robot

* Tasks:
    1. load learned classifier in `PostureRecognitionAgent.__init__`
    2. recognize current posture in `PostureRecognitionAgent.recognize_posture`

* Hints:
    Let the robot execute different keyframes, and recognize these postures.

'''
#versione finale

import pickle, io, numpy as np
from os import *
from angle_interpolation import AngleInterpolationAgent
from keyframes import *

ROBOT_POSE_DATA_DIR = 'robot_pose_data'
ROBOT_POSE_PKL = 'robot_pose.pkl'

class PostureRecognitionAgent(AngleInterpolationAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(PostureRecognitionAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.posture = 'unknown'
        self.posture_classifier = pickle.load(io.open(ROBOT_POSE_PKL))

    def think(self, perception):
        self.posture = self.recognize_posture(perception)
        return super(PostureRecognitionAgent, self).think(perception)

    def recognize_posture(self, perception):
        posture = 'unknown'
        features = ['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 
                    'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch']

        postures = ['Frog', 'Knee', 'Stand', 'Crouch', 'Right', 'Sit', 
                    'Belly', 'Back', 'StandInit', 'HeadBack', 'Left']
        
        
        pred_data  = [self.perception.joint[i] for i in features] +self.perception.imu

        p_ix = self.posture_classifier.predict(np.array(pred_data).reshape(1,-1))[0]
        
        posture = postures[p_ix]
        #print(posture)


        return posture

if __name__ == '__main__':
    agent = PostureRecognitionAgent()
    agent.keyframes = leftBellyToStand()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
