# Imports #
import pygame as pg
import random
from math import *
from level_editor import *
#from cyclops import *
from settings import *
# Settings #
title = 'Stuffy stuffs'
#width = 1350
#height = 600
fps = 120
global gravity
gravity = .02
#COLORS
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
randcolors = [pg.Color('#ffe2e2'),pg.Color('#7579e7'),pg.Color('#ff9a76'),pg.Color('#f0a500'),
              pg.Color('#d6e0f0'),pg.Color('#206a5d')]
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self,world):
        self.world = world
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10,10))
        self.image.fill(white)#pg.Color('#5d54a4'))
        self.rect = self.image.get_rect()
        self.r = vec(width/2,height/2)
        self.rect.x,self.rect.y = self.r.x,self.r.y
        self.v = vec(0,0)
        self.a = vec(0,0)
        self.center = (self.rect.width/2,self.rect.height/2)
        self.jump_clock = 0
        self.dive_clock = 0
        self.fps = fps
        self.offset = vec(0,0)
    def receive(self,keys):
        propulsion = True
        if self.jump_clock>0:
            self.jump_clock -= 1
        if self.dive_clock>0:
            self.dive_clock -= 1
        if (keys[pg.K_SPACE]): #and self.jump_clock==0):
            self.fps = 30
            #self.v.y = -2.5
            self.jump_clock = 30
            #self.dive_clock = 10
            #self.world.all_sprites.add(particle(self.world,self,c='#ffffff',direction='up'))
        if keys[pg.K_1]:
            for m in self.world.mobs:
                m.chase_flag=True
        if keys[pg.K_0]:
            for m in self.world.mobs:
                m.chase_flag=False
        elif(self.jump_clock==0):
            self.fps = fps
        if (keys[pg.K_UP] and self.dive_clock==0):
                self.dive_clock = 10
                self.v.x = 0
                self.v.y = -.5
        if (keys[pg.K_DOWN] and self.dive_clock==0):
                self.dive_clock = 10
                self.v.x = 0
                self.v.y = .5
        if (keys[pg.K_RIGHT] and self.dive_clock==0):
                self.dive_clock = 10
                self.v.x = .5
                self.v.y = 0
        if (keys[pg.K_LEFT] and self.dive_clock==0):
                self.dive_clock = 10
                self.v.x = -.5
                self.v.y = 0
        if keys[pg.K_a]:
            self.a.x=-.02
            #self.a.x = -0.025
            #self.v.x = -1
            self.world.all_sprites.add(particle(self.world,self,c='#28df99',direction='left'))
            self.image.fill(random.choice(randcolors))
        if keys[pg.K_d]:
            if (self.dive_clock==0 and self.jump_clock>0 and 1==2):
                self.dive_clock = self.jump_clock
                self.v.x = 5
                self.v.y = 0
            else:
                self.a.x=.02
                #self.a.x = 0.025
                #self.v.x = 1
                self.world.all_sprites.add(particle(self.world,self,c='#ffb0b0',direction='right'))
                self.image.fill(random.choice(randcolors))
        if keys[pg.K_w]:
            if (self.dive_clock==0 and self.jump_clock>0 and 1==2):
                self.dive_clock = self.jump_clock
                self.v.x = 0
                self.v.y = -5
            else:
                self.a.y=-.1
                self.a.y = -0.035
                self.world.all_sprites.add(particle(self.world,self,c='#c3aed6',direction='up'))
                self.image.fill(random.choice(randcolors))
        if keys[pg.K_s]:
            if (self.dive_clock==0 and self.jump_clock>0 and 1==2):
                self.dive_clock = self.jump_clock
                self.v.y = 2
                self.v.x = 0
            else:
                self.a.y = .02
                self.world.all_sprites.add(particle(self.world,self,'#ffffff',direction='down'))
            self.image.fill(random.choice(randcolors))
        self.world.all_sprites.add(particle(self.world,self,c='#ffffff',direction=None))
        if (self.jump_clock>0 and self.dive_clock==0):
            self.gravity=gravity
        else:
            self.gravity=gravity
        if keys[pg.K_e]:
            self.world.build_level()
        if keys[pg.K_l]:
            self.world.build_level_copy()
    def update(self):
        self.image.fill(black)
        self.a = vec(0,0)
        keys =  pg.key.get_pressed()
        self.receive(keys)
        self.a += vec(0,gravity)
        self.v+=self.a
        #self.r+=self.v + 0.5*self.a
        self.rect.center = self.r
        #self.world.check_collisions()
        self.world.check_collisions2(self,self.world.platforms)
        self.rect.center = self.r
        # map constraints:
        rel = False
        if (1==1):    
            if (self.r.x-self.rect.width/2>width):
                self.r.x = 0 - self.rect.width/2
                self.rect.center = self.r
                self.offset.x += xtiles
                self.world.build_level()
            if (self.r.x+self.rect.width/2<0):
                self.r.x = width + self.rect.width/2
                self.rect.center = self.r
                self.offset.x -= xtiles
                self.world.build_level()
            if (self.r.y-self.rect.height/2>height):
                self.r.y = 0 - self.rect.height/2
                self.rect.center = self.r
                self.offset.y += ytiles
                self.world.build_level()
            if (self.r.y+self.rect.height/2<0):
                self.r.y = height + self.rect.height/2
                self.rect.center = self.r
                self.offset.y -= ytiles
                self.world.build_level()
        print(self.offset)
    # particle class
class particle(pg.sprite.Sprite):
    def __init__(self,world,player,c=None,direction=None,max_size=5):
        pg.sprite.Sprite.__init__(self)
        self.size = 1
        self.image = pg.Surface((self.size,self.size))
        self.color = pg.Color(c)
        self.image.fill(self.color)
        self.center = player.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        self.inertia_mode = False
        self.self_v = vec(0,0)
        self.player=player
        if direction=='up':
            self.rect.y+=int(player.rect.height/2)
            self.rect.x+=random.randrange(-player.rect.width/2,player.rect.width/2)
            self.self_v.y = 1
        elif direction=='down':
            self.rect.y-=int(player.rect.height/2)
            self.rect.x+=random.randrange(-player.rect.width/2,player.rect.width/2)
            self.self_v.y = -1
        elif direction=='right':
            self.rect.x-=int(player.rect.width/2)
            self.rect.y+=random.randrange(-player.rect.height/2,player.rect.height/2)
            self.self_v.x = -1
        elif direction=='left':
            self.rect.x+=int(player.rect.width/2)
            self.rect.y+=random.randrange(-player.rect.height/2,player.rect.height/2)
            self.self_v.x = 1
        elif direction==None:
            self.inertia_mode = True
        self.v = vec(player.v.x,player.v.y)+self.self_v+self.player.world.screen_speed
        self.center = self.rect.center
        self.max_size = max_size
    def update(self):
        self.size += 0.125
        if self.inertia_mode:
            self.image = pg.Surface((1,1))
            self.image.fill(white)
        if self.inertia_mode==False:
            self.image = pg.Surface((self.size,self.size))
            self.rect = self.image.get_rect()
            self.center+=self.v
            self.rect.center = self.center
            if self.color[0]>0:
                self.color[0]-=1
            if self.color[1]>0:
                self.color[1]-=1
            if self.color[2]>0:
                self.color[2]-=1
            self.image.fill(self.color)
        if (self.size>self.max_size):
            self.kill()
        #
class Platform(pg.sprite.Sprite):
    def __init__(self,world,x=100,y=100,w=100,h=100):
        self.world = world
        self.player = self.world.player
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill((black))
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = x,y
class Cyclop(pg.sprite.Sprite):
    def __init__(self,world=None,x=0,y=0):
        self.world = world
        pg.sprite.Sprite.__init__(self)
        self.selftilesize = tilesize
        self.image = pg.Surface((self.selftilesize,self.selftilesize))
        self.image.fill(pg.Color("#68b0ab"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.r = vec(self.rect.midtop[0],self.rect.midleft[1])
        self.dr = vec(0,0)
        self.v = vec(0,0)
        self.initial_pos = vec(self.rect.midtop[0],self.rect.midleft[1])
        self.player_pos = vec(0,0)
        self.vel = 0.01 
        self.a = vec(0,0)
        self.internal_r = vec(0,0)
        self.n = 6
        self.chase_flag = False
    def update(self):
        self.a = vec(0,gravity)
        self.player_pos = [self.world.player.r.x,self.world.player.r.y]
        if (self.initial_pos.x-(self.n+1)*self.selftilesize < self.player_pos[0] < self.initial_pos.x+(self.n+1)*self.selftilesize and self.initial_pos.y-(self.n+1)*self.selftilesize < self.player_pos[1] < self.initial_pos.y+(self.n+1)*self.selftilesize):
                pass
                #self.chase_flag = True
        if self.chase_flag:
            self.chase()
            self.v+=self.a
            self.rect.center=self.r
        else:
            self.a = vec(0,gravity)
            self.v+=self.a
            self.r+=self.v +0.5*self.a+ self.world.screen_speed
        #self.update_pos()
        #self.v+=self.a
        #self.r+=self.v +0.5*self.a+ self.world.screen_speed
        self.rect.center=self.r
        self.initial_pos+=self.world.screen_speed
        self.world.check_collisions2(self,self.world.platforms)
        #print('c: ',self.a,self.v,self.rect.y,'; p: ',self.world.player.a,self.world.player.v,self.world.player.rect.y)
    def chase(self):
        self.player_pos = self.world.player.r
        self.dr = self.player_pos - self.r
        self.a = vec(0,0)
        if self.dr.x>0:
            self.a.x = 2*self.vel
            #self.world.all_sprites.add(particle(self.world,self,c='#28df99',direction='right'))
        if self.dr.x<0:
            self.a.x = -2*self.vel
            #self.world.all_sprites.add(particle(self.world,self,c='#28df99',direction='left'))
        if self.dr.x==0:
            self.a.x=0
        if self.dr.y>0:
            self.a.y = 0
            #wwself.world.all_sprites.add(particle(self.world,self,c='#28df99',direction='down'))
        if self.dr.y<0:
            self.a.y = -1.5*self.vel*2
            #self.world.all_sprites.add(particle(self.world,self,c='#28df99',direction='up'))
        if self.dr.y==0:
            self.a.y=0
        self.a.y+=gravity
        if self.chase_flag==False:
            self.a=vec(0,gravity)
    def update_pos(self):
        self.v+=self.a
        self.r+=self.v +0.5*self.a+ self.world.screen_speed
        self.initial_pos+=self.world.screen_speed
        if self.r.x>self.initial_pos.x+self.n*self.selftilesize:
            self.r.x = self.initial_pos.x+3*self.selftilesize
            self.v.x*=-0.350
        if self.r.x<self.initial_pos.x-self.n*self.selftilesize:
            self.r.x = self.initial_pos.x-+3*self.selftilesize
            self.v.x*=-0.350
        if self.r.y>self.initial_pos.y+self.n*self.selftilesize:
            self.r.y = self.initial_pos.y+3*self.selftilesize
            self.v.y*=-0.350
        if self.r.y<self.initial_pos.y-self.n*self.selftilesize:
            self.r.y = self.initial_pos.y-3*self.selftilesize
            self.v.y*=-0.350
            #if abs(self.v.x<1):
                #self.v.x=0
        self.rect.center = self.r
        #print(self.rect.x,self.rect.y)
        #self.world.check_collisions2()
class Cyclop_copy(pg.sprite.Sprite):
    def __init__(self,world=None,x=0,y=0):
        self.world = world
        pg.sprite.Sprite.__init__(self)
        self.selftilesize = tilesize
        self.image = pg.Surface((self.selftilesize,self.selftilesize))
        self.image.fill(pg.Color("#68b0ab"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.r = vec(self.rect.midtop[0],self.rect.midleft[1])
        self.dr = vec(0,0)
        self.v = vec(0,0)
        self.initial_pos = vec(self.rect.midtop[0],self.rect.midleft[1])
        self.player_pos = vec(0,0)
        self.vel = 0.02*random.random()#0.02 
        self.a = vec(0,0)
        self.internal_r = vec(0,0)
        self.n = 3
    def update(self):
        self.player_pos = [self.world.player.r.x,self.world.player.r.y]
        if (self.initial_pos.x-(self.n+1)*self.selftilesize < self.player_pos[0] < self.initial_pos.x+(self.n+1)*self.selftilesize and self.initial_pos.y-(self.n+1)*self.selftilesize < self.player_pos[1] < self.initial_pos.y+(self.n+1)*self.selftilesize):
                self.chase()
        else:
            self.a = vec(0,gravity)
        self.update_pos()
    def chase(self):
        self.player_pos = self.world.player.r
        self.dr = self.player_pos - self.r
        #self.dr/=sqrt(self.dr.x**2+self.dr.y**2)
        epsilon = 0.10
        self.a = vec(0,gravity)
        if self.dr.x>0:
            self.a.x = self.vel
            self.world.all_sprites.add(particle(self.world,self,c='#28df99',direction='right'))
        if self.dr.x<0:
            self.a.x = -self.vel
            self.world.all_sprites.add(particle(self.world,self,c='#28df99',direction='left'))
        if self.dr.x==0:
            self.a.x=0
        if self.dr.y>0:
            self.a.y = 0#self.vel
            #self.world.all_sprites.add(particle(self.world,self,c='#28df99',direction='down'))
        if self.dr.y<0:
            self.a.y = -0.025
            self.world.all_sprites.add(particle(self.world,self,c='#28df99',direction='up'))
        if self.dr.y==0:
            self.a.y=0
        self.a.y+=gravity

    def update_pos(self):
        self.v+=self.a
        self.r+=self.v +0.5*self.a+ self.world.screen_speed
        self.initial_pos+=self.world.screen_speed
        if self.r.x>self.initial_pos.x+self.n*self.selftilesize:
            self.r.x = self.initial_pos.x+3*self.selftilesize
            self.v.x*=-0.350
        if self.r.x<self.initial_pos.x-self.n*self.selftilesize:
            self.r.x = self.initial_pos.x-+3*self.selftilesize
            self.v.x*=-0.350
        if self.r.y>self.initial_pos.y+self.n*self.selftilesize:
            self.r.y = self.initial_pos.y+3*self.selftilesize
            self.v.y*=-0.350
        if self.r.y<self.initial_pos.y-self.n*self.selftilesize:
            self.r.y = self.initial_pos.y-3*self.selftilesize
            self.v.y*=-0.350
            #if abs(self.v.x<1):
                #self.v.x=0
        self.rect.center = self.r
        #print(self.rect.x,self.rect.y)
        #self.world.check_collisions2()#eye template
class Game:
    def __init__(self):
        # initialize window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width,height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.playing = False
        self.running = True
        self.all_sprites = None
        self.screen_speed = vec(0,0)
        self.screen_pos = vec(0,0)
        self.screen_size = (width,height)
    def new(self):
        # resets the game
        #self.all_sprites = pg.sprite.Group()
        self.all_sprites =  pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player,layer=1)
        p1=Platform(self,x=150,y=height/2,w=width/5,h=height/5)
        p2=Platform(self,x=550,y=height/2,w=width/4,h=height/5)
        self.platforms.add(p1)
        self.platforms.add(p2)
        self.run()
    def run(self):
        # game loop
        self.playing=True
        while self.playing:
            self.clock.tick(self.player.fps)
            self.events()
            self.update()
            self.draw()
    def update(self):
        # game loop update
        self.all_sprites.update()
        self.platforms.update()
        #self.check_screen_movement()
        self.check_collisions2(self.player,self.platforms)
        self.mobs.update()
    def check_screen_movement(self):
        self.screen_speed = vec(0,0)
        if self.player.rect.top <= height/3:
            self.screen_speed.y = int(abs(self.player.v.y+0.5*self.player.a.y))
            if abs(self.player.v.y)<1:
                self.screen_speed.y = 1
        if self.player.rect.bottom >= 2*height/3:
            self.screen_speed.y = -int(abs(self.player.v.y+0.5*self.player.a.y))
            if abs(self.player.v.y)<1:
                self.screen_speed.y = -1
        if self.player.rect.left <= width/3:
            self.screen_speed.x = int(abs(self.player.v.x+0.5*self.player.a.x))
        if self.player.rect.right >= 2*width/3:
            self.screen_speed.x = -int(abs(self.player.v.x+0.5*self.player.a.x))
            if abs(self.player.v.x)<1:
                self.screen_speed.x = -1
        for s in self.all_sprites:
            s.rect.x += self.screen_speed.x
            s.rect.y += self.screen_speed.y
        for s in self.platforms:
            s.rect.x += self.screen_speed.x
            s.rect.y += self.screen_speed.y
        self.player.r.x += self.screen_speed.x
        self.player.r.y += self.screen_speed.y
        self.screen_pos += self.screen_speed
    def check_collisions(self):
        # platform collisions
        dx = self.player.v.x + 0.5*self.player.a.x
        dy = self.player.v.y + 0.5*self.player.a.y
        flagx = True
        flagy = True
        self.player.r.x += dx
        self.player.rect.center = self.player.r
        hits = pg.sprite.spritecollide(self.player,self.platforms,False)
        for hit in hits:
            if abs(self.player.v.x<1):
                self.player.v.x = 0
            else:
                self.player.v.x *= -0.35
            if dx > 0:
                self.player.r.x = hit.rect.midleft[0] - self.player.rect.width/2
                self.player.rect.center = self.player.r
            if dx < 0:
                self.player.r.x = hit.rect.midright[0]+self.player.rect.width/2
                self.player.rect.center = self.player.r
        self.player.r.y += dy
        self.player.rect.center = self.player.r
        hits = pg.sprite.spritecollide(self.player,self.platforms,False)
        for hit in hits:
            if flagy:
                if abs(self.player.v.y<1):
                    self.player.v.y = 0
                else:
                    self.player.v.y *= -0.35
                flagy = False
            if dy > 0:
                self.player.r.y = hit.rect.midtop[1]-self.player.rect.height/2
                self.player.rect.center = self.player.r
            if dy < 0:
                self.player.r.y = hit.rect.midbottom[1]+self.player.rect.height/2
                self.player.rect.center = self.player.r
    def check_collisions2(self,sprite,sprite_group):
        # platform collisions
        dx = sprite.v.x + 0.5*sprite.a.x
        dy = sprite.v.y + 0.5*sprite.a.y
        flagx = True
        flagy = True
        sprite.r.x += dx
        sprite.rect.center = sprite.r
        hits = pg.sprite.spritecollide(sprite,sprite_group,False)
        for hit in hits:
            if abs(sprite.v.x<1):
                sprite.v.x = 0
            else:
                sprite.v.x *= -0.35
            if dx > 0:
                sprite.r.x = hit.rect.midleft[0] - sprite.rect.width/2
                sprite.rect.center = sprite.r
            if dx < 0:
                sprite.r.x = hit.rect.midright[0]+sprite.rect.width/2
                sprite.rect.center = sprite.r
        sprite.r.y += dy
        sprite.rect.center = sprite.r
        hits = pg.sprite.spritecollide(sprite,sprite_group,False)
        for hit in hits:
            if flagy:
                if abs(sprite.v.y<1):
                    sprite.v.y = 0
                else:
                    sprite.v.y *= -0.35
                flagy = False
            if dy > 0:
                sprite.r.y = hit.rect.midtop[1]-sprite.rect.height/2
                sprite.rect.center = sprite.r
            if dy < 0:
                sprite.r.y = hit.rect.midbottom[1]+sprite.rect.height/2
                sprite.rect.center = sprite.r
    def build_level(self):
        l=level_editor(self)
        l.load2(offset=self.player.offset)
        self.screen = pg.display.set_mode((width,height))
        for s in l.all_sprites:
            x,y = s.rect.x,s.rect.y
            if s.tag == 1:
                self.platforms.add(Platform(self,x=x,y=y,w=tilesize,h=tilesize))
            if s.tag == 2:
                self.mobs.add(Cyclop(world=self,x=x,y=y))
        #self.player.v = vec(0,0)
    def build_level_copy(self):
        #for s in self.platforms:
        #    s.kill()
        l = level_editor(self)
        l.new()

        self.screen = pg.display.set_mode((width,height))
        for s in l.all_sprites:
            x,y = s.rect.x,s.rect.y
            if s.tag == 1:
                self.platforms.add(Platform(self,x=x,y=y,w=tilesize,h=tilesize))
            if s.tag == 2:
                self.mobs.add(Cyclop(world=self,x=x,y=y))
        self.player.v = vec(0,0)
        pass
    def events(self):

        # game loop events
        for event in pg.event.get():
            if event.type==pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running=False
                print('Done')
    def draw(self):
        # game loop draw
        self.screen.fill(pg.Color('#393b44'))
        self.all_sprites.draw(self.screen)
        self.platforms.draw(self.screen)
        self.mobs.draw(self.screen)
        pg.display.flip()        
    def show_go_screen(self):
        # game over/continue screen
        pass


g=Game()
while g.running:
    g.new()
    #g.run()
pg.quit()

