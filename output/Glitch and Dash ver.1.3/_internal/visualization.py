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

tv_timer=timer(0,70)
spike_timer=timer(0,100)


init()
white=(255,255,255)
black=(0,0,0)
gray=(128,128,128)
blue=(128,128,128)
red=(255,0,0)
silver=(154,154,154)
green=(0,255,0)
blocksulf=Surface((1000,1000))
blocksulf.fill(black)
blocksulf.set_colorkey(black)
screen_x=1064
screen_y=756
game_size=(screen_x,screen_y)
display_s=display.set_mode(game_size)

background=image.load("./image/background/background.jpg").convert_alpha()
gamemachinescreen=image.load("./image/background/gamemachinescreen.png")
gamemachinescreen=transform.scale(gamemachinescreen,(1064,756)).convert_alpha()

def background_animation(displaysulf,camera_view_x,camera_view_y):
    distance=7
    displaysulf.blit(background,(-camera_view_x/distance+132,-camera_view_y/distance+50))
    displaysulf.blit(gamemachinescreen,(0,0))

nut_img=image.load("./image/block/normal_block/nut.png").convert_alpha()
def normal_block_animation(displaysulf,block):
    arc_block_size=40
    dule=3
    
    if block[2]>=80 and block[3]>=80:    
        for i in range(4):
            if i==0:
                c,d=block[2]-arc_block_size,0
            elif i==1:
                c,d=0,0
            elif i==2:
                c,d=0,block[3]-arc_block_size
            elif i==3:
                c,d=block[2]-arc_block_size,block[3]-arc_block_size
            draw.circle(displaysulf,gray,(int(block[0]+c+arc_block_size/2),int(block[1]+d+arc_block_size/2)),int(arc_block_size/2))
            draw.circle(displaysulf,silver,(int(block[0]+c+arc_block_size/2),int(block[1]+d+arc_block_size/2)),int(arc_block_size/2)-dule)
              
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
    elif block[2]<=block[3] and block[2]>2*dule:
        draw.circle(displaysulf,gray,(int(block[0]+block[2]/2),int(block[1]+block[2]/2)),int(block[2]/2))
        draw.circle(displaysulf,silver,(int(block[0]+block[2]/2),int(block[1]+block[2]/2)),int(block[2]/2-dule))
        draw.circle(displaysulf,gray,(int(block[0]+block[2]/2),int(block[1]+block[3]-block[2]/2)),int(block[2]/2))
        draw.circle(displaysulf,silver,(int(block[0]+block[2]/2),int(block[1]+block[3]-block[2]/2)),int(block[2]/2-dule))
        draw.rect(displaysulf,gray,(block[0],block[1]+block[2]/2,block[2],block[3]-block[2]))
        draw.rect(displaysulf,silver,(block[0]+dule,block[1]+block[2]/2,block[2]-2*dule,block[3]-block[2]))
        displaysulf.blit(nut_img,(int(block[0]+block[2]/2)-10,int(block[1]+block[3]-block[2]/2)-10))
        displaysulf.blit(nut_img,(int(block[0]+block[2]/2)-10,int(block[1]+block[2]/2)-10))
        
    elif block[2]>block[3] and block[3]>2*dule:
        draw.circle(displaysulf,gray,(int(block[0]+block[3]/2),int(block[1]+block[3]/2)),int(block[3]/2))
        draw.circle(displaysulf,silver,(int(block[0]+block[3]/2),int(block[1]+block[3]/2)),int(block[3]/2-dule))
        draw.circle(displaysulf,gray,(int(block[0]+block[2]-block[3]/2),int(block[1]+block[3]/2)),int(block[3]/2))
        draw.circle(displaysulf,silver,(int(block[0]+block[2]-block[3]/2),int(block[1]+block[3]/2)),int(block[3]/2-dule))
        draw.rect(displaysulf,gray,(block[0]+block[3]/2,block[1],block[2]-block[3],block[3]))
        draw.rect(displaysulf,silver,(block[0]+block[3]/2,block[1]+dule,block[2]-block[3],block[3]-2*dule))
        displaysulf.blit(nut_img,(int(block[0]+block[3]/2)-10,int(block[1]+block[3]/2)-10))
        displaysulf.blit(nut_img,(int(block[0]+block[2]-block[3]/2)-10,int(block[1]+block[3]/2)-10))

spark_num=1
spark=timer(0,60)
imagelist=[]
for i in range(4):
    name="./image/block/spark/"+str(i+1)+".png"
    imaged=image.load(name).convert_alpha()
    imagelist.append(imaged)
def spark_animation(scale,angle):
    transformed_image_list=[]
    for i in range(4):    
        imaged=transform.scale(imagelist[i],(scale[0],scale[1]))
        imaged=transform.rotate(imaged,angle)
        transformed_image_list.append(imaged)
    return transformed_image_list
def spark_first_processing(block_list):
    spark_list=[]
    for i in block_list:
        spark_support=[]
        spark_support.append(i)
        for k in range(4):
            transformed_image_list=[]    
            imaged=transform.scale(imagelist[k],(i[2]-20,300))
            imaged=transform.rotate(imaged,0)
            transformed_image_list.append(imaged)
            imaged=transform.scale(imagelist[k],(i[3]-20,300))
            imaged=transform.rotate(imaged,90)
            transformed_image_list.append(imaged)
            spark_support.append(transformed_image_list)
        spark_list.append(spark_support)
    return spark_list

def spark_block_animation(block,displaysulf,spark_list):
    global spark_num
    for i in spark_list:
        if i[0][2]==block[2]:
            if i[0][3]==block[3]:
                break
    if spark.timer():
        spark_num+=1
        if spark_num==5:
            spark_num=1
    displaysulf.blit(i[spark_num][0],(block[0]+block[2]/2-i[spark_num][0].get_width()/2,block[1]-i[spark_num][0].get_height()/2+10))
    displaysulf.blit(i[spark_num][0],(block[0]+block[2]/2-i[spark_num][0].get_width()/2,block[1]+block[3]-i[spark_num][0].get_height()/2-10))
    displaysulf.blit(i[spark_num][1],(block[0]-i[spark_num][1].get_width()/2+10,block[1]+block[3]/2-i[spark_num][1].get_height()/2))
    displaysulf.blit(i[spark_num][1],(block[0]+block[2]-i[spark_num][1].get_width()/2-10,block[1]+block[3]/2-i[spark_num][1].get_height()/2))

def matrix(displaysulf,block):
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

def noise(block,scale,displaysulf,frequency=50):
    buho=1
    k=0
    chopped_size=20
    noise_intensity=20
    frag_num=block[3]//chopped_size+1
    noise_sulf=Surface((block[2]+2*scale,block[3]))
    noise_sulf.blit(displaysulf,(-block[0]+scale,-block[1]))
    for i in range(frag_num):
        k=random.randint(-noise_intensity,noise_intensity)
        if random.randint(0,frequency)!=0:
            k=0
        noised_sulf=Surface((block[2]+2*scale,chopped_size))
        noised_sulf.blit(noise_sulf,(0,-i*chopped_size))
        noise_sulf.blit(noised_sulf,(k,i*chopped_size))     
    displaysulf.blit(noise_sulf,(block[0]-scale,block[1]))
def noise2(block,scale,displaysulf,frequency=50):
    buho=1
    k=0
    chopped_size=20
    noise_intensity=20
    frag_num=block[2]//chopped_size+1
    noise_sulf=Surface((block[2],block[3]+2*scale))
    noise_sulf.blit(displaysulf,(-block[0],-block[1]+scale))
    for i in range(frag_num):
        k=random.randint(-noise_intensity,noise_intensity)
        if random.randint(0,frequency)!=0:
            k=0
        noised_sulf=Surface((chopped_size,block[3]+2*scale))
        noised_sulf.blit(noise_sulf,(-i*chopped_size,0))
        noise_sulf.blit(noised_sulf,(i*chopped_size,k))     
    displaysulf.blit(noise_sulf,(block[0],block[1]-scale))

flicking_list=[[],[]]
def flicking(block,frequency=800,period=100):
    global flicking_list
    if random.randint(0,frequency)==0:    
        if block not in flicking_list[0]:
            flicking_list[0].append(block)
            flicking_list[1].append(timer(1,period))    
    for i,k in zip(flicking_list[0],flicking_list[1]):
        if k.timer():
            flicking_list[0].remove(i)
            flicking_list[1].remove(k)
def reset_flicking():
    flicking_list=[[],[]]
 


img_num=0
a=6
tv_script=image.load("./image/object/tv/script/waiting.png").convert_alpha()
tv_script1=image.load("./image/object/tv/script/1.png").convert_alpha()
tv_script2=image.load("./image/object/tv/script/2.png").convert_alpha()
tv_script5=image.load("./image/object/tv/script/5.png").convert_alpha()
tv_script9=image.load("./image/object/tv/script/9.png").convert_alpha()
tv_script1=transform.scale(tv_script1,(tv_script1.get_width()*a,tv_script1.get_height()*a))
tv_script2=transform.scale(tv_script2,(81*a,50*a))
tv_script5=transform.scale(tv_script5,(81*a,50*a))
tv_script9=transform.scale(tv_script9,(81*a,50*a))
tv_img_list=[]
for i in range(1,11):
    file_name="./image/object/tv/tv_animation/"+str(i)+".png"
    tv_img_list.append(image.load(file_name).convert_alpha())
def tv_animation(displaysulf,pos,on,off,near,mapnumber):
    global img_num
    displaysulf.blit(tv_img_list[img_num],pos)
    if img_num==0:
        if near: displaysulf.blit(tv_script,(pos[0]+50,pos[1]-60))
        tv_switch=False
    else: 
        tv_switch=True
    if on:
        tv_switch=True
    if off:
        tv_switch=False
        img_num=0
    if tv_switch:
        if tv_timer.timer():
            img_num+=1
    if img_num>=10:
        img_num=9
        tv_switch=False
    if img_num==9:
        displaysulf.blit(eval("tv_script"+str(mapnumber)),(pos[0]-tv_script1.get_width()/2,pos[1]-tv_script1.get_height()-10))
fade_list=[]
for i in range(14):
    name="./image/effect/fadein_out/"+str(i)+".png"
    fadeimage=image.load(name)
    fadeimage=transform.scale(fadeimage,(1064,756)).convert_alpha()
    fade_list.append(fadeimage)
fadetimer=timer(1,30)
def fade_out(displaysulf):    
    i=0
    while i<=13:
        displaysulf.blit(fade_list[i],(0,0))
        display.update()
        if fadetimer.timer():
            i+=1
def fade_in(displaysulf):
    supdisplay=display.get_surface().copy()
    i=7
    while i>=0:
        if fadetimer.timer():
            displaysulf.blit(supdisplay,(0,0))
            displaysulf.blit(fade_list[i],(0,0))
            display.update()
            i-=1
scc1in_list=[]
for i in range(8):
    name="./image/effect/screenconversion1/fadein/"+str(i)+".png"
    fadeimage=image.load(name)
    fadeimage=transform.scale(fadeimage,(1064,756)).convert_alpha()
    scc1in_list.append(fadeimage)
scc1out_list=[]
fadetimer2=timer(1,50)
for i in range(7):
    name="./image/effect/screenconversion1/fadeout/"+str(i)+".png"
    fadeimage=image.load(name)
    fadeimage=transform.scale(fadeimage,(1064,756)).convert_alpha()
    scc1out_list.append(fadeimage)
def screenconversion1_in(displaysulf):
    i=0
    while i<=7:
        displaysulf.blit(scc1in_list[i],(0,0))
        display.update()
        if fadetimer2.timer():
            i+=1
def screenconversion1_out(displaysulf):
    supdisplay=display.get_surface().copy()
    i=0
    while i<=6:
        if fadetimer2.timer():
            displaysulf.blit(supdisplay,(0,0))
            displaysulf.blit(scc1out_list[i],(0,0))
            display.update()
            i+=1
font.init()
my_font=font.Font(font.get_default_font(),60)
lock=image.load("./image/block/lock/lock.png").convert_alpha()
lock_num1=image.load("./image/block/lock/key.png").convert_alpha()
lock_num2=image.load("./image/block/lock/key2.png").convert_alpha()
lock_num3=image.load("./image/block/lock/key3.png").convert_alpha()
def key_block(displaysulf,block,key_num):
    draw.rect(displaysulf,white,block)
    text1=my_font.render(key_num,True,black)
    displaysulf.blit(text1,(block[0]+block[2]/2-text1.get_width()/2,block[1]+block[2]/2-text1.get_height()/2))
def lock_block(displaysulf,block,password,password2):
    new_sulf=lock.copy()
    t=-1
    while t!=4:
            t+=1    
            a=random.randint(0,9)
            new_sulf.blit(lock_num3,(10+30*t,140),(15*(int(a)-1),0,15,25))
    for i,k in zip(list(password),range(len(password))):
        if i==list(password2)[k]:
            new_sulf.blit(lock_num1,(10+30*k,140),(15*(int(i)-1),0,15,25))
        elif i!=list(password2)[k]:
            new_sulf.blit(lock_num2,(10+30*k,140),(15*(int(i)-1),0,15,25))
        t=k
        while t!=4:
            t+=1    
            a=random.randint(0,9)
            new_sulf.blit(lock_num3,(10+30*t,140),(15*(int(a)-1),0,15,25))
    new_sulf=transform.scale(new_sulf,(block[2]-20,block[3]-20))
    draw.rect(displaysulf,gray,block)
    displaysulf.blit(new_sulf,(block[0]+10,block[1]+10))
glitch_effect_image_list=[]
for i in range(9):
    gimage=image.load("./image/effect/glitch/"+str(i+4)+".png")
    gimage=transform.scale(gimage,(222,74)).convert_alpha()
    glitch_effect_image_list.append(gimage)
def dead_effect(x,y):
    pass