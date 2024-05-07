import pygame
import random
class Pipe():
    GAP = 180
    VEL = 1

    def __init__(self, x):
        self.x = x
        self.height = 0

        # position en y du tuyau haut et bas
        self.top = 0
        self.bottom = 0

        self.pipe_img = pygame.transform.scale(pygame.image.load("images/pipe.png"), (100, 700))

        self.PIPE_TOP = pygame.transform.flip(self.pipe_img, False, True)
        self.PIPE_BOTTOM = self.pipe_img

        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = random.randrange(150, self.PIPE_TOP.get_height()- 250)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.top + self.PIPE_TOP.get_height() + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False