import os
import imageio
import numpy as np 
import shutil
class SoulGiver:
	
	snapshots = []
	paths = []
	recursive = []
	maxshape = [0,0,0]
	poster= None
	minlims = [0,0]
	coords = []
	
	def __init__(self):
		pass
		
	#def __init__(self,path_,rgraverobberecursive_ = True ):
	#	if os.path.isdir(path_):
	#		self.paths.append(path_)
	#		self.recursive.append(recursive_)
	#	else:
	#		print("Error: Invalid path") 

	def pngSearch(self, lresize=True):
		for directory, rec in zip(self.paths, self.recursive):
			if rec:
				files=sorted(os.listdir(directory))
				msk = [os.path.isdir(directory+'/'+f) for f in files]
				subdirectories = [f for f, m in zip(files, msk) if m]
				for sd in subdirectories:
					self.paths.append(directory+'/'+sd)
					self.recursive.append(True)
		
		
		for directory in self.paths:
			files=sorted(os.listdir(directory))
			msk = [f[-4:] == '.png' for f in files]
			snapshots_ = sorted([f for f, m in zip(files, msk) if m])
			self.snapshots.append(snapshots_)
			for s in snapshots_:
				image = imageio.imread(directory + '/' + s)
				dim = image.shape
				for i in range(3):
					if dim[i]>=self.maxshape[i]:
						self.maxshape[i] = dim[i]
						
				
						
										 
							
		idx = 0			
		while(True):
			if(len(self.snapshots[idx]) == 0):
				self.snapshots.pop(idx)
				self.paths.pop(idx)
				self.recursive.pop(idx)
				print(len(self.paths), idx)
			else:
				idx= idx+1
				if(idx >= len(self.paths)):
					break
				
			     
	def pngReframe(self):	
		minmaxx = [self.maxshape[1],0]
		minmaxy =[self.maxshape[0],0]
		
		for i,directory in zip(range(len(self.paths)), self.paths):
			for snapshot in self.snapshots[i]:
				image = imageio.imread(directory + '/' + snapshot)
				last = 0 
				delta = 0 
				ylims = [0,0]
				xlims = [0,0]
				for x in range(image.shape[1]):
					if(max(image[:,x,self.maxshape[2]-1]) > 0.01 ):	
						xlims[0] = x
						minmaxx[0] = min(xlims[0], minmaxx[0])		
						break
				for x in range(image.shape[1]-1,-1,-1):
					if(max(image[:,x,self.maxshape[2]-1]) > 0.01 ):	
						xlims[1] = x
						minmaxx[1] = max(xlims[1], minmaxx[1])
						break
				for y in range(image.shape[0]):
					if(max(image[y,:,self.maxshape[2]-1]) > 0.01 ):	
						ylims[0] = y		
						minmaxy[0] = min(ylims[0], minmaxy[0])
						break
				for y in range(image.shape[0]-1,-1,-1):
					if(max(image[y,:,self.maxshape[2]-1]) > 0.01 ):	
						ylims[1] = y
						
						minmaxy[1] = max(ylims[1], minmaxy[1])	
						break
		
			
			
		self.minlims = [minmaxy[0],minmaxx[0]]
		self.maxshape[0]= minmaxy[1]-minmaxy[0]
		self.maxshape[1]= minmaxx[1]-minmaxx[0]
		
		newgraveyard = "/home/edoardo/Desktop/graverobberdir"
		if os.path.exists(newgraveyard):
		    shutil.rmtree(newgraveyard)
		os.makedirs(newgraveyard)

		for i,directory in zip(range(len(self.paths)), self.paths):
			for snapshot in self.snapshots[i]:
				image = imageio.imread(directory + '/' + snapshot)
				imageio.imwrite(newgraveyard + '/' 
					+snapshot[:-4] + 'A.png', image[minmaxy[0]:minmaxy[1],minmaxx[0]:minmaxx[1]])	
		
		self.paths = [newgraveyard]
		self.recursive = [False]
		self.snapshots=[sorted(os.listdir(newgraveyard))]
		print(len(self.snapshots))
		print(self.snapshots)
								      	
	def AddPath(self,path_,recursive_ = True ):
		if os.path.isdir(path_):
			self.paths.append(path_)
			self.recursive.append(recursive_)
		else:
			print("Error: Invalid path") 	
	
	def GeneratePoster(self):
		Nimg=sum([len(l) for l in self.snapshots])
		side = int(np.ceil(np.sqrt(float(Nimg))))
		self.poster=np.zeros((side*self.maxshape[0],side*self.maxshape[1], self.maxshape[2]))
		cnt = 0
		print()
		print(self.maxshape, self.minlims, side)
		for folder, imfile in zip(self.paths,self.snapshots):
			self.coords.append([])
			for snap in imfile:
				image = imageio.imread(folder + '/' + snap)
				print(folder + '/' + snap, image.shape)
				i = cnt // side
				j = cnt % side		
				self.poster[i*self.maxshape[0]:(i+1)*self.maxshape[0],
					    j*self.maxshape[1]:(j+1)*self.maxshape[1], :] = image/255.0
				self.coords[-1].append([i,j])
				cnt+=1
	 
	 	 
	 				

	
