from PIL import Image
import sys
import os
import math
img = Image.open(os.path.join(sys.path[0], "norway.png"))  # choose which image to look at
slc=125 # which elevation to slice at - based on brightness
thresh=1 # tolerance for the slice
times=20
dictlist = []
w, h = img.size
scale=1.1
scalespace = range(35, 45)
for k in scalespace:
    dictlist.append({})
for i in range(w):
    for j in range(h):
        val = img.getpixel((i,j))[0]
        if val > slc-thresh and val < slc+thresh:
            img.putpixel((i,j), (155, 155, 155))
            for k in scalespace:
                dictlist[k-scalespace[0]][(int(i/scale**k), int(j/scale**k))] = True
        else:
            img.putpixel((i,j), (0, 0, 0))
        #img.putpixel((i,j), min(1,round(val/125))*155)
        #print(val, round(val/155)*155)

sumprod = 0
sumx = 0
sumy = 0
sumx2 = 0
sumy2 = 0
for k in scalespace:
    amount = 0
    for i in dictlist[k-scalespace[0]]:
        amount += 1
    sumx += k
    sumy += math.log(amount, scale)
    sumx2 += k**2
    sumy2 += math.log(amount, scale)**2
    sumprod += k*math.log(amount, scale)

slope = (len(scalespace)*sumprod-sumx*sumy)/(len(scalespace)*sumx2-sumx**2)
r = (len(scalespace)*sumprod-sumx*sumy)/((len(scalespace)*sumx2-sumx**2)*(len(scalespace)*sumy2-sumy**2))**0.5
print(-slope)
    

img.save(os.path.join(sys.path[0], "processed.png"))



