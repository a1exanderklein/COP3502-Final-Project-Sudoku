import pygame
import sys
from constants import *
import os

pygame.init()
pygame.display.set_caption("Sudoku")
numberFont = pygame.font.Font(None, )
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 600 px by 650 px screen
screen.fill(BG_COLOR)

# font = pygame.font.SysFont("", )
easy_image = pygame.image.load("Button_Easy.png").convert_alpha()
medium_image = pygame.image.load("Button_Medium.png").convert_alpha()
hard_image = pygame.image.load("Button_Hard.png").convert_alpha()
background = pygame.image.load("Button_Background.png").convert_alpha()
restart_image = pygame.image.load(os.path.join('Assets', 'restart.png'))
exit_image = pygame.image.load(os.path.join('Assets', 'exit.png'))
exit_small_image = pygame.image.load(os.path.join('Assets', 'exit_small.png'))
restart_small_image = pygame.image.load(os.path.join('Assets', 'restart_small.png'))
reset_image = pygame.image.load(os.path.join('Assets', 'reset.png'))
class Button:
    def __init__(self, image, position):
        self.image = image
        self.rect = image.get_rect(topleft=position)


    def when_clicked(self):
        pass