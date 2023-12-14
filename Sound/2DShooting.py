import pygame,os,random,sys
from pygame.locals import *
import math

class G: #Class for some global variables
    S_width = 930
    S_height = 630
    Max_width = 930
    Max_height = 730
    O_width = 50
    O_height = 50
    C_width = 30
    C_height = 30
    W_width = 15
    W_height = 15
    O_number = 20
    C_number = 10
    E_width = 30
    E_height = 30
    E_number = 3
    A_width = 30
    A_height = 30
    A_number = 5
    X_width = 30
    X_height = 30
    X_number =5
    M_width = 30
    M_height =30
    M_number = 3
    upbullet = 5
    gold_point = 500
    c_group = pygame.sprite.Group()   #coin group
    r_group = pygame.sprite.Group()#role group
    br_group = pygame.sprite.Group()# bullet group
    o_group = pygame.sprite.Group()# barrier group
    e_group = pygame.sprite.Group()
    a_group = pygame.sprite.Group()
    x_group = pygame.sprite.Group()
    m_group = pygame.sprite.Group()
    be_group = pygame.sprite.Group()
    oarmor = 76
    ohealth = 76
    oneEhealth = 10
    onehit = 1
    oneshoot = 76
    onershoot = 6
    Maxarmor = 380
    Maxhealth = 380
    Ehealth = 30



    
# Model
class role(pygame.sprite.Sprite):#role
    def __init__(self):
        super().__init__()
        self.master_image = pygame.image.load('role2.png').convert_alpha()  # 导入人物动画完整图像
        self.rect=self.master_image.get_rect()
        self.frame_width=self.rect.width//9  #整个图像分层9列--就是每个画面的宽
        self.frame_height =self.rect.height//4  #整个图像分层4行--就是每个画面的高
        self.image = self.master_image.subsurface((0,2*self.frame_height,self.frame_width,self.frame_height))
        self.rect=self.image.get_rect()
        self.rect.x = G.W_width
        self.rect.y = G.W_height

        #初始动作向右-4行0列的动作
        #每帧画面
        self.mask=pygame.mask.from_surface(self.image)
        self.x = 0   #x轴每次移动量
        self.y = 0  # y轴每次移动量
        self.row = 3  # 记录行
        self.col = 0  # 记录列
        self.co=0 #列偏移量
        self.prex =0 #role 的初始x
        self.prey =0 #role 的初始y
        self.health = 5*G.oarmor
        self.armor =0
        self.bn =10
        self.gold = 0
        self.point =0
        self.flash =1
        self.snd = pygame.mixer.Sound('walk.wav')
        
        

    def update(self):  # update function
        self.prex = self.rect.x
        self.prey = self.rect.y
        self.rect.x =self.rect.x+self.x*1.2
        self.rect.y = self.rect.y + self.y*1.2        #更新人物坐标



        self.col+=self.co  #一个方向动作循环
        if self.col>8:
            self.col=0
        self.image = self.master_image.subsurface((self.col*self.frame_width, self.row * self.frame_height, self.frame_width, self.frame_height))


class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.master_image = pygame.image.load('E1.png').convert_alpha()  # 导入人物动画完整图像
        self.rect=self.master_image.get_rect()
        self.frame_width=self.rect.width//4  #整个图像分层4列--就是每个画面的宽
        self.frame_height =self.rect.height//4  #整个图像分层4行--就是每个画面的高
        self.image = self.master_image.subsurface((0,0,self.frame_width,self.frame_height))
        self.rect=self.image.get_rect()
        self.rect.x = G.W_width
        self.rect.y = G.W_height



        self.mask=pygame.mask.from_surface(self.image)
        self.x=0   #x轴每次移动量
        self.y = 0  # y轴每次移动量
        self.row = 0
        self.col = 0
        self.co = 0 #列偏移量
        self.speed = 1
        self.prex =0
        self.prey =0
        self.health = 3*G.oneEhealth


    def update(self,nx,ny):
        dx = self.rect.x - nx
        dy = self.rect.y - ny

        if dx == 0:
            if dy > 0:
                self.y = -1
                self.x = 0
                self.row = 3
                
            else:
                self.y = 1
                self.x = 0
                self.row = 0
        elif dy == 0:
            if dx >0:
                self.x = -1
                self.y =0
                self.row = 1
            else:
                self.x = 1
                self.y =0
                self.row = 2
        else:
            if self.prex == self.rect.x and self.prey == self.rect.y:
                if self.y == 0:
                    self.x = 0
                    if dy > 0:
                        self.y = -1
                        self.row = 3
                    else:
                        self.y = 1
                        self.row = 0
                else:
                    self.y = 0
                    if dx > 0:
                        self.x = -1
                        self.row = 1
                    else:
                        self.x = 1
                        self.row = 2
            else:
                self.y = 0
                if dx > 0:
                    self.x = -1
                    self.row = 1
                else:
                    self.x = 1
                    self.row = 2
            



        self.prex = self.rect.x
        self.prey = self.rect.y
        self.rect.x += self.x * self.speed*1.2
        self.rect.y += self.y * self.speed*1.2


          

        shoot= random.randint(0,70)
        if shoot == 0:
            be = bullet_enemy()
            snd = pygame.mixer.Sound('shoot.wav')
            snd.set_volume(0.2)
            snd.play()
            if self.row == 2:                
               
                be.rect.x = self.rect.x + self.frame_width
                be.rect.y = self.rect.y + self.frame_height//2 - be.frame_height//2
                be.x = 5
                be.y = 0

            if self.row == 1:
                
                be.rect.x = self.rect.x - be.frame_width 
                be.rect.y = self.rect.y + self.frame_height//2 - be.frame_height//2
                be.x = -5
                be.y = 0

            if self.row == 3:
                
                be.rect.x = self.rect.x  + self.frame_width//2 - be.frame_width//2
                be.rect.y = self.rect.y - be.frame_height 
                be.x = 0
                be.y = -10


            if self.row == 0:
                
                be.rect.x = self.rect.x + self.frame_width//2 - be.frame_width//2
                be.rect.y = self.rect.y + self.frame_height 
                be.x = 0
                be.y = 5

            G.be_group.add(be)


        self.col+=self.co  #一个方向动作循环
        if self.col>3:
            self.col=0
        self.image = self.master_image.subsurface((self.col*self.frame_width, self.row * self.frame_height, self.frame_width, self.frame_height))


class coin(pygame.sprite.Sprite):  #coin
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('coin.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)


class Armor(pygame.sprite.Sprite):  #Armor
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('armor.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)


class BB(pygame.sprite.Sprite):  #blood box
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Blood.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)


class caisson(pygame.sprite.Sprite):  #caisson
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('caisson.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)


class barrier(pygame.sprite.Sprite):#barrier
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('box.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)


class wall(pygame.sprite.Sprite): #wall 我用wall围一圈就是方便判定子弹和边界的冲突
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('wall.GIF').convert_alpha()
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)


class bullet_role(pygame.sprite.Sprite): #bullet
    def __init__(self):
        super().__init__()
        self.master_image = pygame.image.load('bullet.PNG').convert_alpha()  
        self.rect=self.master_image.get_rect()
        self.frame_width = self.rect.width//6
        self.frame_height =self.rect.height

        self.image = self.master_image.subsurface(0,0,self.frame_width,self.frame_height) 
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.x = 0
        self.y = 0

        

    def update(self): #子弹的新的坐标
        self.rect.x = self.rect.x + self.x
        self.rect.y = self.rect.y + self.y



class bullet_enemy(pygame.sprite.Sprite): #bullet
    def __init__(self):
        super().__init__()
        self.master_image = pygame.image.load('bullet2.GIF').convert_alpha()
        self.rect=self.master_image.get_rect()
        self.frame_width = self.rect.width
        self.frame_height =self.rect.height

        self.image = self.master_image.subsurface(0,0,self.frame_width,self.frame_height) 
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.x = 0
        self.y = 0

        

    def update(self): #子弹的新的坐标
        self.rect.x = self.rect.x + self.x
        self.rect.y = self.rect.y + self.y




def Create_enemy():
    
    ex = (G.S_width  - 2* G.W_width)// G.E_width
    ey = (G.S_height - 2* G.W_height) // G.E_height

    e=enemy()
    while True:
        e.rect.x = random.randint(0,ex-1) * G.E_width + G.W_width
        e.rect.y = random.randint(0,ey-1) * G.E_height + G.W_height

        E = pygame.sprite.spritecollide(e, G.e_group, False, pygame.sprite.collide_mask)  # collision
        if E:
            continue
        if pygame.sprite.collide_rect(e,r):
            continue
        E = pygame.sprite.spritecollide(e, G.o_group, False, pygame.sprite.collide_mask)  # collision
        if E:
            continue
        E = pygame.sprite.spritecollide(e, G.c_group, False, pygame.sprite.collide_mask)  # collision
        if E:
            continue
        E = pygame.sprite.spritecollide(e, G.a_group, False, pygame.sprite.collide_mask)  # collision
        if E:
            continue
        E = pygame.sprite.spritecollide(e, G.x_group, False, pygame.sprite.collide_mask)  # collision
        if E:
            continue
        E = pygame.sprite.spritecollide(e, G.m_group, False, pygame.sprite.collide_mask)  # collision
        if E:
            continue
        break

    G.e_group.add(e)



def Create_O():
    ox = (G.S_width  - 2* G.W_width) // G.O_width
    oy = (G.S_height - 2* G.W_height) // G.O_height

    o = barrier()

    while True:
        o.rect.x = random.randint(0,ox-1) * G.O_width + G.W_width
        o.rect.y = random.randint(0,oy-1) * G.O_height + G.W_height
        O = pygame.sprite.spritecollide(o, G.o_group, False, pygame.sprite.collide_mask)  # collision
        if O:
            continue
        if pygame.sprite.collide_rect(o,r):
            continue
        O = pygame.sprite.spritecollide(o, G.c_group, False, pygame.sprite.collide_mask)  # collision
        if O:
            continue
        O = pygame.sprite.spritecollide(o, G.a_group, False, pygame.sprite.collide_mask)  # collision
        if O:
            continue
        O = pygame.sprite.spritecollide(o, G.x_group, False, pygame.sprite.collide_mask)  # collision
        if O:
            continue

        O = pygame.sprite.spritecollide(o, G.m_group, False, pygame.sprite.collide_mask)  # collision
        if O:
            continue
        O = pygame.sprite.spritecollide(o, G.e_group, False, pygame.sprite.collide_mask)  # collision
        if O:
            continue
        break
    G.o_group.add(o)

def Create_coin():
    cx = (G.S_width  - 2* G.W_width)// G.C_width
    cy = (G.S_height - 2* G.W_height) // G.C_height

    c=coin()

    while True:
        c.rect.x = random.randint(0,cx-1) * G.C_width + G.W_width
        c.rect.y = random.randint(0,cy-1) * G.C_height + G.W_height
        C = pygame.sprite.spritecollide(c, G.c_group, False, pygame.sprite.collide_mask)  # collision
        if C:
            continue
        if pygame.sprite.collide_rect(c,r):
            continue
        C = pygame.sprite.spritecollide(c, G.o_group, False, pygame.sprite.collide_mask)  # collision
        if C:
            continue
        C = pygame.sprite.spritecollide(c, G.a_group, False, pygame.sprite.collide_mask)  # collision
        if C:
            continue
        C = pygame.sprite.spritecollide(c, G.x_group, False, pygame.sprite.collide_mask)  # collision
        if C:
            continue

        C = pygame.sprite.spritecollide(c, G.m_group, False, pygame.sprite.collide_mask)  # collision
        if C:
            continue
        C = pygame.sprite.spritecollide(c, G.e_group, False, pygame.sprite.collide_mask)  # collision
        if C:
            continue
        break
    G.c_group.add(c)



def Create_armor():
    ax = (G.S_width  - 2* G.W_width)// G.C_width
    ay = (G.S_height - 2* G.W_height) // G.C_height

    a=Armor()

    while True:
        a.rect.x = random.randint(0,ax-1) * G.A_width + G.W_width
        a.rect.y = random.randint(0,ay-1) * G.A_height + G.W_height
        A = pygame.sprite.spritecollide(a, G.a_group, False, pygame.sprite.collide_mask)  # collision
        if A:
            continue
        if pygame.sprite.collide_rect(a,r):
            continue
        A = pygame.sprite.spritecollide(a, G.o_group, False, pygame.sprite.collide_mask)  # collision
        if A:
            continue
        A = pygame.sprite.spritecollide(a, G.c_group, False, pygame.sprite.collide_mask)  # collision
        if A:
            continue
        A = pygame.sprite.spritecollide(a, G.x_group, False, pygame.sprite.collide_mask)  # collision
        if A:
            continue

        A = pygame.sprite.spritecollide(a, G.m_group, False, pygame.sprite.collide_mask)  # collision
        if A:
            continue
        A = pygame.sprite.spritecollide(a, G.e_group, False, pygame.sprite.collide_mask)  # collision
        if A:
            continue
        break
    G.a_group.add(a)


def Create_bloodbox():
    xx = (G.S_width  - 2* G.W_width)// G.C_width
    xy = (G.S_height - 2* G.W_height) // G.C_height
    x=BB()

    while True:
        x.rect.x = random.randint(0,xx-1) * G.X_width + G.W_width
        x.rect.y = random.randint(0,xy-1) * G.X_height + G.W_height
        X = pygame.sprite.spritecollide(x, G.x_group, False, pygame.sprite.collide_mask)  # collision
        if X:
            continue
        if pygame.sprite.collide_rect(x,r):
            continue
        X = pygame.sprite.spritecollide(x, G.o_group, False, pygame.sprite.collide_mask)  # collision
        if X:
            continue
        X = pygame.sprite.spritecollide(x, G.c_group, False, pygame.sprite.collide_mask)  # collision
        if X:
            continue
        X = pygame.sprite.spritecollide(x, G.a_group, False, pygame.sprite.collide_mask)  # collision
        if X:
            continue

        X = pygame.sprite.spritecollide(x, G.m_group, False, pygame.sprite.collide_mask)  # collision
        if X:
            continue
        X = pygame.sprite.spritecollide(x, G.e_group, False, pygame.sprite.collide_mask)  # collision
        if X:
            continue
        break
    G.x_group.add(x)

    
def Create_caisson():
    
    mx = (G.S_width  - 2* G.W_width)// G.C_width
    my = (G.S_height - 2* G.W_height) // G.C_height

    m=caisson()

    while True:
        m.rect.x = random.randint(0,mx-1) * G.M_width + G.W_width
        m.rect.y = random.randint(0,my-1) * G.M_height + G.W_height
        M = pygame.sprite.spritecollide(m, G.m_group, False, pygame.sprite.collide_mask)  # collision
        if M:
            continue
        if pygame.sprite.collide_rect(m,r):
            continue    
        M = pygame.sprite.spritecollide(m, G.o_group, False, pygame.sprite.collide_mask)  # collision
        if M:
            continue
        M = pygame.sprite.spritecollide(m, G.c_group, False, pygame.sprite.collide_mask)  # collision
        if M:
            continue
        M = pygame.sprite.spritecollide(m, G.a_group, False, pygame.sprite.collide_mask)  # collision
        if M:
            continue

        M = pygame.sprite.spritecollide(m, G.x_group, False, pygame.sprite.collide_mask)  # collision
        if M:
            continue
        M = pygame.sprite.spritecollide(m, G.e_group, False, pygame.sprite.collide_mask)  # collision
        if M:
            continue
        break
    G.m_group.add(m)
    



        
# Initialization
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Set up the screen
screen = pygame.display.set_mode((G.Max_width,G.Max_height))
pygame.display.set_caption("Shoooot")
clock = pygame.time.Clock()
count = 1
count2 = 1
score=0

# Load images
menu = pygame.image.load("title.png")
end = pygame.image.load("end.png")


# Menus
def start_menu():
    while True:
        screen.blit(menu,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False
        pygame.display.update()

def end_screen():
    while True:

        screen.blit(end, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        pygame.display.update()

# Pause
white = (255, 255, 255)
black = (  0,   0,   0)
green = (0, 255, 0)
blue = (0, 0, 180)
red = (255,   0,   0)

fontP = pygame.font.Font('freesansbold.ttf', 32)
textX3 = 930/2 - 100
textY3 = 630/2-100

fontUP = pygame.font.Font('freesansbold.ttf', 32)
textX4 = 930/2 - 190
textY4 = 630/3 + 100

def paused():
    loop = 1
    pause = fontP.render("Paused", True, black, white)
    screen.blit(pause, (textX3, textY3))
    unpause = fontUP.render("Press P to continue", True, black, white)
    screen.blit(unpause, (textX4, textY4))
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    loop = 0
                if event.key == pygame.K_p:
                    screen.fill((0, 0, 0))
                    loop = 0
        pygame.display.update()
        clock.tick(60)

# Walls
w_group = pygame.sprite.Group()

#先求出wall的每行每列能放多少个
wx = G.S_width // G.W_width
wy = G.S_height // G.W_height
#画墙
for i in range (0 , wx):
    w_top1 = wall()
    w_top1.rect.x = i * G.W_width
    w_top1.rect.y = 0
    w_group.add(w_top1)
    w_bot1 = wall()
    w_bot1.rect.x = i * G.W_width
    w_bot1.rect.y = G.S_height - G.W_height
    w_group.add(w_bot1)


for i in range (0 , wy):
    w_top2 = wall()
    w_top2.rect.x = 0
    w_top2.rect.y = i * G.W_height
    w_group.add(w_top2)
    w_bot2 = wall()
    w_bot2.rect.x = G.S_width - G.W_width
    w_bot2.rect.y = i * G.W_height
    w_group.add(w_bot2)
    

# Music
music = pygame.mixer.Sound('music.mp3')
music.set_volume(0.1)
music.play(3)

# Game loop
start_menu()
while True:

    G.c_group.empty()   #coin group
    G.r_group.empty()   #role group
    G.br_group.empty()  #bullet group
    G.o_group.empty()   #barrier group
    G.e_group.empty()
    G.a_group.empty()
    G.x_group.empty()
    G.m_group.empty()


    G.O_number= 5*count
    G.A_number = 2*count
    G.E_number = 1*count
    G.X_number = 2*count
    G.M_number = 2*count


    r=role()  #role sprite
    G.r_group.add(r)

    #为了避免重叠，用了几个冲突判定

    for i in range (0,G.O_number):
        Create_O()

    #和上面一样

    for i in range(0,G.C_number):
        Create_coin()

    for i in range(0,G.A_number):
        Create_armor()

    for i in range(0,G.X_number):
        Create_bloodbox()

    for i in range(0,G.M_number):
        Create_caisson()

    for i in range(0,G.E_number):
        Create_enemy()

    nx = r.rect.x
    ny = r.rect.y
    while True:
        for event in pygame.event.get():
            nx = r.rect.x
            ny = r.rect.y

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p:
                    paused()
                if event.key == pygame.K_w:  # 如果按下是向上键w
                    r.row =0  #第3行向上
                    r.y = -2
                    r.co=1
                    r.snd.set_volume(0.1)
                    r.snd.play(100)
                if event.key == pygame.K_a:  # 如果按下是向左键
                    r.row =1   #第1行向左
                    r.x = -2
                    r.co = 1
                    r.snd.set_volume(0.1)
                    r.snd.play(100)
                if event.key == pygame.K_s:  # 如果按下是向下键
                    r.row = 2  #第0行向下
                    r.y = 2
                    r.co = 1
                    r.snd.set_volume(0.1)
                    r.snd.play(100)
                if event.key == pygame.K_d:  # 如果按下是向右键
                    r.row = 3  #第2行向右
                    r.x = 2
                    r.co = 1
                    r.snd.set_volume(0.1)
                    r.snd.play(100)
                if event.key == pygame.K_f:
                    if r.flash > 0:
                        snd = pygame.mixer.Sound('flash.wav')
                        snd.set_volume(0.2)
                        snd.play()
                        if r.row == 0:
                            if r.rect.y > 100:
                                r.rect.y -= 100

                        if r.row == 1:
                            if r.rect.x > 100:
                                r.rect.x -= 100

                        if r.row == 2:
                            if r.rect.y < 530:
                                r.rect.y += 100

                        if r.row == 3:
                            if r.rect.x < 830:
                                r.rect.x += 100

                        r.flash -= 1

                if event.key == pygame.K_j: #按j射击
                    if r.bn > 0:
                        br = bullet_role()
                        snd = pygame.mixer.Sound('eshoot.wav')
                        snd.set_volume(0.3)
                        snd.play()
                        if r.row == 0: #朝上射
                            br.rect.x = r.rect.x  + r.frame_width//2 - br.frame_width//2
                            br.rect.y = r.rect.y - br.frame_height 
                            br.x = 0
                            br.y = -5
                        if r.row == 1: #朝左射
                            br.rect.x = r.rect.x - br.frame_width 
                            br.rect.y = r.rect.y + r.frame_height//2 - br.frame_height//2
                            br.x = -5
                            br.y = 0
                        if r.row == 2: #朝下射
                            br.rect.x = r.rect.x + r.frame_width//2 - br.frame_width//2
                            br.rect.y = r.rect.y + r.frame_height 
                            br.x = 0
                            br.y = 5
                        if r.row == 3: #朝右射
                            br.rect.x = r.rect.x + r.frame_width
                            br.rect.y = r.rect.y + r.frame_height//2 - br.frame_height//2
                            br.x = 5
                            br.y = 0
                        G.br_group.add(br)
                        r.bn -= 1
                        

            elif event.type == pygame.KEYUP:  # 如果有键盘释放
                if event.key == pygame.K_w:  # 如果释放的是向上键
                    r.y=0
                    r.co = 0
                    r.snd.stop()
                if event.key == pygame.K_a:  # 如果释放的是向左键
                    r.x=0
                    r.co = 0
                    r.snd.stop()
                if event.key == pygame.K_s:  # 如果释放的是向下键
                    r.y = 0
                    r.co = 0
                    r.snd.stop()
                if event.key == pygame.K_d:  # 如果释放的是向右键
                    r.x = 0
                    r.co = 0
                    r.snd.stop()
                if event.key == pygame.K_f:
                    if r.row == 0:
                        r.y = 0
                        r.flash -=1
                    if r.row == 1:
                        r.x = 0
                        r.flash -=1
                    if r.row == 2:
                        r.y = 0
                        r.flash -=1
                    if r.row == 3:
                        r.x =0
                        r.flash -=1

                    
                
     

        E_E = pygame.sprite.groupcollide(G.e_group, G.e_group, False, False)
        if E_E:
            for keys in E_E.keys():
                if len(E_E[keys]) >1:
                    keys.rect.x = keys.prex
                    keys.rect.y = keys.prey

        E_R = pygame.sprite.groupcollide(G.e_group, G.r_group, False, False)
        if E_R:
            for keys in E_R.keys():
                
                keys.rect.x = keys.prex
                keys.rect.y = keys.prey

            if r.armor >= 0:
                r.armor -= G.onehit
            else:
                r.health -= G.onehit
            
        E_O = pygame.sprite.groupcollide(G.e_group, G.o_group, False, False)
        if E_O:
            for keys in E_O.keys():
                
                keys.rect.x = keys.prex
                keys.rect.y = keys.prey


        E_W = pygame.sprite.groupcollide(G.e_group, w_group, False, False)
        if E_W:
            for keys in E_W.keys():
                
                keys.rect.x = keys.prex
                keys.rect.y = keys.prey


        R_E = pygame.sprite.groupcollide(G.r_group, G.e_group, False, False)

        if R_E:
            for keys in R_E.keys():
            
                keys.rect.x = keys.prex
                keys.rect.y = keys.prey

            if r.armor >= 0:
                r.armor -= G.onehit
            else:
                r.health -= G.onehit


        R_C = pygame.sprite.spritecollide(r, G.c_group, True, pygame.sprite.collide_mask)#人和coin的collision
        if R_C:
            snd = pygame.mixer.Sound('coin.wav')
            snd.set_volume(0.3)
            snd.play()
            r.gold +=1
            r.point = r.gold * G.gold_point
            if len(G.c_group)< 5:
                for i in range (0,len(G.c_group)):
                    Create_coin()


        R_M = pygame.sprite.spritecollide(r, G.m_group, True, pygame.sprite.collide_mask)
        if R_M:
            r.bn += G.upbullet
            snd = pygame.mixer.Sound('ammo.wav')
            snd.set_volume(0.3)
            snd.play()

        R_A = pygame.sprite.spritecollide(r, G.a_group, True, pygame.sprite.collide_mask)
        if R_A:
            r.armor += G.oarmor
            snd = pygame.mixer.Sound('armor.wav')
            snd.set_volume(0.3)
            snd.play()
            if r.armor > G.Maxarmor:
                r.armor = G.Maxarmor


        R_X = pygame.sprite.spritecollide(r, G.x_group, True, pygame.sprite.collide_mask)
        if R_X:
            r.health += G.ohealth
            snd = pygame.mixer.Sound('health.wav')
            snd.set_volume(0.3)
            snd.play()
            if r.health > G.Maxhealth:
                r.health = G.Maxhealth
            
            
        R_O = pygame.sprite.spritecollide(r, G.o_group, False, pygame.sprite.collide_mask) #人和barrier的collision ,如果人撞到障碍物，回到之前的位置就是前面的(r.rect.prex, r.rect.prey)
        if R_O:
            r.rect.x = r.prex
            r.rect.y = r.prey

        R_W = pygame.sprite.spritecollide(r, w_group, False, pygame.sprite.collide_mask)#人和wall的collision
        if R_W:
            r.rect.x = r.prex
            r.rect.y = r.prey

        Br_O = pygame.sprite.groupcollide(G.br_group,G.o_group,True,False)#bullet和barrier的collision
        if Br_O:
            snd = pygame.mixer.Sound('hit.wav')
            snd.set_volume(0.3)
            snd.play()

        Br_W = pygame.sprite.groupcollide(G.br_group,w_group,True,False)#bullet和wall的collision
        if Br_W:
            snd = pygame.mixer.Sound('hit.wav')
            snd.set_volume(0.3)
            snd.play()

        Br_E = pygame.sprite.groupcollide(G.br_group,G.e_group,True,False)
        if Br_E:
            snd = pygame.mixer.Sound('ehit.wav')
            snd.set_volume(0.2)
            snd.play()
            for value in Br_E.values():
                for i in value:
                    i.health -= G.onershoot
                    if i.health < G.onershoot:
                        G.e_group.remove(i)
                        Create_enemy()



        Be_O = pygame.sprite.groupcollide(G.be_group,G.o_group,True,False)#bullet和barrier的collision

        Be_W = pygame.sprite.groupcollide(G.be_group,w_group,True,False)#bullet和wall的collision
        if Be_W:
            snd = pygame.mixer.Sound('hit.wav')
            snd.set_volume(0.3)
            snd.play()

        Be_R = pygame.sprite.groupcollide(G.be_group,G.r_group,True,False)
        if Be_R:
            snd = pygame.mixer.Sound('rhit.wav')
            snd.set_volume(0.3)
            snd.play()
            if r.armor >= 0:
                r.armor -= G.oneshoot
            else:
                r.health -= G.oneshoot

        screen.fill((255, 255, 255))
        bg = pygame.image.load("bg" + str(count2) + ".png")
        screen.blit(bg, (0, 0))
        ui = pygame.image.load('头像.png')
        screen.blit(ui,(0,630))
        blood = pygame.image.load('血量.jpg')
        screen.blit(blood,(100,630))
        armor = pygame.image.load('护甲.png')
        screen.blit(armor,(100,680))


        pygame.draw.rect(screen, (255,0,0,180), Rect(150,640,r.health,30))
        pygame.draw.rect(screen, (255,0,0,180), Rect(150,640,G.Maxhealth,30), 2)
                                                             

        pygame.draw.rect(screen, (0,0,255,180), Rect(150,690,r.armor,30))
        pygame.draw.rect(screen, (0,0,255,180), Rect(150,690,G.Maxarmor,30), 2)


        font1 = pygame.font.SysFont('Arial', 16)

        bulletsurface = font1.render('Bullet Number × %d'%r.bn, True, [0, 0, 0])

        screen.blit(bulletsurface, (540,690))


        pointsurface = font1.render(' Point : %d'%r.point, True, [0, 0, 0])

        screen.blit(pointsurface , (740,690))

        G.r_group.update()  # 执行更新函数
        G.br_group.update()
        G.be_group.update()
        G.e_group.update(nx,ny)
        G.a_group.draw(screen)
        G.x_group.draw(screen)
        G.c_group.draw(screen)
        G.m_group.draw(screen)
        G.r_group.draw(screen)
        G.br_group.draw(screen)
        G.be_group.draw(screen)
        G.o_group.draw(screen)
        w_group.draw(screen)
        G.e_group.draw(screen)

        for e in G.e_group:
            pygame.draw.rect(screen, (255,0,0,180), Rect(e.rect.x,e.rect.y,e.health,4))
            pygame.draw.rect(screen, (255,0,0,180), Rect(e.rect.x,e.rect.y,G.Ehealth,4), 1)


        clock.tick(60)#帧数
        pygame.display.update()
        if r.point >= 2000*count:
            break
        if r.health <= 0:
            break
    if r.health <= 0:
        break

    r.snd.stop()
    count += 1
    count2 += 1
    score += r.point
    if count2 > 4:
        count2 = 1

r.snd.stop()
end_screen()