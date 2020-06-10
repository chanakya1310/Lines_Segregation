import cv2
import numpy as np
import cv2
from matplotlib import pyplot as plt
from api import *
import json

inputFile="Enter your image here"
outputFile=inputFile.split(".")[0]+"_1Output.jpeg"

img=cv2.imread(inputFile,1)
img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
a=img.shape
print("Image Info:",a)
height=a[0]#763
width=a[1]#969
print("Height (Vert) x Width (Horiz) = "+str(height)+" x "+str(width))


#These rows have data, ie atleast 1 pixel does not match background color
dataRows=[]

# Start from 1,1 since we used 0,0 for background
for i in range(0,height):
    dataInRow=False
    backgroundPixel=img[i,0]
    #if i< 3: print("")
    for j in range(1,width):
        pixelToCheck=img[i,j]
        if np.array_equal(pixelToCheck,backgroundPixel):
            dataInRow=False
            
        else:
            if (abs(int(pixelToCheck[0])-int(backgroundPixel[0]))>100) or (abs(int(pixelToCheck[1])-int(backgroundPixel[1]))>100) or (abs(int(pixelToCheck[2])-int(backgroundPixel[2]))>100):
                print("Data Found",i,pixelToCheck,backgroundPixel)
                #time.sleep(1)
                dataInRow=True
                break            
    if(dataInRow):
        dataRows.append(i)
        
#print(dataRows)

#Get Line markers by removing continuous values & leave the jumps

markerRows=[]
#markerRows.append(int(dataRows[0]))
for row in range(1,len(dataRows)):
    if int(dataRows[row])==(int(dataRows[row-1])+1):
        if (row-1)==0:
            markerRows.append(dataRows[row-1])
        continue
    else: 
        markerRows.append(dataRows[row-1])
        markerRows.append(dataRows[row])

#Unique Values
#print(markerRows)      
markerRows=set(markerRows)
markerRows=sorted(list(markerRows))
print(markerRows)
print(len(markerRows))
m=[]
for i in range(0,len(markerRows)-1,1):
    if abs(markerRows[i]-markerRows[i+1])>=40:
        m.append(markerRows[i])
#print(m)

for breakPoint in markerRows:
    #print("Processing breakPoint", breakPoint)
    cv2.rectangle(img,(0,int(breakPoint)),(int(width),int(breakPoint)),(0,255,0),1)

plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
cv2.imwrite(outputFile,img) #Save the outputs to a file
