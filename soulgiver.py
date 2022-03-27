from graverobber import SoulGiver
import imageio
import matplotlib.pyplot as plt
from threading import Thread
import time
graverobber = SoulGiver()
graverobber.AddPath("../../Monk/png")
graverobber.pngSearch()
graverobber.pngReframe()

#output name
filename_out = 'test.png'

for idx in range(len(graverobber.snapshots)):
	print()
	print(graverobber.paths[idx])
	print(graverobber.snapshots[idx])
graverobber.GeneratePoster()
imageio.imwrite(filename_out, graverobber.poster)


import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '768')
Config.set('graphics', 'height', '564')
Config.set('graphics', 'resizable', False)
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.lang.parser import global_idmap   
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.effects.scroll import ScrollEffect 


class Animator(Widget):
    pass




class Row(BoxLayout):
	dr  = StringProperty('')
	idx = StringProperty('')

	def __init__(self, dr, idx , **kwargs):

		super(Row, self).__init__(**kwargs)
		self.idx = idx
		self.dr = dr

	def remove_row(self):
		self.remove_widget(Row)


class MyApp(App):
	myanim = None
	loggg = None
	size = [768,564]
	mine = None
	
	diridx = 0
	imgidx = 0
	
	imgname = ""
	currentdir = ""
	currentimg = ""
	currentframe = -1
	workonframe=-1
	workonframestr= 'N'
	drwf = 'N'
	
	FrameInput = None
	myt = None
	lplay = False
	
	
	images= []
	duration =[]
	index =[]	
	infoboxes=[]
	infolayout=[]
	coords = []
	
	
	animmode= False

	
	def NextDir(self,i):
		if(self.lplay):
			self.Stop()
		if(self.animmode): 
			self.SwitchMode()
		self.diridx = self.diridx+i
		if(self.diridx >= len(self.mine.snapshots)):
			self.diridx = 0 
		if(self.diridx < 0):
			self.diridx = len(self.mine.snapshots)-1		
		self.imgidx = 0 
		self.currentdir=  self.mine.paths[self.diridx]
		self.currentimg = self.mine.paths[self.diridx]+"/"+self.mine.snapshots[self.diridx][self.imgidx]
		self.imgname= self.mine.snapshots[self.diridx][self.imgidx]
		
		self.myanim.labeltextimg.text = self.imgname
		self.myanim.labeltextdir.text = self.currentdir
		self.myanim.labelimgsource.source = self.currentimg
	
	
	def NextImg(self, i):
		if(self.animmode):
			#if(self.lplay):
			#	if(len(self.images) > 0):
			#		self.workonframe+=i
			#		if(self.workonframe >= len(self.images)):
			#			self.workonframe = 0 
			#		if(self.workonframe < 0):
			#			self.workonframe = len(self.images)-1 
					
					#self.myanim.labeldurationlabel.text = self.drwf
					#self.myanim.labelworkframelabel.source = self.images[self.currentframe]
			#else:		
			if(len(self.images) > 0):
				self.currentframe+=i
				if(self.currentframe >= len(self.images)):
					self.currentframe = 0 
				if(self.currentframe < 0):
					self.currentframe = len(self.images)-1 
				
				self.myanim.labeltextimg.text = str(self.currentframe)
				self.myanim.labelimgsource.source = self.images[self.currentframe]
			else:
				self.SwitchMode(-1)
		else :
			self.imgidx = self.imgidx+i
			if(self.imgidx >= len(self.mine.snapshots[self.diridx])):
				self.imgidx = 0 
			if(self.imgidx < 0):
				self.imgidx = len(self.mine.snapshots[self.diridx])-1 
			self.currentimg = self.mine.paths[self.diridx]+"/"+self.mine.snapshots[self.diridx][self.imgidx]
			self.imgname= self.mine.snapshots[self.diridx][self.imgidx]
			
			self.myanim.labeltextimg.text = self.imgname
			self.myanim.labelimgsource.source = self.currentimg
		
		
	def SetSearch(self,graverobber):
		self.mine = graverobber
		print(len(self.mine.paths), len(self.mine.snapshots[0]))
		self.currentdir = self.mine.paths[0]
		self.currentimg = self.mine.paths[0]+"/"+self.mine.snapshots[0][0]
		self.imgname= self.mine.snapshots[self.diridx][self.imgidx]
		
	def build(self):

		
		self.loggg =  ScrollView(size_hint=(1, None), size=(100, 250))
		self.myanim = Animator()
		return self.myanim
	
	def SwitchMode(self, i):
		if(i>0):
			print("press anim")
		else :
			print("press navig")
		if(self.lplay):
			self.StopAnim()
			self.myt.join()
		if not self.animmode and i > 0 :
			self.animmode=True
			self.myanim.animbtnlabel.background_color = 'red'
			self.myanim.navigbtnlabel.background_color = 'grey'
			print("to anim")
			self.NextImg(0)
			
		elif (self.animmode and i < 0 ):
			self.animmode=False
			self.myanim.navigbtnlabel.background_color = 'red'
			self.myanim.animbtnlabel.background_color = 'grey'
			print("to navig")
			self.NextImg(0)
		
		
	def AddImg(self):
		
		if(self.lplay):
			self.Stop()
		if(self.animmode): 
			self.SwitchMode()
		else :
			self.images.append(self.mine.paths[self.diridx]+"/"+self.mine.snapshots[self.diridx][self.imgidx])
			self.coords.append(self.mine.coords[self.diridx][self.imgidx])
			self.workonframe=0
			self.duration.append(5)	
			self.AddRecap()
			self.NextImg(1)
		
	def RemoveImg(self):
		if(len(images) > 0):
			self.images.pop(currentframe)
			self.duration.pop(currentframe)	
	
	def PlayAnim(self):
		if(not self.animmode):
			self.SwitchMode(1)
		if (not self.lplay):
			self.lplay=True
			self.myt = Thread(target=self.Movie, args=())
			self.myt.start()
		
	def StopAnim(self):
		self.lplay= False
	def Movie(self):
		while(True):
			time.sleep(self.duration[self.currentframe]/1000)
			self.NextImg(+1)
			if(not self.lplay):
				break
	def Reset(self):
		self.images= []
		self.duration =[]
		self.index =[]	
		self.infoboxes=[]
		self.coords = []
		for i in self.infolayout: 
			self.myanim.animinfolabel.remove_widget(i)
		self.infolayout=[]
		self.SwitchMode( 1)
		
	
	def on_stop(self):
		self.StopAnim()
		self.myt.join()
		return True
	
	def ChangeDuration(self, idx, dr) :
		self.duration[int(idx)-1]=int(dr) 
		print(idx, dr)
	
		
	def ChangeWorkFrame(self):
		self.workonframe = int(self.myanim.workframelabel.text) 
		
		self.myanim.durationlabel.text = str(self.duration[self.workonframe])
		selfdrwf = int(self.myanim.durationlabel.text) 
		
		print(self.drwf,self.workonframe )
		
	def MoveFrame(self,i):
		if self.currentframe+i == len(self.images):
			i = -self.currentframe
		if self.currentframe+i == -1:
			i = len(self.images) - 1 - self.currentframe
	
		a = self.images[self.currentframe]
		b = self.duration[self.currentframe]
		self.images[self.currentframe]		= self.images[self.currentframe+i]
		self.duration[self.currentframe] 	= self.duration[self.currentframe+i]
		self.duration[self.currentframe+i]	= b
		self.images[self.currentframe+i] 	= a
		self.currentframe = self.currentframe +i
		self.NextImg(0)
		
	def AddRecap(self):
		#self.infoboxes.append(TextInput(text=str(self.duration[-1]) )) 
		self.infolayout.append( Row(idx = str(len(self.images)) , dr = str(self.duration[-1]) ) )
		self.myanim.animinfolabel.add_widget(self.infolayout[-1])
		
		
	def DumpAnim(self):
		with open("monk.anim",'w+') as f:
			f.write('# Anim  01 \n') 
			f.write('#info' )
			f.write('\n')
			f.write(filename_out) 
			f.write('\n')
			f.write(str(self.mine.maxshape[0])+ '     ' + str(self.mine.maxshape[1]) )
			f.write('\n') 
			f.write('#data')
			f.write('\n')
			for i in range(len(self.images)): 
				f.write(self.images[i] )
				f.write('     ') 
				f.write(str(self.coords[i][0]))
				f.write('     ') 
				f.write(str(self.coords[i][1]))
				f.write('     ') 
				f.write(str(self.duration[i]))
				f.write('\n') 
		
	
	#def RemoveRecap(self):
		

if __name__ == '__main__':
	test = MyApp()
	test.SetSearch(graverobber)
	test.run()

#soulgiver
