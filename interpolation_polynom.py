# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:51:06 2020

@author: josef
"""
from scipy import interpolate
from numpy import polynomial as P
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
x = np.array([1,2,3,4])
y = np.array([1,3,5,4])
deg = len(x) -1
A = P.polynomial.polyvander(x, deg)
c = linalg.solve(A,y)
f1 = P.Polynomial(c)


xx = np.linspace(0,10,10)
fig, ax = plt.subplots(1,1,figsize = (12,4) )
ax.plot(xx,f1(xx),'b')
ax.scatter(x,y,label = 'data points')
