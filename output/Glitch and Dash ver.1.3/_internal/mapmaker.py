import sys,pygame,os,visualization
from pygame import *
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
quit_support=False

game_size=(1064,756)
camera_view_x=0
camera_view_y=0
gray=(128,128,128)
black=(0,0,0)
white=(255,255,255)
red=(255,0,0,255)
green=(0,255,0,255)
blue=(0,0,255,255)
yellow=(255,255,0)
orange=(255,127,0)
rect_list=[]
moving=[]
spike=[]
falling=[]
non_glitch=[]
glitch_crystal=[]
start_point=[0,0,11,11]
end_point=[0,0,11,11]
tv_pos=[]
init()
display_surface=display.set_mode(game_size)

mouse_pos_x=0
mouse_pos_y=0

clicked_point_x=None
clicked_point_y=None
unclicked_point_x=None
unclicked_point_y=None

mouse_left_clicked=False
mouse_left_clicked_reset=True
mouse_wheel_clicked=False
mouse_right_clicked=False

up_pressed=0
down_pressed=0
right_pressed=0
left_pressed=0
glitched_lock=False

def mouse_rect_in(mouse_x,mouse_y,rect):
    if rect[0]<=mouse_x<=rect[0]+rect[2] and rect[1]<=mouse_y<=rect[1]+rect[3]:
        return True
    return False  

def camera_to(rect):
    rect_support=list(rect[:])
    rect_support[0]-=camera_view_x
    rect_support[1]-=camera_view_y
    return rect_support

font.init()
my_font=font.Font(font.get_default_font(),50)
your_font=font.Font(font.get_default_font(),30)
text1=my_font.render("Choose map you want to edit",True,white)
guide_text1=your_font.render("1:moving,2:falling,3:spike,4:crystal,5:non_glitch",True,white)
guide_text2=your_font.render("d:delete,m:move,c:copy,s:start,e:end",True,white)
map_named=os.listdir("./map/")
map_name=[]
for i in map_named:
    if os.path.isfile("./map/"+i):
        map_name.append(i)
map_name2=[]
for i in range(len(map_name)):
    name="map"+str(i+1)+".txt"
    map_name2.append(your_font.render(name,True,white))    
map_name2.append(your_font.render("new",True,white))
map_name3=[]
for i in range(len(map_name)):
    name="map"+str(i+1)+".txt"
    map_name3.append(name)    
map_name3.append("new")
break_support=False
reading_map=""
selectiontimer=timer(1,100)
max_state=len(map_name)//9+1
state=1
while True:
    events=event.get()
    if events != []:
        ret = events[0]
    display_surface.fill(black)
    display_surface.blit(text1,(532-text1.get_width()//2,50))
    if selectiontimer.timer():
        if (ret.type==KEYDOWN and ret.key==K_LEFT):
            if state>1:
                state-=1
        if (ret.type==KEYDOWN and ret.key==K_RIGHT):
            if state<max_state:
                state+=1
    for i in map_name2:
        if 9*state>map_name2.index(i)>=9*(state-1):
            num=map_name2.index(i)
            display_surface.blit(i,(532-i.get_width()//2,100+text1.get_height()+(num-9*(state-1))*(30+i.get_height())))
            page_num=your_font.render("-"+str(state)+"-",True,white)
            display_surface.blit(page_num,(532-page_num.get_width()//2,100+text1.get_height()+9*(30+page_num.get_height())))
            rc=[532-i.get_width()//2,100+text1.get_height()+(num-9*(state-1))*(30+i.get_height()),i.get_width(),i.get_height()]
            draw.rect(display_surface,white,rc,1)
            if rc[0]<=mouse.get_pos()[0]<=rc[0]+rc[2] and rc[1]<=mouse.get_pos()[1]<=rc[1]+rc[3]:
                if mouse.get_pressed()[0]:
                    break_support=True
                    reading_map=map_name3[num]
                    break
    if break_support:
        break
    display.update()
spark_list=[]
def mapreading():
    global rect_list,spike,falling,moving,non_glitch,glitch_crystal,tv_pos,spark_list,camera_limit_move,glitched_lock
    map_dic={}
    rect_list=[]
    falling=[]
    spike=[]
    moving=[]
    non_glitch=[]
    glitch_crystal=[]
    file=open("./map/"+reading_map,'r')
    while True:
        line=file.readline()
        line=line.strip("\n")
        if line=="":
            break
        asd=line.split("=")
        map_dic[asd[0]]=eval(asd[1])
    rect_list=map_dic["map"]
    falling=map_dic["falling_block"]
    spike=map_dic["spike_block"]
    moving=map_dic["moving_block"]
    glitch_crystal=map_dic["glitch_crystal"]
    non_glitch=map_dic["non_glitch_block"]
    moving_block_support=[]
    start_point=[map_dic["start_point"][0],map_dic["start_point"][1]]
    end_point=[map_dic["end_point"][0],map_dic["end_point"][1]]
    if tv_pos!=[]: tv_pos=[map_dic["tv_pos"][0],map_dic["tv_pos"][1]]
    camera_limit_move=map_dic["camera_limit_move"]
    glitched_lock=map_dic["glitched_lock"]
    spark_list=visualization.spark_first_processing(spike)
    file.close()
    return
if not reading_map=="new": mapreading()

while True:
    camera_limit_move=[0,0,0,0]
    for game_event in event.get():
        mouse_pos_x, mouse_pos_y=mouse.get_pos()
        mouse_left_clicked, mouse_wheel_clicked, mouse_right_clicked= mouse.get_pressed()
        
        if mouse_left_clicked and mouse_left_clicked_reset:
            clicked_point_x,clicked_point_y=mouse_pos_x,mouse_pos_y
            mouse_left_clicked_reset=False
        
        if mouse_left_clicked==False and mouse_left_clicked_reset==False:
            unclicked_point_x,unclicked_point_y=mouse_pos_x,mouse_pos_y
            mouse_left_clicked_reset=True
            rect_list.append([min(clicked_point_x,unclicked_point_x)+camera_view_x,min(clicked_point_y,unclicked_point_y)+camera_view_y,abs(clicked_point_x-unclicked_point_x),abs(clicked_point_y-unclicked_point_y)])
        
        if mouse_right_clicked:
            for rect in rect_list:
                if mouse_rect_in(mouse_pos_x+camera_view_x,mouse_pos_y+camera_view_y,rect):
                    if game_event.type==KEYDOWN:
                        if game_event.key==K_d:
                            rect_list.remove(rect)
                            if rect in moving:moving.remove(rect)
                            if rect in falling:falling.remove(rect)
                            if rect in spike:spike.remove(rect)
                            if rect in non_glitch:non_glitch.remove(rect)
                        elif game_event.key==K_m:
                            while not(game_event.type==KEYUP and game_event.key==K_m):
                                support_x,support_y=mouse.get_pos()
                                rect[0],rect[1]=support_x+camera_view_x,support_y+camera_view_y
                                lian=event.get() 
                                if lian!=[]:
                                    game_event=lian[-1]
                        elif game_event.key==K_c:
                            while not(game_event.type==KEYUP and game_event.key==K_c):
                                mouse_pos_x, mouse_pos_y=mouse.get_pos()
                                lian=event.get() 
                                if lian!=[]:
                                    game_event=lian[-1] 
                            rect_list.append([mouse_pos_x+camera_view_x,mouse_pos_y+camera_view_y,rect[2],rect[3]])
                        elif game_event.key==K_1:
                            if rect not in moving:
                                end=[0,0]
                                while not(game_event.type==KEYUP and game_event.key==K_1):
                                    support_x,support_y=mouse.get_pos()
                                    if abs(rect[0]-(support_x+camera_view_x))>=abs(rect[1]-(support_y+camera_view_y)):
                                        support_y=rect[1]-camera_view_y
                                    else:
                                        support_x=rect[0]-camera_view_x
                                    end[0],end[1]=support_x+camera_view_x,support_y+camera_view_y
                                    lian=event.get() 
                                    if lian!=[]:
                                        game_event=lian[-1]
                                moving.append([rect,end])
                        elif game_event.key==K_2:
                            if rect not in falling:
                                falling.append(rect)
                        elif game_event.key==K_3:
                            if rect not in spike:
                                spike.append(rect)
                                rect_list.remove(rect)
                                spark_list=visualization.spark_first_processing(spike)
                        elif game_event.key==K_4:
                            if rect not in glitch_crystal:
                                rect_list.remove(rect)
                                rect[2]=20
                                rect[3]=20
                                glitch_crystal.append(rect)
                                #현재는 제거불가
                        elif game_event.key==K_5:
                            if rect not in non_glitch:
                                non_glitch.append(rect)
                        elif game_event.key==K_s:
                            start_point=[rect[0],rect[1],11,11]
                            rect_list.remove(rect)
                        elif game_event.key==K_e:
                            end_point=[rect[0],rect[1],11,11]
                            rect_list.remove(rect)
                        elif game_event.key==K_t:
                            tv_pos=[rect[0],rect[1]]
                            rect_list.remove(rect)

        if game_event.type==KEYDOWN:
            if game_event.key==K_UP:
                camera_view_y-=100
            elif game_event.key==K_DOWN:
                camera_view_y+=100
            elif game_event.key==K_RIGHT:
                camera_view_x+=100
            elif game_event.key==K_LEFT:
                camera_view_x-=100
            elif game_event.key==K_r:
                camera_view_x,camera_view_y=(0,0)
            
        if game_event.type == KEYDOWN:
            if game_event.key == K_KP8:
                up_pressed = 1
            elif game_event.key == K_KP2:
                down_pressed = 1
            elif game_event.key == K_KP6:
                right_pressed = 1
            elif game_event.key == K_KP4:
                left_pressed = 1
        if game_event.type == KEYUP:
            if game_event.key == K_KP8:
                up_pressed = 0
            elif game_event.key == K_KP2:
                down_pressed = 0
            elif game_event.key == K_KP6:
                right_pressed = 0
            elif game_event.key == K_KP4:
                left_pressed = 0  
                
        if up_pressed:
            camera_view_y-=1
        elif down_pressed:
            camera_view_y+=1
        elif right_pressed:
            camera_view_x+=1
        elif left_pressed:
            camera_view_x-=1   
            

        display_surface.fill(black)
        for rect in non_glitch:
            visualization.normal_block_animation(display_surface,camera_to(rect))
        for rect in rect_list:
            if rect not in non_glitch:
                visualization.matrix(display_surface,camera_to(rect))
        for rect in spike:
            visualization.spark_block_animation(camera_to(rect),display_surface,spark_list)
        for rect in moving:
            rect_support=camera_to(rect[0])
            draw.rect(display_surface,green,rect_support)
            draw.line(display_surface,green,(rect_support[0],rect_support[1]),(rect_support[0]+rect[1][0]-rect[0][0],rect_support[1]+rect[1][1]-rect[0][1]))
        for rect in falling:
            visualization.noise(camera_to(rect),50,display_surface)
        for rect in glitch_crystal:
            rect_support=camera_to(rect)
            draw.polygon(display_surface,orange,[(rect_support[0],rect_support[1]+rect_support[3]/2),(rect_support[0]+rect_support[2]/2,rect_support[1]),(rect_support[0]+rect_support[2],rect_support[1]+rect_support[3]/2),(rect_support[0]+rect_support[2]/2,rect_support[1]+rect_support[3])])
        if tv_pos!=[]: visualization.tv_animation(display_surface,(tv_pos[0]-camera_view_x,tv_pos[1]-camera_view_y),False,False)
        if start_point!=[]:draw.rect(display_surface,yellow,camera_to(start_point))
        if end_point!=[]:draw.rect(display_surface,yellow,camera_to(end_point))
        
        display_surface.blit(guide_text1,(0,0))
        display_surface.blit(guide_text2,(0,50))
        for i in range(1,11):
            draw.line(display_surface,white,(100*i,756),(100*i,0))
            draw.line(display_surface,white,(0,100*i),(1064,100*i))
        draw.circle(display_surface,white,(500,400),200,1)

        if mouse_left_clicked:
            draw.rect(display_surface,gray,(min(clicked_point_x,mouse_pos_x),min(clicked_point_y,mouse_pos_y),abs(clicked_point_x-mouse_pos_x),abs(clicked_point_y-mouse_pos_y)),2)
        display.update()

        if game_event.type == QUIT or (game_event.type==KEYUP and game_event.key==K_ESCAPE) and start_point!=end_point:
            state=0
            text0=my_font.render("new",True,white)
            text1=my_font.render("overwrite",True,white)
            text2=my_font.render("quit",True,white)
            text3=my_font.render("new",True,yellow)
            text4=my_font.render("overwrite",True,yellow)
            text5=my_font.render("quit",True,yellow)
            while True:
                events=event.get()
                if events != []:
                    ret = events[0]
                if state!=0:
                    display_surface.blit(text0,(532-300-text0.get_width()/2,200))
                else:
                    display_surface.blit(text3,(532-300-text0.get_width()/2,200))
                if state!=1:
                    display_surface.blit(text1,(532-text1.get_width()/2,200))
                else:
                    display_surface.blit(text4,(532-text1.get_width()/2,200))
                if state!=2:
                    display_surface.blit(text2,(532+300-text0.get_width()/2,200))
                else:
                    display_surface.blit(text5,(532+300-text0.get_width()/2,200))
                if selectiontimer.timer():
                    if (ret.type==KEYDOWN and ret.key==K_LEFT):
                        if state>0:
                            state-=1
                    if (ret.type==KEYDOWN and ret.key==K_RIGHT):
                        if state<2:
                            state+=1
                        if state==0:    
                            x=1
                    if (ret.type==KEYUP and ret.key==K_ESCAPE):
                        state=3
                        time.delay(1000)
                        display_surface.fill(black)
                        display.update()
                        break
                if (ret.type==KEYDOWN and ret.key==K_x):
                    break
                display.update()
            if state==0:
                for i in range(100):
                    name="map"+str(i)+".txt"
                    if os.path.isfile("./map/"+name):
                        x=i+1
                name="map"+str(x)+".txt"
                file=open("./map/"+name,'w')
                file.write("map="+str(rect_list)+"\n")
                file.write("falling_block="+str(falling)+"\n")
                file.write("spike_block="+str(spike)+"\n")
                file.write("moving_block="+str(moving)+"\n")
                file.write("glitch_crystal="+str(glitch_crystal)+"\n")
                file.write("non_glitch_block="+str(non_glitch)+"\n")
                file.write("start_point="+str(start_point)+"\n")
                file.write("end_point="+str(end_point)+"\n")
                file.write("tv_pos="+str(tv_pos)+"\n")
                file.write("glitched_lock="+str(glitched_lock)+"\n")
                left_limit=camera_limit_move[1]
                right_limit=camera_limit_move[0]
                up_limit=camera_limit_move[3]
                for i in rect_list:
                    left=i[0]
                    right=i[0]+i[2]-1064
                    up=i[1]-300
                    if left_limit>left:
                        left_limit=left
                        camera_limit_move[1]=left_limit
                    if right_limit<right:
                        right_limit=right
                        camera_limit_move[0]=right_limit
                    if up_limit>up:
                        up_limit=up
                        camera_limit_move[3]=up_limit
                file.write("camera_limit_move="+str(camera_limit_move)+"\n")
                file.close()
                quit_support=True
                break
            if state==1:
                name=reading_map
                file=open("./map/"+name,'w')
                file.write("map="+str(rect_list)+"\n")
                file.write("falling_block="+str(falling)+"\n")
                file.write("spike_block="+str(spike)+"\n")
                file.write("moving_block="+str(moving)+"\n")
                file.write("glitch_crystal="+str(glitch_crystal)+"\n")
                file.write("non_glitch_block="+str(non_glitch)+"\n")
                file.write("start_point="+str(start_point)+"\n")
                file.write("end_point="+str(end_point)+"\n")
                file.write("tv_pos="+str(tv_pos)+"\n")
                file.write("glitched_lock="+str(glitched_lock)+"\n")
                left_limit=0
                right_limit=0
                up_limit=0
                for i in rect_list:
                    left=i[0]
                    right=i[0]+i[2]-1064
                    up=i[1]-300
                    if left_limit>left:
                        left_limit=left
                        camera_limit_move[1]=left_limit
                    if right_limit<right:
                        right_limit=right
                        camera_limit_move[0]=right_limit
                    if up_limit>up:
                        up_limit=up
                        camera_limit_move[3]=up_limit
                file.write("camera_limit_move="+str(camera_limit_move)+"\n")
                file.close()
                quit_support=True
                break
            if state==2:
                quit_support=True
                break
    if quit_support: break
quit()