import pygame
import os
import math
import enemy

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """


        """
        Hint:
        x1, y1 = enemy.get_pos()
        ...
        """
        en_x, en_y = enemy.get_pos()      #enemy座標
        x, y = self.center                #塔的中央座標
        distance = math.sqrt((en_x - x)**2 + (en_y - y)** 2)  #計算兩者間距離
        if distance < self.radius:                            #距離小於半徑，表示進入攻擊範圍
            return True
        return False
        

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        transparent_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)   #先設定一個有透明度的surface
        transparency = 50       #設定透明度
        pygame.draw.circle(transparent_surface, (255, 255, 255, transparency), (self.radius, self.radius), self.radius)  #在有透明度的surface上畫圓
        x, y = self.center  #圓的中心座標
        win.blit(transparent_surface, (x - self.radius, y - self.radius))     #將有透明度的surface放到win上面，xy座標分別剪掉半徑(因為是對準左上角)


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = False  # the state of whether the tower is selected
        self.type = "tower"
        self.attack_list = []

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """

        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """
        if self.cd_count < self.cd_max_count:     #設定計數器，不到一輪(60 frames)的時候就加一，並回傳False表示尚未冷卻
            self.cd_count += 1
            return False
        else:                                     #滿一輪(60 frames)將計數器歸零重計，並回傳True表示已冷卻完成
            self.cd_count = 0
            return True

    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        enemy_group = enemy_group.get()     #取出在場上的enemy
        self.attack_list = []               #每次都先把要攻擊的list清空
        for en_count in enemy_group:        #判斷場上的enemy有沒有在塔的攻擊範圍中，若進入攻擊範圍，則將enemy放入該塔要攻擊的list中
            if self.range_circle.collide(en_count):
                self.attack_list.append(en_count)
        if self.is_cool_down():                             #當塔完成冷卻
            for i in range (len(self.attack_list)):  
                self.attack_list[i].get_hurt(self.damage)   #攻擊在attack list中的第一個enemy(範圍中第一個enemy)
                break                                       #只攻擊第一個，所以執行後就break

    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        tower_x, tower_y = self.rect.center                         #取得塔的中心位置
        distance = math.sqrt((x - tower_x)**2 + (y - tower_y)**2)   #計算塔與滑鼠游標之間距離
        if distance < 50:     #若距離小於50則在塔的上方(塔的長寬為70，故從中心至邊上為70/2=35，中心至頂點為35*sqrt(2)=50)
            return True       #回傳True
        else:                 #距離大於50表示沒有點到塔，回傳False
            return False

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected        #將引述的布林值指派給self.is_selected，改變該塔的狀態

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

