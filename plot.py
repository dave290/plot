#plot.py
#plots multiple scans from .kel files
#Example of 2D plot
#python plot.py -T 2 -L -200 -H +200 -C 4
#Example of 3D plot
#python plot.py -T 3 -L -200 -H +200 -C 4

import argparse
parser = argparse.ArgumentParser(description='A test program.')
parser.add_argument("-T", "--plot_type", help="Enter 2 or 3 for plot dimension", type=int)
parser.add_argument("-L", "--lowest_vel", help="Enter lowest velocity in km/s", type=int)
parser.add_argument("-H", "--highest_vel", help="Enter highest velocity in km/s", type=int)
parser.add_argument("-C", "--count_every", help="Count every c files", type=int)
args = parser.parse_args()
flag=args.plot_type
lowerfitthreshold=args.lowest_vel*1000
upperfitthreshold=args.highest_vel*1000
countevery=args.count_every

import os
import collections
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
fig=plt.figure(figsize=(12,6))

if flag==2:
    ax=plt.axes()
    ax.set_title("Intensity vs Velocity")
    ax.set_xlabel("Velocity (m/s)")
    ax.set_ylabel("Intensity (K)")

if flag==3:
    ax=plt.axes(projection='3d')
    ax.set_title("Intensity vs Velocity")
    ax.set_xlabel("File Number")
    ax.set_ylabel("Velocity (m/s)")
    ax.set_zlabel("Intensity (K)")

#read filenames and sort by prefix
os.chdir('Data')
filelist=os.listdir(".")
filelist.sort()

#Initialize variables
GALLON=[0];GALLAT=[0];velocity=[0];intensity=[0]
colon=[999];correction=0

#determine start and end lines for reading data
datafile=filelist[0]
with open(datafile, 'r') as f:  
    linesofdata=[0]
    line_no=0
    for line in f:
        line_no=line_no+1
        linestring=line.split()
        if linestring[0]=="#":
            pass
        else:
            vel=float(linestring[1])
            if vel>=lowerfitthreshold and vel<=upperfitthreshold:
                linesofdata.append(line_no)
f.closed
True
startline=int(linesofdata[1])
endline=int(linesofdata[-1])

#read file info
filenumber=0
for i in filelist:
    filenumber=filenumber+1
    GALLON=[0];GALLAT=[0];velocity=[0];intensity=[0]
    with open(i,'r') as f:
        N=0
        for line in f:
            N=N+1
            linestring=line.split()
            if linestring[1]=="GALLON":
                coordinate=linestring[3]
                for j in range(8):
                    if coordinate[j]==":":
                        colon.append(j)
                degrees=float(coordinate[0:colon[1]])
                minutes=float(coordinate[colon[1]+1:colon[2]])
                seconds=float(coordinate[colon[2]+1:])
                degrees=degrees+minutes/60.0+seconds/3600.0
                gallon=float(round(degrees,2))
                colon=[999]
            if linestring[1]=="GALLAT":
                coordinate=linestring[3]
                if coordinate[0]=="-":
                    multiplier=-1.0
                if coordinate[0]=="+":
                    multiplier=+1.0
                for j in range(8):
                    if coordinate[j]==":":
                        colon.append(j)
                degrees=float(coordinate[1:colon[1]])
                minutes=float(coordinate[colon[1]+1:colon[2]])
                seconds=float(coordinate[colon[2]+1:])
                degrees=multiplier*(degrees+minutes/60.0+seconds/3600.0)
                gallat=float(round(degrees,2))
                colon=[999]
            if N>=startline and N<=endline:
                GALLON.append(gallon)
                GALLAT.append(gallat)
                linestring=line.split()      
                x=float(linestring[1])
                velocity.append(x)
                y=float(linestring[2])
                intensity.append(y)
    f.closed
    True
    GALLON[0]=GALLON[1];GALLAT[0]=GALLAT[1]
    velocity[0]=velocity[1];intensity[0]=intensity[1]
    temp=filenumber-correction
    if temp==countevery:
        correction=filenumber
        print(i)
        print("GALLON")
        print(GALLON[0])
        print("GALLAT")
        print(GALLAT[0])
        print(" ")
        if flag==2:
            ax.scatter(velocity,intensity,marker=".",label=("GLONG,GLAT= "+str(GALLON[0])+"  "+str(GALLAT[0])))
            ax.legend(loc="best")
        if flag==3:
            ax.scatter(filenumber, velocity, intensity, marker=".")
        else:
            continue

plt.show()
exit()
