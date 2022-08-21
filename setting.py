from pygame import display,SCALED,FULLSCREEN,time,font,sprite,image,transform,mask,mixer
from os import walk
#screen setup
Width=288
Height=512
screen=display.set_mode((Width,Height),SCALED,FULLSCREEN)
#color
red=(255,0,0)
grey=(50,50,50)
#font & text
font=font.Font(None,50)
def cre_text(name,x,y):
	text=font.render(str(name),1,red)
	screen.blit(text,(x,y))
#image
def import_sprite(folder):
	for _,__,img in walk(folder):
		return [image.load(folder+i).convert_alpha() for i in img]

bgs=import_sprite("backgrounds/")

numbers=import_sprite("numbers/")

base_img=image.load("base.png").convert()
message_img=image.load("message.png").convert_alpha()
game_over_img=image.load("gameover.png").convert_alpha()
#time
clock=time.Clock()
#sprite group
bird_group=sprite.Group()
pipe_group=sprite.Group()
bullet_group=sprite.Group()
#sound
for _,__,sound in walk("audio/"):
	audio={i.replace(".wav",""):mixer.Sound("audio/"+i) for i in sound}