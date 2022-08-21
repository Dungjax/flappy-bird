from pygame import init,event,FINGERDOWN
init()
from setting import *
from bird import Bird
from pipe import Pipe
from random import randint

class Game:
	def __init__(self):
		self.is_waiting=1
		self.on=1
		self.is_start=0
		self.lose=0
		self.speed=2
		self.score=0
		#player setup
		self.player=Bird()
		bird_group.add(self.player)
		#pipe setup
		self.pipe_size=int(Height/7)
		pipe_group.add(Pipe(randint(self.pipe_size,Height-self.pipe_size*2-base_img.get_height())))
		pipe_group.add(Pipe(pipe_group.sprites()[len(pipe_group)-1].height+self.pipe_size))
		#background & base setup
		self.bg=bgs[randint(0,len(bgs)-1)]
		self.base_offsetx=0
		#message
		self.message_alpha=255
		self.game_over_alpha=0
		self.alpha_speed=15
	
	def cre_pipe(self):
		if pipe_group.sprites()[len(pipe_group)-1].rect.centerx<=Width/2:
			pipe_group.add(Pipe(randint(self.pipe_size,Height-self.pipe_size*2-base_img.get_height())))
			pipe_group.add(Pipe(pipe_group.sprites()[len(pipe_group)-1].height+self.pipe_size))
			
	def collision(self):
		pipe_col=sprite.groupcollide(bird_group,pipe_group,0,0,sprite.collide_mask)
		if pipe_col:
			if self.lose==0:
				audio["hit"].play()
				audio["die"].play()
			self.lose=1
		if self.player.rect_t.bottom>=Height-base_img.get_height():
			if self.lose==0:
				audio["hit"].play()
				audio["die"].play()
			self.lose=2
			
	def draw(self):
		pipe_group.draw(screen)
		bird_group.draw(screen)
		#base
		screen.blit(base_img,(self.base_offsetx,Height-base_img.get_height()))
		if self.lose==0:
			self.base_offsetx-=self.speed
		limit_base_offsetx=base_img.get_width()-Width
		if self.base_offsetx<=-limit_base_offsetx:
			self.base_offsetx=0
		#message
		screen.blit(message_img,(Width/2-message_img.get_width()/2,0))
		message_img.set_alpha(self.message_alpha)
		if self.is_start==1:
			if self.message_alpha>=0:
				self.message_alpha-=self.alpha_speed
		
		if self.lose==1:
			game_over_img.set_alpha(self.game_over_alpha)
			screen.blit(game_over_img,(Width/2-game_over_img.get_width()/2,Height/3))
			if self.game_over_alpha<=255:
				self.game_over_alpha+=self.alpha_speed
		#score
		str_number=str(self.score)
		for i in range(len(str_number)):
			screen.blit(numbers[int(str_number[i])],(Width/2+(i*24)-len(str_number)*(24)/2,Height/8))
			
	def restart(self):
		pipe_group.empty()
		bird_group.empty()
		self.__init__()
		self.on=0
		self.is_waiting=1	
			
	def update(self):
		bird_group.update(self.is_start,self.lose)
		pipe_group.update(self.is_start,self.lose,self.speed)
		
		self.collision()
		if len(pipe_group)>0:
			self.cre_pipe()
		
			if pipe_group.sprites()[0].rect.centerx<=self.player.rect.centerx:
				self.score+=pipe_group.sprites()[0].score
				if pipe_group.sprites()[0].score>0:
					audio["point"].play()
				pipe_group.sprites()[0].score=0
			
	def loop(self):
		while 1:
			while self.is_waiting:
				clock.tick(60)
				for ev in event.get():
					if ev.type==FINGERDOWN:
						self.is_waiting=0
						self.is_start=1
						self.on=1
					self.player.get_input(ev.type==FINGERDOWN)
						
				screen.blit(self.bg,(0,0))
				screen.blit(message_img,(Width/2-message_img.get_width()/2,0))
				self.draw()
				self.update()
				display.update()
						
			while self.on:
				clock.tick(60)
				for ev in event.get():
					if ev.type==FINGERDOWN:
						self.is_start=1
					if self.lose==0:
						self.player.get_input(ev.type==FINGERDOWN)
					elif self.lose==2:
						self.restart()
						
				screen.blit(self.bg,(0,0))
				self.draw()
				self.update()
				display.update()
			
game=Game()
game.loop()