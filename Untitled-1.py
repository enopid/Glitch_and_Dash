from pygame import *
from pygame.surface import Surface
import random
import math

class timer():
    def __init__(self,eventtype,cooldown):
        self.eventtype=eventtype
        self.timer_working=False
        self.cooldown=cooldown
    def set_eventtype(self,eventtype):
        self.eventtype=eventtype
    def get_eventtype(self):
        return self.eventtype
    def set_cooldown(self,cooldown):
        self.cooldown=cooldown
    def timer(self):
        if self.timer_working==False:
            self.starttime=time.get_ticks()
            self.timer_working=True
        currenttime=time.get_ticks()
        if currenttime-self.starttime>=self.cooldown:
            self.timer_working=False
            return True
        return False
    def collected_timer_end(self):
        currenttime=time.get_ticks()
        if currenttime-self.starttime>=self.cooldown:
            self.timer_working=False
    def collected_timer(self):
        if self.timer_working==False:
            self.starttime=time.get_ticks()
            self.timer_working=True
        currenttime=time.get_ticks()
        if currenttime-self.starttime>=self.cooldown:
            return True
        return False
    def reset_timer(self):
        self.starttime=time.get_ticks()

tv_timer=timer(0,1)
spike_timer=timer(0,100)


init()
white=(255,255,255)
black=(0,0,0)
gray=(128,128,128)
blue=(128,128,128)
silver=(154,154,154)
green=(0,255,0)
displaysulf=display.set_mode((1064,800))
blocksulf=Surface((1000,1000))
blocksulf.fill(black)
blocksulf.set_colorkey(black)
displaysulf.fill(white)
enm=5
s_a=-enm
s_b=0
chopped_block_size=12
x_margin=30
y_margin=30
transparency_rate=0
font.init()
my_font=font.Font(font.get_default_font(),chopped_block_size)
block_interval=2
gammadisplay=Surface((100,100))
gammadisplay.set_alpha(transparency_rate)
gammadisplay.fill(black)
gammadisplay.set_colorkey(black)
textdisplay=Surface((100,100))
textdisplay.fill(black)
textdisplay.set_colorkey(black)
def spike_animation(block,s_a):
    global sp_sup,textdisplay,gammadisplay
    s_b=sp_sup[s_a]+enm
    u=block[3]//(chopped_block_size + block_interval)
    if spike_timer.collected_timer():
        a=sp_sup[s_a]
        b=s_b
        #a,b=0,u+1
        if a<0:
            a=0
        if u+1<b:
            b=u+1
        gammadisplay=Surface((block[2]+x_margin,block[3]+y_margin))
        gammadisplay.set_alpha(transparency_rate)
        gammadisplay.fill(black)
        gammadisplay.set_colorkey(black)
        textdisplay=Surface((block[2]+x_margin,block[3]+y_margin))
        textdisplay.fill(black)
        textdisplay.set_colorkey(black)
        for k in range(a,b):
            c=random.randint(0,8)
            for i in range(block[2]//chopped_block_size):
                if (chopped_block_size+block_interval)*i+c+chopped_block_size-16<block[2]:
                    rect=((chopped_block_size+block_interval)*i+c,(chopped_block_size+block_interval)*k,chopped_block_size,chopped_block_size)
                    draw.rect(gammadisplay,blue,rect)
                    d=random.randint(33,127)
                    if random.randint(0,1):
                        text1=my_font.render(chr(d),False,white)
                    else:
                        text1=my_font.render("",False,white)
                    textdisplay.set_colorkey(black)
                    textdisplay.blit(text1,(rect[0],rect[1]))
        sp_sup[s_a]+=1
        if a==u:
            sp_sup[s_a]=-enm
        blocksulf.blit(gammadisplay,(block[0]-8,block[1]))
        blocksulf.blit(textdisplay,(block[0]-8,block[1]))
    displaysulf.blit(blocksulf,(0,0))
sp_sup=[]
def collected_spike_block_animation(block_list):
    global sp_sup,blocksulf
    if spike_timer.collected_timer():
        blocksulf=Surface((1000,1000))
        blocksulf.fill(black)
        blocksulf.set_colorkey(black)
    if sp_sup==[]:
        for i in range(len(block_list)):
            sp_sup.append(-enm)
    for i,j in zip(range(len(block_list)),block_list):
        spike_animation(j,i)
    spike_timer.collected_timer_end()


def normal_block_animation(block):
    arc_block_size=40
    dule=3
    nut_img=image.load("./image/block/normal_block/nut.png")
    for i in range(4):
        if i==0:
            c,d=block[2]-arc_block_size,0
        elif i==1:
            c,d=0,0
        elif i==2:
            c,d=0,block[3]-arc_block_size
        elif i==3:
            c,d=block[2]-arc_block_size,block[3]-arc_block_size
        draw.circle(displaysulf,gray,(block[0]+c+int(arc_block_size/2),block[1]+d+int(arc_block_size/2)),int(arc_block_size/2))
        draw.circle(displaysulf,silver,(block[0]+c+int(arc_block_size/2),block[1]+d+int(arc_block_size/2)),int(arc_block_size/2)-dule)
        nut_img.blit(displaysulf,(block[0]+c,block[1]+d))
    draw.rect(displaysulf,gray,(block[0],block[1]+arc_block_size/2,block[2],block[3]-arc_block_size))
    draw.rect(displaysulf,silver,(block[0]+dule,block[1]+arc_block_size/2,block[2]-2*dule,block[3]-arc_block_size))
    draw.rect(displaysulf,gray,(block[0]+arc_block_size/2,block[1],block[2]-arc_block_size,block[3]))
    draw.rect(displaysulf,silver,(block[0]+arc_block_size/2,block[1]+dule,block[2]-arc_block_size,block[3]-2*dule))
    for i in range(4):
        if i==0:
            c,d=block[2]-arc_block_size,0
        elif i==1:
            c,d=0,0
        elif i==2:
            c,d=0,block[3]-arc_block_size
        elif i==3:
            c,d=block[2]-arc_block_size,block[3]-arc_block_size
        displaysulf.blit(nut_img,(block[0]+c+10,block[1]+d+10))
img_num=0
def tv_animation(pos):
    global img_num
    tv_img_list=[]
    tv_script=image.load("./image/object/tv/script/waiting.png")
    for i in range(1,11):
        file_name="./image/object/tv/tv_animation/"+str(i)+".png"
        tv_img_list.append(image.load(file_name))
    displaysulf.blit(tv_img_list[img_num],pos)
    if img_num==0:
        displaysulf.blit(tv_script,(pos[0]+50,pos[1]-60))
        tv_switch=False
    else: 
        tv_switch=True
    if mouse.get_pressed()[0]:
        tv_switch=True
    if mouse.get_pressed()[2]:
        tv_switch=False
        img_num=0
    if tv_switch:
        if tv_timer.timer():
            img_num+=1
    if img_num>=10:
        img_num=9
        tv_switch=False
spark_num=0
spark=timer(0,60)
def spark_animation(center,scale,angle=0):
    global spark_num
    imagelist=[]
    for i in range(4):
        name="./image/block/spark/"+str(i+1)+".png"
        imaged=image.load(name).convert_alpha()
        imagelist.append(imaged)
    if spark.timer():
        spark_num+=1
        if spark_num==4:
            spark_num=0
    imaged=transform.scale(imagelist[spark_num],(scale[0],scale[1]))
    imagedd=transform.rotate(imaged,angle)
    displaysulf.blit(imagedd,(center[0]-imagedd.get_width()/2,center[1]-imagedd.get_height()/2))
def spark_block_animation(block):
    spark_animation((block[0]+block[2]/2,block[1]),(block[2],300))
    spark_animation((block[0]+block[2]/2,block[1]+block[3]),(block[2],300))
    spark_animation((block[0],block[1]+block[3]/2),(block[3],300),90)
    spark_animation((block[0]+block[2],block[1]+block[3]/2),(block[3],300),90)
def matrix(block):
    dule=2
    interval=40
    interval2=20
    width1=3
    width2=1
    draw.rect(displaysulf,gray,block)
    draw.rect(displaysulf,black,(block[0]+dule,block[1]+dule,block[2]-2*dule,block[3]-2*dule))
    i=0
    while block[2]/2-i*interval2>dule:
        draw.line(displaysulf,green,(block[0]+block[2]/2+i*interval2,block[1]+dule),(block[0]+block[2]/2+i*interval2,block[1]+block[3]-dule),width2)
        i+=1
    i=0
    while block[2]/2-i*interval2>dule:
        draw.line(displaysulf,green,(block[0]+block[2]/2-i*interval2,block[1]+dule),(block[0]+block[2]/2-i*interval2,block[1]+block[3]-dule),width2)
        i+=1
    i=0
    while block[3]/2-i*interval2>dule:
        draw.line(displaysulf,green,(block[0]+dule,block[1]+block[3]/2+i*interval2),(block[0]+block[2]-dule,block[1]+block[3]/2+i*interval2),width2)
        i+=1
    i=0
    while block[3]/2-i*interval2>dule:
        draw.line(displaysulf,green,(block[0]+dule,block[1]+block[3]/2-i*interval2),(block[0]+block[2]-dule,block[1]+block[3]/2-i*interval2),width2)
        i+=1
    i=0
    while block[2]/2-i*interval>dule:
        draw.line(displaysulf,white,(block[0]+block[2]/2+i*interval,block[1]+dule),(block[0]+block[2]/2+i*interval,block[1]+block[3]-dule),width1)
        i+=1
    i=0
    while block[2]/2-i*interval>dule:
        draw.line(displaysulf,white,(block[0]+block[2]/2-i*interval,block[1]+dule),(block[0]+block[2]/2-i*interval,block[1]+block[3]-dule),width1)
        i+=1
    i=0
    while block[3]/2-i*interval>dule:
        draw.line(displaysulf,white,(block[0]+dule,block[1]+block[3]/2+i*interval),(block[0]+block[2]-dule,block[1]+block[3]/2+i*interval),width1)
        i+=1
    i=0
    while block[3]/2-i*interval>dule:
        draw.line(displaysulf,white,(block[0]+dule,block[1]+block[3]/2-i*interval),(block[0]+block[2]-dule,block[1]+block[3]/2-i*interval),width1)
        i+=1

def noise(block,scale):
    buho=1
    k=0
    chopped_size=20
    noise_power=20
    frag_num=block[3]//chopped_size
    noise_sulf=Surface((block[2]+2*scale,block[3]))
    noise_sulf.blit(displaysulf,(-block[0]+scale,-block[1]))
    for i in range(frag_num):
        k=random.randint(-noise_power,noise_power)
        if random.randint(0,50)!=0:
            k=0
        noised_sulf=Surface((block[2]+2*scale,chopped_size))
        noised_sulf.blit(noise_sulf,(0,-i*chopped_size))
        noise_sulf.blit(noised_sulf,(k,i*chopped_size))     
    displaysulf.blit(noise_sulf,(block[0]-scale,block[1]))
fade_list=[]
for i in range(14):
    name="./image/effect/fadein&out/"+str(i)+".png"
    fadeimage=image.load(name)
    fadeimage=transform.scale(fadeimage,(1064,756)).convert_alpha()
    fade_list.append(fadeimage)
fadetimer=timer(1,300)
def fade_out(displaysulf):    
    i=0
    while i<=13:
        displaysulf.blit(fade_list[i],(0,0))
        display.update()
        if fadetimer.timer():
            i+=1
def fade_in(displaysulf):
    supdisplay=display.get_surface().copy()
    i=10
    while i>=0:
        displaysulf.blit(supdisplay,(0,0))
        displaysulf.blit(fade_list[i],(0,0))
        image.save(supdisplay,"./fuc.jpeg")
        display.update()
        if fadetimer.timer():
            i-=1 
while True:
    displaysulf.fill(white)
    normal_block_animation((200,400,500,100))
    normal_block_animation((300,0,300,300))
    matrix((400,600,500,100))
    normal_block_animation((700,0,100,500))
    tv_animation((0,300))
    spark_block_animation((200,400,500,100))
    spark_block_animation((700,0,100,500))
    noise((300,0,300,300),50)
    if mouse.get_pressed()[0]:
        fade_out(displaysulf)
    if mouse.get_pressed()[2]:
        fade_in(displaysulf)
    display.update()
    for game_event in event.get():
        if game_event.type == QUIT or (game_event.type==KEYUP and game_event.key==K_ESCAPE ):
            quit()