import imageio
from matplotlib import pyplot as plt
import os 
from matplotlib.animation import FuncAnimation
import numpy as np

path_ = 'Monk/png/'
dirs = os.listdir(path_)
print(dirs)
sizex = 0
sizey = len(dirs)

theshape = (0,0,0)

for dir1 in dirs:
    dirs2 = (os.listdir(path_+dir1))
    if(len(dirs2) > sizex ):
        sizex = len(dirs2)
    for f in dirs2:
        im = imageio.imread(path_+dir1+'/'+f)
        theshape = im.shape

           
full =  np.zeros((sizey*theshape[0],sizex*theshape[1],theshape[2]))
print(full.shape)
print(theshape)
for i in range(len(dirs)):
    dirs2 = sorted(os.listdir(path_+dirs[i]))
    if(len(dirs2) > sizex ):
        sizex = len(dirs2)
    for j in range(len(dirs2)):
        print(path_+dirs[i]+'/'+dirs2[j])
        im = imageio.imread(path_+dirs[i]+'/'+dirs2[j])
        plt.imshow(im)
        #print(im.shape, i*theshape[0],(i+1)*theshape[0],j*theshape[1],(j+1)*theshape[1] )
        full[i*theshape[0]:(i+1)*theshape[0],j*theshape[1]:(j+1)*theshape[1],:] =  np.array(im, int)

print(np.max(full))
    #for f in files:
    #        im = imageio.imread(path_+dir1+'/'+dir2+'/'+f)
    #        print(im.shape)
    

