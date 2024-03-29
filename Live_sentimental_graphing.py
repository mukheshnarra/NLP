# -*- coding: utf-8 -*-
"""
Created on Thu May 30 23:44:42 2019

@author: MUKHESH
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time

style.use('ggplot')

fig=plt.figure()
ax1=fig.add_subplot(1,1,1)

def animate(i):
    pull_data=open('tweet.txt','r').read()
    lines=pull_data.split('\n')
    xar=[]
    yar=[]
    x=0
    y=0
    for l in lines[-200:]:
        x+=1
        if 'pos' in l:
            y+=1
        elif 'neg' in l:
            y-=0.3
        xar.append(x)
        yar.append(y)
    ax1.clear()
    ax1.plot(xar,yar)
ani=animation.FuncAnimation(fig,animate,interval=1000)    
plt.show()