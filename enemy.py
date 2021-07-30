import pygame
import math
import os
from settings import *

pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))


class Enemy:
    def __init__(self):
        self.path = PATH
        self.path_index = 0
        self.move_count = 0
        self.stride = 1
        self.image = pygame.transform.scale(ENEMY_IMAGE, (40, 50))
        self.rect = self.image.get_rect()
        self.rect.center = self.path[self.path_index]
        self.health = 10
        self.max_health = 10
        self.path_index = 0
        self.move_count = 0
        self.stride = 1

    def draw(self, win):
        win.blit(self.image, self.rect)
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        bar_width = self.rect.w * (self.health / self.max_health)
        max_bar_width = self.rect.w
        bar_height = 5
        pygame.draw.rect(win, RED, [self.rect.x, self.rect.y - 10, max_bar_width, bar_height])
        pygame.draw.rect(win, GREEN, [self.rect.x, self.rect.y - 10, bar_width, bar_height])

    def move(self):
        x1, y1 = self.path[self.path_index]
        x2, y2 = self.path[self.path_index + 1]
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        max_count = int(distance / self.stride)
        # compute the unit vector
        unit_vector_x = (x2 - x1) / distance
        unit_vector_y = (y2 - y1) / distance
        # compute the movement
        delta_x = unit_vector_x * self.stride * self.move_count
        delta_y = unit_vector_y * self.stride * self.move_count
        # update the position and counter
        if self.move_count <= max_count:
            self.rect.centerx = x1 + delta_x
            self.rect.centery = y1 + delta_y
            self.move_count += 1
        else:
            self.move_count = 0
            self.path_index += 1
            self.rect.center = self.path[self.path_index]

    def get_pos(self):
        return self.rect.center

    def get_hurt(self, damage):
        self.health -= damage

    def died(self):
        if self.health <= 0:
            return True
        return False


class EnemyGroup:
    def __init__(self):
        self.campaign_count = 0
        self.campaign_max_count = 60   # (unit: frame)
        self.reserved_members = []
        self.expedition = []

    def campaign(self):
        """
        Enemy go on an expedition.
        :return: None
        """
        if self.campaign_count > self.campaign_max_count and self.reserved_members:
            self.expedition.append(self.reserved_members.pop())
            self.campaign_count = 0
        else:
            self.campaign_count += 1

    def add(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        self.reserved_members = [Enemy() for n in range(num)]

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)