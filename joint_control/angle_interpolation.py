'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes import * 


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])
        self.T_s = -1
        
    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE
        (names, times, keys) = keyframes

        if(self.T_s == -1):
            self.T_s = perception.time            
        time = perception.time - self.T_s

        for j, joint_name in enumerate(names):
           
           if joint_name not in self.joint_names: #check if the name is really a joint name
                continue
            
            t_joint = times[j]
            k_joint = keys[j]
           
           if time > t_joint[-1]: #when time > last item in the joints, skip the loop below
                target_joints[joint_name] = perception.joint[joint_name]
                continue

            for t in range(len(t_joint)):
                
                if time < t_joint[t]:
                    
                    if t==0: #we don't have a preceding point, so initialize to zero
                        T_0, P_0, P_1 = 0  
                        T_3 = t_joint[0]
                        P_2 = k_joint[0][1][2]
                        P_3 = k_joint[0][0]
                        i = time / T_3
                        
                    elif time > t_joint[t-1]:  #we found the right interval for interpolation
                        
                        T_0, T_3 = t_joint[t-1], t_joint[t]
                        P_0, P_3 = k_joint[t-1], k_joint[t]
                        P_1 = P_0 + k_joint[t-1][2][2]
                        P_2 = P_3+ k_joint[t][1][2]                       
                        i = (time - T_0)/(T_3 -T_0) #normalize i to be in [0,1]

                    target_joints[joint_name] = ((1-i)**3)*P_0 + 3*((1-i)**2)*i*P_1 + 3*((1-i)**3)*(i**2)*P_2 +(i**3)*P_3
                    #from the formula in the slides for cubic Bezier
                    break
        
        return target_joints

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
