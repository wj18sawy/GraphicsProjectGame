from diamondSquare import *
import viz
import vizshape
import math

# Author: R. Flatland
# Controls the generation, display, and navigation of a terrain.

class TerrainController(viz.EventClass):
	
	def __init__(self):
		viz.EventClass.__init__(self)
			
		self.callback(viz.KEYDOWN_EVENT,self.onKeyDown)
		self.callback(viz.TIMER_EVENT,self.onTimer)
				
		#turn on lighting
		
				
		# generate random terrain using diamond-square algorithm
		self.terrainData = diamondSquare(8)
				
		# add some craters to the terrain
		self.makeCrater( self.terrainData, 0, 0, 80)
		self.makeCrater( self.terrainData, 0, len(self.terrainData)/4.5, 40)
		self.makeCrater( self.terrainData, 0, len(self.terrainData), 100)
		self.makeCrater( self.terrainData, len(self.terrainData)/4, len(self.terrainData)+20, 60)
		self.makeCrater( self.terrainData, (len(self.terrainData)*3)/4, len(self.terrainData)+20, 60)
		self.makeCrater( self.terrainData, -20, len(self.terrainData)/2, 40)
		self.makeCrater( self.terrainData, len(self.terrainData)/2, 0, 40)
		self.makeCrater( self.terrainData, len(self.terrainData)/2, len(self.terrainData)/8, 40)

#		self.makeHill(self.terrainData, 5, len(self.terrainData)/2, len(self.terrainData)/2, 25,40)
				
		# create a triangular mesh (a Vizard layer of triangles) out of the data
		terrainLayer = self.generateLayer(self.terrainData)
		terrainLayer.enable(viz.LIGHTING)
		viz.MainView.getHeadLight().disable()
		self.newLight = viz.addLight()
		self.newLight.enable()
		self.newLight.color(1,1,1)
		
		m = viz.Matrix()
		m.postAxisAngle(1,0,0,45)
		self.newLight.setMatrix(m)
		
		# viewer is located at (self.x,self.y,self.z)
		
		
		self.rotate = 0
		self.height = 0
		self.xVal = 0
		self.zVal = 0
		# initializing this starting view 
		view = viz.MainView
		m = viz.Matrix()
		m.postAxisAngle( 0,1,0, self.rotate) 
		m.postTrans(self.xVal,self.height,self.zVal)  
		view.setMatrix(m)
		
		
		
		#Put monsters 
		self.zombie = viz.add('licker.dae')
		self.zombX = len(self.terrainData)-15
		self.zombZ = len(self.terrainData)-20
		m = viz.Matrix()
		m.postTrans(0,0,0)
		m.postAxisAngle(1,0,0,90)
		m.postScale(10,10,10)
		m.postTrans(self.zombX,self.terrainData[self.zombX][self.zombZ],self.zombZ)
		self.zombie.setMatrix(m)
		
		self.zombie2 = viz.add('licker.dae')
		self.zombX2 = len(self.terrainData)/2
		self.zombZ2 = len(self.terrainData)-20
		m = viz.Matrix()
		m.postTrans(0,0,0)
		m.postAxisAngle(1,0,0,90)
		m.postScale(10,10,10)
		m.postTrans(self.zombX2,self.terrainData[self.zombX2][self.zombZ2],self.zombZ2)
		self.zombie2.setMatrix(m)
	
	# Input: a 2D square array containing elevation data 
	# Returns: a Vizard layer which is a triangular mesh 
	# representing the surface of the terrain 
	def generateLayer( self, terrainData ):
		viz.startLayer(viz.TRIANGLES)
		for r in range(0, len(terrainData)-1):
			for c in range(0, len(terrainData)-1):
				# each array location generates two triangles
				
				viz.vertexColor( 0.545,.2,0.074)
				# corners of first triangle, in ccw order when looking down on the surface
				c1 = [c, terrainData[r][c], r]
				c2 = [c+1, terrainData[r+1][c+1], r+1]
				c3 = [c, terrainData[r+1][c], r+1]
			
				viz.normal(self.normal(c1,c2,c3))
				viz.vertex(c1)
				viz.vertex(c2)
				viz.vertex(c3)
				
				viz.vertexColor( 0.545,.2,0.074)
				# corners of second triangle, in ccw order when looking down on the surface
				c1 = [c, terrainData[r][c], r]
				c2 = [c+1, terrainData[r][c+1], r]
				c3 = [c+1, terrainData[r+1][c+1], r+1]
				
				viz.normal(self.normal(c1,c2,c3))
				viz.vertex(c1)
				viz.vertex(c2)
				viz.vertex(c3)
				
		return viz.endLayer()
		

	def onKeyDown(self,key):
		
		if key == viz.KEY_LEFT:
			#spin
			self.rotate -= 2
		elif key == viz.KEY_RIGHT:
			self.rotate += 2
		elif key == viz.KEY_UP: #move forward
			self.xVal += 2* (math.sin(math.radians(self.rotate)))
			self.zVal += 2* (math.cos(math.radians(self.rotate)))
		elif key == viz.KEY_DOWN: #move backward
			temp = 0 
			if(self.rotate <= 180):
				temp = self.rotate+180
			else:
				temp = self.rotate-180
				
			self.xVal += 2*(math.sin(math.radians(temp)))
			self.zVal += 2*(math.cos(math.radians(temp)))
		elif key == "a":
			
			
			self.starttimer(1,.05,viz.PERPETUAL)

			
		
			
		self.height = self.findHeight(self.terrainData,self.zVal,self.xVal) #weirdly have to switch x and z for it to work
		#sets the changed view			
		view = viz.MainView
		m = viz.Matrix()
		m.postAxisAngle( 0,1,0, self.rotate) 
		m.postTrans(self.xVal,self.height+5,self.zVal)  
		view.setMatrix(m)
		
		
		
		
		
	def onTimer(self,num):
		
		if num == 1:
			
			self.zombZ -= 2
			
			zombHeight = self.findHeight(self.terrainData,self.zombZ,self.zombX) #weirdly have to switch x and z for it to work
			
			m = viz.Matrix()
			m.postTrans(0,0,0)
			m.postAxisAngle(1,0,0,90)
			m.postScale(10,10,10)
			m.postTrans(self.zombX,zombHeight,self.zombZ)  
			self.zombie.setMatrix(m)
			
			self.zombZ2 -= 2
			
			zombHeight2 = self.findHeight(self.terrainData,self.zombZ2,self.zombX2) #weirdly have to switch x and z for it to work
			
			m = viz.Matrix()
			m.postTrans(0,0,0)
			m.postAxisAngle(1,0,0,90)
			m.postScale(10,10,10)
			m.postTrans(self.zombX2,zombHeight2,self.zombZ2)  
			self.zombie2.setMatrix(m)
			
			
			
	#Input the elevation array, size of hill(1-5), center point, width, length 
	def makeHill(self, array, size, x, z, width, length ):
		
		
		for r in range(0, len(array)):
			for c in range(0, len(array)):
				
				if (abs(r-x) <= width and abs(c-z) <= length):
					dist = math.sqrt(math.pow(abs(r-x),2)+math.pow(abs(c-z),2))
					max = math.sqrt(math.pow(width,2)+math.pow(length,2))
					
					if(dist != 0):						
						array[r][c] += array[r][c] * (.1*(size/(dist/2)))
					else:
						
						array[r][c] += array[r][c] * (.1*(size))
	
	def makeCrater(self, data, cr, cc, radius):
		for r in range(0, len(data)):
			for c in range(0, len(data)):
				dist = math.sqrt((r - cr)*(r - cr) + (c - cc)*(c - cc))
				if (dist < (radius)):
					y = math.sqrt( radius*radius - dist*dist )
					data[r][c] += y/15.0

					
					
				
		
	def normal(self,c1,c2,c3):
		
		a = [c3[0]-c1[0], c3[1]-c1[1], c3[2] - c1[2]] 
		b = [c2[0]-c1[0], c2[1]-c1[1], c2[2] - c1[2]] 
		
		x = (a[1]*b[2])-(a[2]*b[1])
		y = -((a[0]*b[2])-(a[2]*b[0]))
		z = (a[0]*b[1])-(a[1]*b[0])
		
		n = [x,y,z]
		
		return n
		
	def findHeight(self,array,x,z):
		
		c1 = 0
		c2 = 0 
		c3 = 0
		
		norm = [0,0,0]
		
		rx = int(round(x, 0))
		rz = int(round(z, 0))
		
		p = [0,0,0]
		
		
		if (x>z): #Bottom triangle
			
			if (rx > x):
				
				if (rz > z):
					
					c1 = [rx-1, array[rx-1][rz-1], rz-1]
					c2 = [rx, array[rx][rz-1], rz-1]
					c3 = [rx, array[rx][rz], rz]
					
					p = c2
					
				else:
					
					c1 = [rx-1, array[rx-1][rz], rz]
					c2 = [rx, array[rx][rz], rz-1]
					c3 = [rx, array[rx-1][rz], rz+1]
					
					p = c3
				
			else:
				
				c1 = [rx, array[rx][rz], rz]
				c2 = [rx+1, array[rx+1][rz], rz]
				c3 = [rx+1, array[rx+1][rz+1], rz+1]
					
				p = c2
					
		else: #top triangle
			
			if (rx > x):
				
				c1 = [rx-1, array[rx-1][rz-1], rz-1]
				c2 = [rx, array[rx][rz], rz]
				c3 = [rx-1, array[rx-1][rz], rz]
					
				p = c2
			
		
			else:
				
				if (rz > z):
					
					c1 = [rx, array[rx][rz-1], rz-1]
					c2 = [rx+1, array[rx+1][rz], rz]
					c3 = [rx, array[rx][rz], rz]
					
					p = c2
					
				else:
					
					c1 = [rx, array[rx][rz], rz]
					c2 = [rx+1, array[rx+1][rz+1], rz+1]
					c3 = [rx, array[rx][rz+1], rz+1]
					
					p = c3
		
		norm = self.normal(c1,c2,c3)
		
		#now we use multiply the normal by v-p to find the height of the surface
		
			
		
		
		part1 = (norm[1]*p[1]) - (norm[0]*(x-p[0])) - (norm[2]*(z-p[2]))
		
		if (norm[1] != 0):
			
			height = part1/norm[1]
		
		else:
			print("ahh")
			
			
		
		
			
			
	
		print(norm)
		return height
		