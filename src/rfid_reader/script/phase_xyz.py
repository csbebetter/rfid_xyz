#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import message_filters
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
import Levenberg_Marquarelt_algorithm as LM

pub = rospy.Publisher('tagxyzpub', Float32MultiArray, queue_size=10)  #发布话题设为全局变量

class listener():
    def __init__(self,file_input):
        rospy.init_node("multi_receive_node",anonymous=True)
        subcriber_phase1 = message_filters.Subscriber('/DataDev_info1', Float32, queue_size=1)
        subcriber_phase2 = message_filters.Subscriber('/DataDev_info2', Float32, queue_size=1)
        subcriber_phase3 = message_filters.Subscriber('/DataDev_info3', Float32, queue_size=1)
        subcriber_phase4 = message_filters.Subscriber('/DataDev_info4', Float32, queue_size=1)
        sync = message_filters.ApproximateTimeSynchronizer([subcriber_phase1, subcriber_phase2, subcriber_phase3, subcriber_phase4],10,0.1,allow_headerless=True)
        sync.registerCallback(self.multi_callback)
        file=file_input

    def multi_callback(self,recieve_phase1,recieve_phase2,recieve_phase3,recieve_phase4):
        arr_lambda_data=[0,0,0,0]
        arr_lambda_data[0]=recieve_phase1.data
        arr_lambda_data[1]=recieve_phase2.data
        arr_lambda_data[2]=recieve_phase3.data
        arr_lambda_data[3]=recieve_phase4.data
        tagxyz_obj = LM.Levenberg_Marquarelt(arr_lambda_data)
        tagxyz = tagxyz_obj.LM_main()
        tagxyz_list=[0,0,0]
        for i in range(0,3):
            tagxyz_list[i]=(tagxyz.A)[i][0]
        #file.writelines(tagxyz_list[0],',',tagxyz_list[1],',',tagxyz_list[2],'\n')
        print(tagxyz_list)
        tagxyz_pub_info = Float32MultiArray(data=tagxyz_list)
        pub.publish(tagxyz_pub_info)

if __name__ == '__main__':
    # file=open('data/xyz_data','a')
    myclass=listener(file)
    rospy.spin()
    file.close()
