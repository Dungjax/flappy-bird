from setting import *
from os import walk
from random import randint

birds=[import_sprite("blue_bird/"),
import_sprite("red_bird/"),
import_sprite("yellow_bird/")]
	
class Bird(sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.sprite_index=0
		self.current_bird=birds[randint(0,2)]
		self.image=self.current_bird[self.sprite_index]
		self.image_t=self.image
		self.rect=self.image.get_rect()
		self.rect.center=Width/4,Height/2
		self.rect_t=self.image.get_rect()
		self.rect_t.center=self.rect.center
		
		self.mask=mask.from_surface(self.image)
		
		self.gravity=0
		self.gravity_accelate=0.2
		self.flap_speed=3
		
		self.angle=0
		
	def animation(self):
		self.sprite_index+=0.2
		if self.sprite_index>=len(self.current_bird):
			self.sprite_index=0
		self.image=self.current_bird[int(self.sprite_index)]
		self.image_t=self.current_bird[int(self.sprite_index)]
	
	def flap(self):
		self.gravity=-self.flap_speed
		audio["wing"].play()
	
	def get_input(self,f_down):
		if f_down:
			self.flap()
		
	def apply_gravity(self):
		self.rect.centery+=self.gravity
		self.rect_t.centery+=self.gravity
		self.gravity+=self.gravity_accelate
	
	def rotate(self):
		self.image=transform.rotate(self.image_t,self.angle)
		self.mask=mask.from_surface(self.image)
		self.rect.center=self.rect_t.centerx-self.image.get_width()/2+self.image_t.get_width()/2,self.rect_t.centery-self.image.get_height()/2+self.image_t.get_height()/2
		
		if self.gravity<0:
			limit_angle_up=40
			if self.angle<limit_angle_up:
				self.angle+=10
		else:
			limit_angle_down=-90
			if self.angle>limit_angle_down:
				self.angle-=self.gravity
		
	def update(self,is_start,lose):
		if lose==0:
			self.animation()
		if is_start==1:
			if self.rect_t.bottom<=Height-base_img.get_height():
				self.apply_gravity()
			self.rotate()