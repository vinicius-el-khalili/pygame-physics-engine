import pygame as pg
import random
from math import *
from settings import *
class level_editor:
	def __init__(self,world):
		pg.init()
		self.world=world
		self.screen = pg.display.set_mode((width,height))
		self.clock = pg.time.Clock()
		self.running = True
		self.all_sprites = pg.sprite.Group()
		self.world_sprites = pg.sprite.Group()
		for s in self.world.all_sprites:
			self.world_sprites.add(s)
		for plat in self.world.platforms:
			self.all_sprites.add(sprite_icon(world=self,x=plat.rect.x,y=plat.rect.y,color=black,tag=1))
			plat.kill()
		for mob in self.world.mobs:
			self.all_sprites.add(sprite_icon(world=self,x=mob.initial_pos.x-mob.selftilesize/2,y=mob.initial_pos.y-mob.selftilesize/2,color=blue,tag=2))
			mob.kill()
		self.drag = False
		self.dragged = None
		self.erasing = False
		self.creating = False
		self.mousecollision = False
		self.tag = None
		self.color = black
		self.color_box = sprite_icon(world=self,color=self.color,size=(tilesize,tilesize))
		self.x = 0
		self.y = 0
		self.editor_tag = 1

	def update(self):
		self.all_sprites.update()
	def draw (self):
		self.screen.fill(pg.Color('#393b44'))
		for i in range (xtiles):
			pg.draw.line(self.screen,purple,[i*tilesize+self.x,0+self.y],[i*tilesize+self.x,height+self.y],1)
		for i in range (ytiles):
			pg.draw.line(self.screen,purple,[0+self.x,i*tilesize+self.y],[width+self.x,i*tilesize+self.y],1)
		self.all_sprites.draw(self.screen)
		self.world_sprites.draw(self.screen)
		pg.display.flip()
	def new(self):
		#self.all_sprites = pg.sprite.Group()
		self.all_sprites.add(self.color_box)
		self.run()
	def run(self):
		while self.running:
			self.clock.tick(120)
			self.events()
			self.update()
			self.draw()
		if self.running==False:
			file = open('fase.txt','w')
			for s in self.all_sprites:
				if s.tag!=None:
					file.write("%g %g %g\n"%(s.rect.x,s.rect.y,s.tag))
			#pg.quit()
			pass
	def events(self):
		pos = pg.mouse.get_pos()
		self.mousecollision = False
		for s in self.all_sprites:
			if s.rect.collidepoint(pos):
				self.mousecollision = True

		for event in pg.event.get():
			if event.type==pg.QUIT:
				self.running=False
			if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				self.creating = True
				if self.mousecollision:
					self.drag = True	
			if event.type == pg.MOUSEBUTTONUP:
				self.creating,self.erasing,self.drag = False,False,False


		mouse = pg.mouse.get_pressed()
		self.creating,self.erasing=False,False
		if mouse[0]==1 and mouse[2]==0:
			self.creating = True
		if mouse[2]==1 and mouse[0]==0:
			self.erasing = True
		
		if self.creating and not self.mousecollision:
			self.create_sprite(pos)
			#print(len(self.all_sprites))
		if self.erasing and self.mousecollision:
			for s in self.all_sprites:
				if s.rect.collidepoint(pos):
					s.kill()


		
		keys =  pg.key.get_pressed()
		if keys[pg.K_1]:
			self.editor_tag = 1 
			self.color = black
			self.color_box.image.fill(self.color)
		if keys[pg.K_2]:
			self.editor_tag = 2
			self.color = randcolors[2]
			self.color_box.image.fill(self.color)
		if keys[pg.K_3]: 
			self.color = randcolors[3]
			self.color_box.image.fill(self.color)
		if keys[pg.K_4]: 
			self.color = randcolors[4]
			self.color_box.image.fill(self.color)
		if keys[pg.K_q]: 
			self.running = False
		if keys[pg.K_c]:
			for s in self.all_sprites:
				s.kill()
		self.x = 0
		self.y = 0
		if keys[pg.K_UP]:
			self.y = -1
		if keys[pg.K_DOWN]:
			self.y = 1
		if keys[pg.K_RIGHT]:
			self.x = 1
		if keys[pg.K_LEFT]:
			self.x = -1
		if keys[pg.K_l]:
			self.load2()
		for s in self.all_sprites:
			s.rect.x += self.x
			s.rect.y += self.y
	def create_sprite(self,pos):
		mx,my = pos[0],pos[1]
		mx = int(mx/tilesize)*(tilesize)
		my = int(my/tilesize)*(tilesize)
		if self.editor_tag==1:
			self.all_sprites.add(sprite_icon(world=self,x=mx,y=my,color=self.color,tag=1))
		if self.editor_tag==2:
			self.all_sprites.add(sprite_icon(world=self,x=mx,y=my,color=blue,tag=2))
	def events_copy(self):
		#print(type(pg.mouse.get_pressed()))
		for event in pg.event.get():
			pos = pg.mouse.get_pos()
			if event.type==pg.QUIT:
				self.running=False
			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1:
					for s in self.all_sprites:
						if s.rect.collidepoint(pos):
							self.drag = True
							self.draged = s
				if event.button == 3:
					self.erasing = True
			if event.type == pg.MOUSEBUTTONUP:
				if event.button == 1:
					mx,my = pg.mouse.get_pos()
					if self.drag==False:
						mx = int(mx/tilesize)*(tilesize)
						my = int(my/tilesize)*(tilesize)
						if self.editor_tag==1:
							self.all_sprites.add(sprite_icon(world=self,x=mx,y=my,color=self.color,tag=1))
						if self.editor_tag==2:
							self.all_sprites.add(sprite_icon(world=self,x=mx,y=my,color=blue,tag=2))
					if self.drag:
						for s in self.all_sprites:
							if s.rect.collidepoint(pos):
								#mx = int(mx/tilesize)*tilesize
								#my = int(my/tilesize)*tilesize
								s.rect.center = pos
								
					self.drag = False
				self.erasing=False
			if self.drag:
				self.draged.rect.center = pg.mouse.get_pos()
			if self.erasing:
				for s in self.all_sprites:
					if s.rect.collidepoint(pos):
						s.kill()
		keys =  pg.key.get_pressed()
		if keys[pg.K_1]:
			self.editor_tag = 1 
			self.color = black
			self.color_box.image.fill(self.color)
		if keys[pg.K_2]:
			self.editor_tag = 2
			self.color = randcolors[2]
			self.color_box.image.fill(self.color)
		if keys[pg.K_3]: 
			self.color = randcolors[3]
			self.color_box.image.fill(self.color)
		if keys[pg.K_4]: 
			self.color = randcolors[4]
			self.color_box.image.fill(self.color)
		if keys[pg.K_q]: 
			self.running = False
		self.x = 0
		self.y = 0
		if keys[pg.K_UP]:
			self.y = -1
		if keys[pg.K_DOWN]:
			self.y = 1
		if keys[pg.K_RIGHT]:
			self.x = 1
		if keys[pg.K_LEFT]:
			self.x = -1
		if keys[pg.K_l]:
			self.load()
		for s in self.all_sprites:
			s.rect.x += self.x
			s.rect.y += self.y
	def load(self,filename='fase.txt'):
		for s in self.all_sprites:
			s.kill()
		file = open(filename,'r')
		for line in file:
			l = line.split()
			#print (l)
			mx = int(l[0])
			my = int(l[1])
			self.all_sprites.add(sprite_icon(world=self,x=mx,y=my,color=self.color,tag=int(l[2])))	
	def load2(self,offset = vec(0,0)):
		for s in self.all_sprites:
			s.kill()
		for x in range (-1,xtiles+1):
			for y in range (-1,ytiles+1):
				if (noise(x+offset.x,y-offset.y)<0.00002):
					self.create_sprite((x*tilesize,y*tilesize))
		print(len(self.all_sprites))

def noise(x,y):
	return (sin(.1*x)+cos(.1*y)+cos(.2*y)+sin(.5*x))
class sprite_icon(pg.sprite.Sprite):
	def __init__(self,world=None,x=0,y=0,color=white,size=(tilesize,tilesize),tag=None):
		pg.sprite.Sprite.__init__(self)
		self.world = world
		self.color = color
		self.image = pg.Surface(size)
		self.image.fill(self.color)
		self.tag = tag
		self.rect = self.image.get_rect()
		self.rect.x,self.rect.y = x,y
	def update(self):
		if self.tag==1:
			self.image.fill(purple)
			if self.rect.x%tilesize==0:
				self.image.fill(white)
			if self.rect.y%tilesize==0:
				self.image.fill(white)
			if self.rect.x%tilesize==0 and self.rect.y%tilesize==0:
				self.image.fill(self.color)
		


print('kawabanga!')
