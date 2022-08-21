from setting import *

pipes=import_sprite("pipes/")

class Pipe(sprite.Sprite):
	def __init__(self,offsety):
		super().__init__()
		self.width=pipes[0].get_width()
		self.height=offsety
		if len(pipe_group)%2==0:
			self.image=transform.flip(transform.rotate(pipes[0],180),1,0)
			self.rect=self.image.get_rect()
			self.rect.bottomleft=Width,offsety
		else:
			self.image=pipes[0]
			self.rect=self.image.get_rect()
			self.rect.topleft=Width,offsety
		self.mask=mask.from_surface(self.image)
		
		self.score=1
	
	def scroll(self,global_speed):
		self.rect.centerx-=global_speed
	
	def update(self,is_start,lose,global_speed):
		if is_start==1 and lose==0:
			self.scroll(global_speed)
		if self.rect.centerx<0-self.width/2:
			self.kill()