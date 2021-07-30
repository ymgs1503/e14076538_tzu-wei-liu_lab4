import pygame
from enemy import EnemyGroup
from tower import TowerGroup

import os
from settings import WIN_WIDTH, WIN_HEIGHT, FPS

# initialization
pygame.init()
# load image
BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "Map.png"))
HP_IMAGE = pygame.image.load(os.path.join("images", "hp.png"))
HP_GRAY_IMAGE = pygame.image.load(os.path.join("images", "hp_gray.png"))
# set the title and icon
pygame.display.set_caption("My TD game")


class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.bg_image = pygame.transform.scale(BACKGROUND_IMAGE, (WIN_WIDTH, WIN_HEIGHT))
        self.hp_images = [pygame.transform.scale(HP_IMAGE, (40, 40)),
                          pygame.transform.scale(HP_GRAY_IMAGE, (40, 40))]
        self.enemies = EnemyGroup()
        self.towers = TowerGroup()
        self.base = pygame.Rect(430, 90, 195, 130)

    @staticmethod
    def select(group, x, y):
        """
        Bonus) If the item is clicked. change the state of whether the tower is selected. (( tower.is_clicked(), tower.get_selected()
        :param group: Group()
        :param x: mouse pos x
        :param y: mouse pos y
        :return: None
        """

        """
        Hint:
        for each object in group list, do
        if the item is clicked, then
            the item is selected.
        else, 
            the item is not selected.
        end if
        end for
        """
        pass

    def collide_base(self, enemy):
        """
        Return True if the enemy collide with base.
        :param enemy: class Enemy()
        :return: Bool
        """
        en_x, en_y = enemy.get_pos()
        x, y = self.base.center
        width, height = self.base.w, self.base.h
        if x - width//2 < en_x < x + width//2 and y - height//2 < en_y < y + height//2:
            return True
        return False

    def draw(self):
        """
        Draw everything in this method.
        :return: None
        """
        # draw background
        self.win.blit(self.bg_image, (0, 0))
        # draw enemy
        for en in self.enemies.get():
            en.draw(self.win)
        # draw tower
        for tw in self.towers.get():
            tw.draw(self.win)

    def game_run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            # event loop
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False  # quit game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n and self.enemies.is_empty():
                        self.enemies.add(5)  # 5 enemy is ready for the next wave
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.select(self.towers, x, y)

            # tower loop
            for tw in self.towers.get():
                tw.attack(self.enemies)

            # enemy loop
            self.enemies.campaign() # let the enemy go on an expidition
            for en in self.enemies.get():
                en.move()
                if en.died():
                    self.enemies.retreat(en)
                # delete the object when it reach the base
                if self.collide_base(en):
                    self.enemies.retreat(en)

            # draw everything
            self.draw()
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    covid_game = Game()
    covid_game.game_run()