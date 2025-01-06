
qwer=0
import sys, os, visualization
#from imp import reload
map_number=1
file=open("./save_file/savefile.txt","w")
file.write(str(map_number))
file.close()
from pygame import *
on=False
off=True
map_convert=False
class timer():
    def __init__(self,eventtype,cooldown):
        self.eventtype=eventtype
        self.timer_working=False
        self.cooldown=cooldown
    def __str__(self):
        return self.cooldown
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
    def truestarttimer(self):
        if self.timer_working==False:
            self.starttime=time.get_ticks()
            self.timer_working=True
            return True
        currenttime=time.get_ticks()
        if currenttime-self.starttime>=self.cooldown:
            self.timer_working=False
        return False
    def show_frame(self):
        currenttime=time.get_ticks()
        return currenttime-self.starttime
    def reset_timer(self):
        self.starttime=time.get_ticks()

k=1
touched=[]
frequency=50
buho=[1,-1,1,1]
time_set=[True,True,True,True]
cloc=time.Clock()
fps_=60
wallfalling=0
white=(255,255,255)
black=(0,0,0)
gray=(123,123,123)
yellow=(255,255,0)
orange=(255,127,0)
red=(255,0,0)
x,y=532,256
fps=time.Clock()
direction=""
right_pressed=0
left_pressed=0
up_pressed=0
down_pressed=0
c_pressed=0
c_key_reset=1
not_c_key_reset=0
x_pressed=0
x_key_reset=0
not_x_key_reset=0
x_key_possible=0
glitch_delay=0
glitch_delay_count=0
glitch_distance=200
ground=False
ground_col=list(range(2,50))
left_wall_col=list(range(2,50))
left_wall=False
wall=False
right_wall_col=list(range(2,50))
right_wall=False
left_wall_jump=False
right_wall_jump=False
wall_holding_count=0
count=0
a=4
velocity_constant_y=0
display.set_caption('Glitch and Dash')
air = True
dead=True
falling_delay=666
regenerating_delay=10000
crystal_regenerating_delay=5000
glitching=False
glitcher=timer(0,200)
glitching_stop=False
velocity_constant_x=0
matrix_state=0
key_block=[[[0,0,10,10],"1",timer(1,1000)],[[0,0,10,10],"2",timer(1,1000)]]
lock_block=[[[100,100,100,100],["1122"]]]
password=""

character_size=20
screen_x=1064
screen_y=756
game_size=(screen_x,screen_y)
init()
display_s=display.set_mode(game_size,RESIZABLE)

    #####################################################################################################################
    #####################################################################################################################

camera_limit=200
camera_limit_move=[2000,0,0,-2000]
camera_view_x=camera_limit_move[0]
camera_view_y=camera_limit_move[1]

def camera_to(rect):
    rect_support=list(rect[:])
    rect_support[0]-=camera_view_x
    rect_support[1]-=camera_view_y
    return rect_support

map_dic={}
map=[]
falling_block=[]
spike=[]
moving_block=[]
non_glitch_block=[]
glitch_crystal=[]
moving_block_support=[]
falling_block_support=[]
glitch_crystal_support=[]
end_point=[]
start_point=[]
tv_pos=[]
glitched_lock=True
spark_list=[]
lockdelaytimer=timer(1,666)
def mapreading():
    global map_dic,map,falling_block,spike,moving_block,non_glitch_block,glitch_crystal,start_point,end_point,moving_block_support,falling_block_support,falling_delay,regenerating_delay,glitch_crystal_support,crystal_regenerating_delay,tv_pos,glitched_lock,camera_limit_move,spark_list,velocity_constant_y,key_block,lock_block
    map_dic={}
    velocity_constant_y=0
    map=[]
    falling_block=[]
    spike_block=[]
    moving_block=[]
    non_glitch_block=[]
    glitch_crystal=[]
    camera_limit_move=[]
    key_block=[]
    lock_block=[]
    file=open("./save_file/savefile.txt","r")
    mapnumber=file.readline()
    file.close()
    name="map"+mapnumber+".txt"
    if not os.path.isfile("./map/"+name):
        quit()
        sys.exit(0)
    file=open("./map/"+name,'r')
    while True:
        line=file.readline()
        line=line.strip("\n")
        if line=="":
            break
        asd=line.split("=")
        map_dic[asd[0]]=eval(asd[1])
    map=map_dic["map"]
    falling_block=map_dic["falling_block"]
    spike=map_dic["spike_block"]
    moving_block=map_dic["moving_block"]
    glitch_crystal=map_dic["glitch_crystal"]
    non_glitch_block=map_dic["non_glitch_block"]
    if "key_block" in map_dic.keys(): key_block=map_dic["key_block"]
    if "lock_block" in map_dic.keys(): lock_block=map_dic["lock_block"]
    moving_block_support=[]
    for i in moving_block:
        moving_block_support.append([(i[0][:],i[1][:]),False,timer(3,666)])
    falling_block_support=[]
    for i in range(len(falling_block)):
        falling_block_support.append([timer(1,falling_delay),timer(1,regenerating_delay),False,False])
    glitch_crystal_support=[]
    for i in range(len(glitch_crystal)):
        glitch_crystal_support.append([glitch_crystal[i],timer(2,crystal_regenerating_delay),False])
    for i in key_block:
        i.append(timer(1,1000))

    start_point=[map_dic["start_point"][0],map_dic["start_point"][1]]
    end_point=[map_dic["end_point"][0],map_dic["end_point"][1]]
    tv_pos=map_dic['tv_pos']
    glitched_lock=map_dic['glitched_lock']
    camera_limit_move=map_dic['camera_limit_move']
    spark_list=visualization.spark_first_processing(spike)
    file.close()
    visualization.reset_flicking()
    return

def char_rect_collision(x,y,rect):
    if rect[0]-character_size<=x<=rect[0]+rect[2] and rect[1]-character_size<=y<=rect[1]+rect[3]:
        return True
    return False
def rect_expansion(rect,x,y):
    return (rect[0]-x,rect[1]-y,rect[2]+2*x,rect[3]+2*y)

total_timer=timer(0,17)
mapreading()
    #####################################################################################################################
    #####################################################################################################################

font.init()
my_font=font.Font(font.get_default_font(),60)
your_font=font.Font(font.get_default_font(),25)
our_font=font.Font(font.get_default_font(),20)
their_font=font.Font(font.get_default_font(),40)
text1=my_font.render("Glitch and Dash",True,white)
text2=your_font.render("click or press 'x' to start",True,yellow)
menu_text0=your_font.render("start",True,white)
menu_text1=your_font.render("edit",True,white)
menu_text2=your_font.render("quit",True,white)
menu_text3=their_font.render("start",True,yellow)
menu_text4=their_font.render("edit",True,yellow)
menu_text5=their_font.render("quit",True,yellow)
fonttime=timer(7,800)
y=1
startscreen=image.load("./image/startscreen/startscreen.png")
startscreen=transform.scale(startscreen,(1064,756))
startscreen2=image.load("./image/startscreen/startscreen2.png")
startscreen2=transform.scale(startscreen2,(1064,756))
while True:
    total_timer.reset_timer()
    events=event.get()
    display_s.fill(white)
    display_s.blit(startscreen,(0,0))
    display_s.blit(text1,(532-text1.get_width()//2,328-text1.get_height()//2))
    if fonttime.timer():
        y*=-1
    if y==1: display_s.blit(text2,(532-text2.get_width()//2,378+text1.get_height()//2+50))
    
    visualization.noise((532-text1.get_width()//2,378-text1.get_height()//2+20,text1.get_width(),text1.get_height()-40),50,display_s)
    visualization.noise2((532-text1.get_width()//2,378-text1.get_height()//2,text1.get_width(),text1.get_height()),50,display_s,200)
    display.update()
    if events != []:
        ret = events[0]
    mouse_pressed=False
    mouse_pressed=mouse.get_pressed()[0]
    if mouse_pressed or (ret.type==KEYDOWN and ret.key==K_x):
        break 
visualization.screenconversion1_in(display_s)
map_convert=True
state=0
selectiontimer=timer(1,100)
while True:
    display_s.fill(black)
    display_s.blit(startscreen2,(0,0))
    for i in range(3):
        name="menu_text"+str(i)    
        if i!=state: display_s.blit(eval(name),(250,200+100*i))
        if state==i:
            name2="menu_text"+str(state+3)
            display_s.blit(eval(name2),(250,200+100*state))
    if map_convert:
        visualization.screenconversion1_out(display_s)
        map_convert=False
    events=event.get()
    if events != []:
        ret = events[0]
    if selectiontimer.timer():
        if (ret.type==KEYDOWN and ret.key==K_UP):
            if state>0:
                state-=1
        if (ret.type==KEYDOWN and ret.key==K_DOWN):
            if state<2:
                state+=1
    mouse_pressed=False
    mouse_pressed=mouse.get_pressed()[0]
    if (ret.type==KEYDOWN and ret.key==K_x):
        if state==0:
            break
        elif state==1:
            import mapmaker
            quit()
            sys.exit(0)
        elif state==2:
            quit()
            sys.exit(0)
    display.update()
    #####################################################################################################################
    #####################################################################################################################

while True:
    total_timer.timer()
    events = event.get()
    if events != []:
        ret = events[-1]
    if ret.type == QUIT or (ret.type==KEYUP and ret.key==K_ESCAPE ):
        quit()
        sys.exit(0)
    keys=key.get_pressed()
    up_pressed = -1 if keys[K_UP] else 0
    down_pressed = 1 if keys[K_DOWN] else 0
    right_pressed = 1 if keys[K_RIGHT] else 0
    left_pressed = -1 if keys[K_LEFT] else 0
    c_pressed = 1 if keys[K_c] else 0
    x_pressed = 1 if keys[K_x] else 0
    #파이게임에는 키를 누르고있는 상태를 가르키는 이벤트가 없어 변술로따로추가한것이다.
    #X_pressed=1(x키눌린상태)

    if right_pressed==1 and left_pressed==0:
        first_insertion_x=0
    elif right_pressed==0 and left_pressed==-1:
        first_insertion_x=1
    if up_pressed==-1 and down_pressed==0:
        first_insertion_y=0
    elif up_pressed==0 and down_pressed==-1:
        first_insertion_y=1
    
    if not (right_wall_jump or left_wall_jump) and not glitching_stop:
        if right_pressed==1 and left_pressed==-1:
            if first_insertion_x==0:
                x+=a*(left_pressed)
            else: 
                x+=a*(right_pressed)
        else:
            x+=a*(right_pressed +left_pressed)
    #왼쪽과 오른쪽 방향키를 동시입력시 조작이 멈추어버리어
    #선입력값을 주어 왼쪽오른쪽 동시입력시 후입력을 우선시하는 식이다.
    if ground:
        x_key_possible=1
    if x_pressed==1 and x_key_reset==1 and ((left_pressed+right_pressed)**2+(up_pressed+down_pressed)**2)!=0 and not glitched_lock:
        table=[left_pressed,right_pressed,up_pressed,down_pressed]
        x_imsi=x+glitch_distance*(left_pressed+right_pressed)*((left_pressed+right_pressed)**2+(up_pressed+down_pressed)**2)**-0.5
        y_imsi=y+glitch_distance*(up_pressed+down_pressed)*((left_pressed+right_pressed)**2+(up_pressed+down_pressed)**2)**-0.5
        glitching=True
        for i in glitch_crystal:
            g_num=max(int(abs(x_imsi-x)),int(abs(y_imsi-y)))
            for e in range(g_num):
                if char_rect_collision(x+(x_imsi-x)*e/g_num,y-1+(y_imsi-y)*e/g_num,i):
                    glitch_delay=0
                    x_key_possible=1
                    glitch_delay_count=0
                    for k in range(len(glitch_crystal_support)):
                        if glitch_crystal_support[k][0]==i and i in glitch_crystal: 
                            glitch_crystal_support[k][2]=True
                            glitch_crystal.remove(i)
                                         
        for i in non_glitch_block:
            g_num=max(int(abs(x_imsi-x)),int(abs(y_imsi-y)))
            for e in range(g_num):
                if char_rect_collision(x+(x_imsi-x)*e/g_num,y-1+(y_imsi-y)*e/g_num,i):
                    glitching=False
                    x=x+(x_imsi-x)*e/g_num
                    y=y+(y_imsi-y)*e/g_num
                    x_key_reset=0
                    velocity_constant_y=0
                    glitch_delay=1
                    velocity_constant_x=0
                    velocity_constant_y=0
                    break

    if glitching:
        x=x_imsi
        y=y_imsi
        x_key_reset=0
        velocity_constant_y=0
        glitch_delay=1
        velocity_constant_x=0
        velocity_constant_y=0
                    
    if glitch_delay==1:
        glitch_delay_count+=10
    if glitch_delay_count>200:
        glitch_delay=0
        glitch_delay_count=0

    for i in glitch_crystal:
            if char_rect_collision(x,y,i):
                glitch_delay=0
                x_key_possible=1
                glitch_delay_count=0
                for k in range(len(glitch_crystal_support)):
                    if glitch_crystal_support[k][0]==i: 
                        glitch_crystal_support[k][2]=True
                        glitch_crystal.remove(i)
    for i in range(len(glitch_crystal_support)):
        if glitch_crystal_support[i][2]:
            if glitch_crystal_support[i][1].timer():
                glitch_crystal_support[i][2]=False
                glitch_crystal.append(glitch_crystal_support[i][0])
    
    if x_key_possible==1 and x_pressed==0:
        x_key_reset=1
        x_key_possible=0

    right_wall_col=list(range(len(map)))
    left_wall_col=list(range(len(map)))
    ground_col=list(range(len(map)))
    i2=0
    for i in map:
        x_center=x+character_size/2
        y_center=y+character_size/2
        if char_rect_collision(x,y,i):
            left_distance=x_center-i[0]
            upper_distance=y_center-i[1]
            right_distance=i[0]+i[2]-x_center
            down_distance=i[1]+i[3]-y_center
            close=min(left_distance,right_distance,upper_distance,down_distance)
            if close==left_distance:
                x=i[0]-character_size
                velocity_constant_y=0
                if close>0 and glitching:
                    velocity_constant_x=-15
                right_wall_col[i2]=True
                not_c_key_reset=1
            else:
                right_wall_col[i2]=False
            if close==right_distance:
                x=i[0]+i[2]
                velocity_constant_y=0
                if close>0 and glitching:
                    velocity_constant_x=15
                left_wall_col[i2]=True
                not_c_key_reset=1
            else:
                left_wall_col[i2]=False
        
            if  close==upper_distance:
                y=i[1]-character_size
                if close>0 and glitching: 
                    velocity_constant_y=12
                    glitch_delay=0
                    glitch_delay_count=0
                    matrix_state=1
                else: velocity_constant_y=0
                ground_col[i2]=True
                not_c_key_reset=1
            else:
                ground_col[i2]=False
            if  close==down_distance:
                y=i[1]+i[3]
                if close>0 and glitching:
                    velocity_constant_y=-12
                else:
                    velocity_constant_y=0
    
        else: right_wall_col[i2],left_wall_col[i2],ground_col[i2]=False,False,False
        i2+=1

    if velocity_constant_x!=0:
        if velocity_constant_x>0:
            velocity_constant_x-=0.5
        if velocity_constant_x<0:
            velocity_constant_x+=0.5
    x+=velocity_constant_x

    #####################################################################################################################
    #####################################################################################################################

    for i in spike:
        if char_rect_collision(x,y,i):
            dead=True
    
    for i in falling_block:
        if char_rect_collision(x,y,i) and i in map:
            col_rect_num=falling_block.index(i)
            falling_block_support[col_rect_num][2]=True
    for i in range(len(falling_block)):
        if falling_block_support[i][2]:
            if falling_block_support[i][0].timer() or glitching:
                falling_block_support[i][2]=False
                map.remove(falling_block[i])
                falling_block_support[i][3]=True
        if falling_block_support[i][3]:
            if falling_block_support[i][1].timer():
                map.append(falling_block[i])
                falling_block_support[i][3]=False
    
    if y>screen_y:
        dead=True
    
    for i in moving_block:
        if char_rect_collision(x,y,i[0]):
            for j in moving_block_support:
                if j[0][1]==i[1]:
                    j[1]=True
                    break
    for i in moving_block_support:
        if i[1]:
            for k in moving_block:
                if k[1]==i[0][1]:
                    if k[0][0]>=k[1][0] and k[0][1]<=k[1][1]:
                        if i[2].timer():
                            for l in map:
                                if l==k[0]:
                                    l[0]=i[0][0][0]
                                    l[1]=i[0][0][1]
                                    break
                            k[0][0]=i[0][0][0]
                            k[0][1]=i[0][0][1]  
                            i[1]=False
                    elif k[0][0]==k[1][0]:
                        for l in map:
                            if l==k[0]:
                                l[1]-=2
                                break
                        k[0][1]-=2
                        if char_rect_collision(x,y,l): y-=2
                    elif k[0][1]==k[1][1]:
                        for l in map:
                            if l==k[0]:
                                l[0]+=2
                                break
                        k[0][0]+=2
                        if char_rect_collision(x,y,l): x+=2                   
                    break
    
    for rect in key_block:
        if char_rect_collision(x,y,rect[0]):
            if rect[2].truestarttimer():
                if len(password)!=4:
                    password+=rect[1]
    unlocked=False
    for rect in lock_block:
        if rect[1]==password:
            unlocked=True
            if char_rect_collision(x,y,rect[0]): 
                lock_block.remove(rect)
                map.remove(rect[0])
                non_glitch_block.remove(rect[0])
                unlocked=False
                x_key_possible=1
                rect=rect[0]
                if x+character_size==rect[0]:
                    velocity_constant_x=-15
                    velocity_constant_y=12
                elif x==rect[0]+rect[2]:
                    velocity_constant_x=15
                    velocity_constant_y=12
                elif y+character_size==rect[1]:
                    velocity_constant_y=15
                elif y==rect[1]+rect[3]:
                    velocity_constant_y=-15

    if len(password)==4 and not unlocked:
        if lockdelaytimer.timer():
            password=""

    #####################################################################################################################
    #####################################################################################################################

    if True in right_wall_col:
        right_wall=True
    else:
        right_wall=False
    if True in left_wall_col:
        left_wall=True
    else:
        left_wall=False
    if right_wall or left_wall:
        wall=True
    else:
        wall=False
    if True in ground_col:
        ground=True
    else:
        ground=False

    if c_pressed == 1 and ground and c_key_reset==1:
        velocity_constant_y=14

    if not(ground or wall):
        air=True
    else:
        air=False
    if air:
        if c_pressed==0:
            c_key_reset=1
            not_c_key_reset=0
        elif not_c_key_reset==1:
            c_key_reset=0
        matrix_state=0
    if (ground or wall)and c_pressed==0:
        c_key_reset=1        

    if c_pressed and wall and c_key_reset==1 and not(right_wall_jump or left_wall_jump):
        velocity_constant_y=10
        if right_wall==True:
            right_wall_jump=True
        elif left_wall==True:
            left_wall_jump=True
    if right_wall_jump==True:
        x-=a*3
        count+=20
    elif left_wall_jump==True:
        x+=a*3
        count+=20
    if count>200 or ((wall or ground) and count>100):
        count=0
        right_wall_jump=False
        left_wall_jump=False   
    
    if glitching:
        glitching_stop=True
    if glitching_stop:
        if glitcher.timer():
            glitching_stop=False
        

    if not wall and not glitching_stop:
        velocity_constant_y-=0.5
    if velocity_constant_y<=-12:
        velocity_constant_y=-12
    #중력가속도
    if ground:    
        wall_holding_count=100
        wallfalling=1
    else:
        wall_holding_count-=1
        if wall_holding_count<0 and wall:
            y+=wallfalling
    #벽에 일정이상 매달릴시 미끄러짐
    y-=velocity_constant_y
    if x<camera_limit_move[1]:
        x=camera_limit_move[1]
    if x+character_size>camera_limit_move[0]+1064:
        x=camera_limit_move[0]+1064-character_size
    #y축속도
    if dead:
        visualization.fade_out(display_s)
        mapreading()
        visualization.sp_sup=[]
        x,y=start_point
        dead=False
        map_convert=True
        password=""
        
          
    if char_rect_collision(x,y,(end_point[0],end_point[1],11,11)):
        file=open("./save_file/savefile.txt","w")
        map_number=str(int(map_number)+1)
        file.write(map_number)
        file.close()
        mapreading()
        map_convert=True
        visualization.fade_out(display_s)
        visualization.sp_sup=[]
        x,y=start_point
        password=""
        for i in range(4):time.set_timer(USEREVENT+4+i,0)
    
    #####################################################################################################################
    #####################################################################################################################
    i=0
    while True:
        if camera_limit_move[1]>=camera_view_x:
            camera_view_x=camera_limit_move[1]
        if camera_limit_move[2]<=camera_view_y:
            camera_view_y=camera_limit_move[2]
        if camera_limit_move[3]>=camera_view_y:
            camera_view_y=camera_limit_move[3]
        if x-camera_view_x>screen_x/2+camera_limit and camera_limit_move[0]>camera_view_x:
            camera_view_x=x-(screen_x/2+camera_limit)
        if x-camera_view_x<screen_x/2-camera_limit and camera_limit_move[1]<camera_view_x:
            camera_view_x=x-screen_x/2+camera_limit
        if y-camera_view_y>screen_y/2+camera_limit and 0>camera_view_y:
            camera_view_y=y-(screen_y/2+camera_limit)
        if y-camera_view_y<screen_y/2-camera_limit and camera_limit_move[3]<camera_view_y:
            camera_view_y=y-screen_y/2+camera_limit
        i+=1
        if i==2:
            break
        
    display_s.fill(black)
    for i in map:
        visualization.matrix(display_s,camera_to(i))
    
    for i in spike:
        visualization.spark_block_animation(camera_to(i),display_s,spark_list)
    for rect in non_glitch_block:
        if rect not in visualization.flicking_list[0]:
            visualization.normal_block_animation(display_s,camera_to(rect))
    for i in key_block:
        visualization.key_block(display_s,camera_to(i[0]),i[1])
    for i in lock_block:
        if i[0] not in visualization.flicking_list[0]:
            visualization.lock_block(display_s,camera_to(i[0]),password,i[1])
            num=4
            for element,k in zip(list(password),range(len(password))):
                if element in list(i[1])[k]:
                    num-=1
            if num==3:
                freq=200
            if num==2:
                freq=50
            if num==1:
                freq=20
            if num==0:
                freq=0
            if num!=4:
                visualization.noise(camera_to(i[0]),50,display_s,freq)
        num=4
        for element,k in zip(list(password),range(len(password))):
            if element==list(i[1])[k]:
                num-=1
        if num==3:
            freq=800
        if num==2:
            freq=100
        if num==1:
            freq=50
        if num==0:
            freq=3
        if num!=4: visualization.flicking(i[0],freq) 
    for rect in glitch_crystal:
        rect_support=camera_to(rect)
        draw.polygon(display_s,orange,[(rect_support[0],rect_support[1]+rect_support[3]/2),(rect_support[0]+rect_support[2]/2,rect_support[1]),(rect_support[0]+rect_support[2],rect_support[1]+rect_support[3]/2),(rect_support[0]+rect_support[2]/2,rect_support[1]+rect_support[3])])
    
    for rect in map:
        for i in lock_block:
            if i[0]!=rect:
                visualization.flicking(rect)
    for k in moving_block:
        if k[0][0]>=k[1][0] and k[0][1]<=k[1][1]:
            visualization.noise(camera_to(k[0]),50,display_s,25)
    if tv_pos!=[]:
        tv_rect=(tv_pos[0]-20,tv_pos[1]-20,140,140)
        if x_pressed==0:
            qwer=1
        if char_rect_collision(x,y,tv_rect): near=True 
        else: near=False
        if x_pressed==1 and qwer==1 and char_rect_collision(x,y,tv_rect) and off:
            on=True
            off=False
            qwer=0
        if (x_pressed==1 and qwer==1) or not char_rect_collision(x,y,tv_rect):
            off=True
            on=False
            qwer=0
        visualization.tv_animation(display_s,(tv_pos[0]-camera_view_x,tv_pos[1]-camera_view_y),on,off,near,map_number)
    for rect in falling_block:
        if rect in map:
            if char_rect_collision(x,y,rect):
                visualization.noise(camera_to(rect),50,display_s,frequency)
                frequency-=2
                if frequency<1:
                    frequency=1
                touched=rect
            else:
                visualization.noise(camera_to(rect),50,display_s)
                if touched==rect:
                    frequency=50
    if glitching:
        glitching=False  
    draw.rect(display_s,yellow,camera_to((start_point[0],start_point[1],11,11)))
    draw.rect(display_s,yellow,camera_to((end_point[0],end_point[1],11,11)))
    draw.rect(display_s,white,camera_to((x,y,character_size,character_size)))
    if not glitched_lock: draw.circle(display_s,white,(int(x+character_size/2-camera_view_x),int(y+character_size/2-camera_view_y)),200,1)
    #화면에 블록,캐릭터 그리는코드
    if x_key_reset==0 and not glitched_lock:
        draw.rect(display_s,yellow,camera_to((x,y,character_size,character_size)))
        draw.circle(display_s,yellow,(int(x+character_size/2-camera_view_x),int(y+character_size/2-camera_view_y)),200,1)
    #글리츠 사용시 사용함을 노락색으로보여줌
    if camera_limit_move[0]<=camera_view_x:
        cameraview_x=camera_limit_move[0]
    if camera_limit_move[1]>=camera_view_x:
        camera_view_x=camera_limit_move[1]
    if camera_limit_move[2]<=camera_view_y:
        camera_view_y=camera_limit_move[2]
    if camera_limit_move[3]>=camera_view_y:
        camera_view_y=camera_limit_move[3]
    if x-camera_view_x>screen_x/2+camera_limit and camera_limit_move[0]>camera_view_x:
        camera_view_x=x-(screen_x/2+camera_limit)
    if x-camera_view_x<screen_x/2-camera_limit and camera_limit_move[1]<camera_view_x:
        camera_view_x=x-screen_x/2+camera_limit
    if y-camera_view_y>screen_y/2+camera_limit and 0>camera_view_y:
        camera_view_y=y-(screen_y/2+camera_limit)
    if y-camera_view_y<screen_y/2-camera_limit and camera_limit_move[3]<camera_view_y:
        camera_view_y=y-screen_y/2+camera_limit
    while not total_timer.timer():
        keys=key.get_pressed()
        up_pressed = -1 if keys[K_UP] else 0
        down_pressed = 1 if keys[K_DOWN] else 0
        right_pressed = 1 if keys[K_RIGHT] else 0
        left_pressed = -1 if keys[K_LEFT] else 0
        c_pressed = 1 if keys[K_c] else 0
        x_pressed = 1 if keys[K_x] else 0
    milisec_per_frame=total_timer.show_frame()
    frame=1000//milisec_per_frame
    fps="fps:"+str(frame)+" passwword:"+password
    text1=our_font.render(fps,True,white)
    display_s.blit(text1,(20,10))
    if map_convert:
        visualization.fade_in(display_s)
        map_convert=False
    display.update()