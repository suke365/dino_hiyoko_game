import pyxel
import math
import random

class App:
    def __init__(self):
        pyxel.init(256, 256,title="hiyoko_kyoryu", fps=60,quit_key=pyxel.KEY_Q)
        pyxel.load("my_resource.pyxres")
        self.score=0
        self.anispe=0
        self.is_arrive=True
        self.hiyoko_states=0
        self.hiyoko_x = 100
        self.hiyoko_y=140
        self.cloud_x=256
        self.tree_hight1=0
        self.tree_hight2=16
        self.tree_x=256
        self.tree_y=184
        self.tree_speed=2
        self.crow_x=256
        self.crow_y=60
        self.crow_y_bottom=self.crow_y+14
        self.crow_speed=1
        self.crow_num=1
        self.crow_second=False
        self.crow_third=False
        self.gravity=3
        pyxel.run(self.update, self.draw)

    def update(self):
        self.update_score()
        self.update_tree()
        self.update_crow()
        self.update_hiyoko()
        self.update_cloud()
        
    def update_score(self):
        if pyxel.frame_count % 10==0 and self.is_arrive:
            self.score+=1

    def update_hiyoko(self):
        #self.gravity += pyxel.frame_count/2000
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.is_arrive:
            self.hiyoko_states=16
            self.hiyoko_y = max(self.hiyoko_y-2,2)
            #self.gravity = 1       
        elif not self.is_arrive :
            self.hiyoko_states=32
            self.hiyoko_y=self.hiyoko_y
            self.is_arrive=False    
        elif self.hiyoko_y<=184 and self.is_arrive:
            self.hiyoko_states=0
            self.hiyoko_y = min(self.hiyoko_y+self.gravity,184)

    def update_cloud(self):
        self.cloud_x= self.cloud_x-0.1
        if self.cloud_x<=-32:
            self.cloud_x=256
    def update_tree(self):
        self.tree_x=self.tree_x - self.tree_speed
        if self.tree_x<=-32:
            self.tree_x=256
            self.tree_hight1=random.randrange(0,33,16)
            if self.tree_hight1==0:
                self.tree_hight2=16
                self.tree_y=184
            elif self.tree_hight1==16:
                self.tree_hight2=24
                self.tree_y=176
            else:
                self.tree_hight2=32
                self.tree_y=168

    def update_crow(self):
        self.crow_x = self.crow_x-self.crow_speed
        if self.crow_x<=-32:
            self.crow_x=256
            #self.crow_y=random.randrange(140)
            self.crow_y=self.hiyoko_y
            self.crow_y_bottom=self.crow_y+14
            if self.crow_second:
                if self.crow_y>=148:
                    self.crow_y-=40
                self.crow_y_bottom=self.crow_y+34
                if self.crow_third:
                    if self.crow_y>=148:
                        self.crow_y-=111
                    self.crow_y_bottom=self.crow_y+54
        elif self.crow_x<=-16 and self.score > 100 :
            self.crow_speed=2
            self.tree_speed=3
            self.crow_second=True
            if self.crow_x<=-16 and self.score > 300 :
                self.crow_speed=3
                self.tree_speed=4
                self.crow_third=True
                if self.crow_x<=-16 and self.score > 500 :
                    self.crow_speed=4
                    self.tree_speed=5

    def draw(self):
        pyxel.cls(6)
        pyxel.rect(0,200,256,100,4)
        pyxel.text(200,10,"score="+str(self.score),0) 

        #雲配置
        pyxel.blt(self.cloud_x, 20, 0, 0, 64, 32, 16)
        pyxel.blt(self.cloud_x+32, 60, 0, 0, 64, 32, 16)

        #木の配置
        pyxel.blt(self.tree_x, self.tree_y,0, self.tree_hight1, 80, 16, self.tree_hight2,6)  

        #カラス配置
        pyxel.blt(self.crow_x, self.crow_y, 0, 16 * self.anispe, 112, 16, 16,6)
        #pyxel.blt(self.crow_x, self.crow_y+20, 0, 16 * self.anispe, 112, 16, 16,6)
        #pyxel.blt(self.crow_x, self.crow_y+40, 0, 16 * self.anispe, 112, 16, 16,6)
        if self.crow_second:
            pyxel.blt(self.crow_x, self.crow_y+20, 0, 16 * self.anispe, 112, 16, 16,6)
        if self.crow_third:
            pyxel.blt(self.crow_x, self.crow_y+40, 0, 16 * self.anispe, 112, 16, 16,6)
        #ひよこ配置
        if pyxel.frame_count % 20==0:
            if pyxel.frame_count / 20 % 2==1:
                self.anispe=1
            elif pyxel.frame_count / 20 % 2==0:
                self.anispe=0
        pyxel.blt(self.hiyoko_x, self.hiyoko_y, 0, 16 * self.anispe, self.hiyoko_states, 16, 16, 6)
        #あたり判定
        #pyxel.line(self.hiyoko_x+8, self.hiyoko_y+8, self.tree_x, self.tree_y, 7)#テスト用ライン
        #pyxel.line(self.hiyoko_x+8, self.hiyoko_y+8, self.tree_x+16, self.tree_y+self.tree_hight2, 7)#テスト用ライン
        #pyxel.line(self.hiyoko_x+8, self.hiyoko_y+8, self.crow_x, self.crow_y, 7)#テスト用ライン       
        #pyxel.line(self.hiyoko_x+8, self.hiyoko_y+8, self.crow_x+16, self.crow_y_bottom, 7)#テスト用ライン
        #木のあたり判定
        if self.hiyoko_x+10<self.tree_x or self.hiyoko_x>self.tree_x+14 or self.hiyoko_y+8<self.tree_y:
            pass
        else:
            self.is_arrive=False
            #pyxel.text(0, 32, "HIT_tree", 7)
        #カラスのあたり判定
        if (self.hiyoko_x+8<self.crow_x or 
            self.hiyoko_x>self.crow_x+14 or 
            self.hiyoko_y+8<= self.crow_y or
            self.hiyoko_y>= self.crow_y_bottom         
            ):
            pass
        else:
            self.is_arrive=False
            #pyxel.text(0, 32, "HIT_crow", 7)
        if not self.is_arrive:
            pyxel.text(124, 124, """GAME OVER
click to RESTART!!!""" ,0)
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.score=0
                self.is_arrive=True
                self.hiyoko_x = 100
                self.hiyoko_y=140
                self.tree_hight1=0
                self.tree_hight2=16
                self.tree_x=256
                self.tree_y=184
                self.tree_speed=2
                self.crow_x=256
                self.crow_y=60
                self.crow_y_bottom=self.crow_y+14
                self.crow_speed=1
                self.crow_second=False
                self.crow_third=False



App()