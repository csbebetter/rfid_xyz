#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from numpy import matrix as mat
import math

class Levenberg_Marquarelt:
    # 导入数据
    #antenna_xyz_data = [[-0.605  , 0.64      , 0.13],[0.785 , 0.64      , 0.13],[0.155   , 0  , 0.121],[-0.155 , 0  , 0.121]]
    label_location = [0.35,1.82,0.435]
    theta_data = [0,0,0,0]
    lambda_data = [0.3125,0.3125,0.3125,0.3125]
    xi_data=[0.785,-0.605,0.155,-0.155]
    yi_data=[0.64,0.64,0,0]
    zi_data=[0.13,0.13,0.121,0.121]


    # 合并为一个矩阵，然后转置,每一行为一组λ，xi, yi,zi。
    Variable_Matrix = mat([lambda_data, xi_data, yi_data, zi_data]).T

    # 算法相关数据
    n = len(theta_data)
    J = mat(np.zeros((n, 3)))  # 雅克比矩阵
    fx = mat(np.zeros((n, 1)))  # f(x)  3*1  误差
    fx_tmp = mat(np.zeros((n, 1)))
    initialization_parameters = mat([[10], [400], [30]])  # 参数初始化
    lase_mse = 0.0
    step = 0.0
    u, v = 1.0, 2.0
    conve = 100

    def __init__(self,theta_data_input):
        self.theta_data = theta_data_input

    def Func(self, parameter, iput):  # 需要拟合的函数，abc是包含三个参数的一个矩阵[[a],[b],[c]]
        x = parameter[0,0]
        y = parameter[1,0]
        z = parameter[2,0]
        residual = mat((4*np.pi / iput[0, 0])*np.sqrt(np.square(iput[0, 1]-x)+np.square(iput[0, 2]-y)+np.square(iput[0, 3]-z)))
        return residual


    def Deriv(self, parameter, iput):  # 对函数求偏导
        x = parameter[0,0]
        y = parameter[1,0]
        z = parameter[2,0]
        x_deriv = -4*np.pi*(iput[0, 1]-x) / (iput[0, 0] * np.sqrt(np.square(iput[0, 1]-x)+np.square(iput[0, 2]-y) + np.square(iput[0, 3]-z)))
        y_deriv = -4*np.pi*(iput[0, 2]-y) / (iput[0, 0] * np.sqrt(np.square(iput[0, 1]-x)+np.square(iput[0, 2]-y) + np.square(iput[0, 3]-z)))
        z_deriv = -4*np.pi*(iput[0, 3]-z) / (iput[0, 0] * np.sqrt(np.square(iput[0, 1]-x)+np.square(iput[0, 2]-y) + np.square(iput[0, 3]-z)))
        deriv_matrix = mat([x_deriv, y_deriv, z_deriv])
        return deriv_matrix

    def LM_main(self):
        while self.conve:
            mse, mse_tmp = 0.0, 0.0
            self.step += 1
            for i in range(len(self.theta_data)):
                self.fx[i] = self.Func(self.initialization_parameters, self.Variable_Matrix[i]) - self.theta_data[i]  # 注意不能写成  y - Func  ,否则发散
                # print(fx[i])
                mse += self.fx[i, 0] ** 2
                self.J[i] = self.Deriv(self.initialization_parameters, self.Variable_Matrix[i])  # 数值求导
            mse = mse/self.n  # 范围约束
            H = self.J.T * self.J + self.u * np.eye(3)  # 3*3
            dx = -H.I * self.J.T * self.fx  # 注意这里有一个负号，和fx = Func - y的符号要对应

            self.initial_parameters_tmp = self.initialization_parameters.copy()
            self.initial_parameters_tmp = self.initial_parameters_tmp + dx
            for j in range(len(self.theta_data)):
                self.fx_tmp[j] = self.Func(self.initial_parameters_tmp, self.Variable_Matrix[j]) - self.theta_data[j]
                mse_tmp += self.fx_tmp[j, 0] ** 2
            mse_tmp = mse_tmp/self.n

            q = (mse - mse_tmp) / ((0.5 * dx.T * (self.u * dx - self.J.T * self.fx))[0, 0])
            #print(q)
            if q > 0:
                s = 1.0 / 3.0
                v = 2
                mse = mse_tmp
                self.initialization_parameters = self.initial_parameters_tmp
                temp = 1 - pow(2 * q - 1, 3)
                if s > temp:
                    self.u = self.u * s
                else:
                    self.u = self.u * temp
            else:
                self.u = self.u * self.v
                self.v = 2 * self.v
                mse = mse_tmp
                self.initialization_parameters = self.initial_parameters_tmp
            #print("step = %d,parameters(mse-lase_mse) = " % self.step, abs(mse - self.lase_mse))
            if abs(mse - self.lase_mse) < math.pow(0.1, 15):
                break
            self.lase_mse = mse  # 记录上一个 mse 的位置
            self.conve -= 1
        #print(self.lase_mse)
        #print(self.initialization_parameters)
        return self.initialization_parameters
