import pygame
import neat


class Bird:
    def __init__(self, x, y, genome, config):
        self.x = x
        self.y = y
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.velocity = 0
        self.angle = 0
        self.image = pygame.transform.scale(pygame.image.load('images/flappybird.png'), (60, 55))
        genome.fitness = 0

    def jump(self):
        self.angle = 70
        self.velocity = -1.5

    def move(self, pipe):
        output = self.net.activate([self.y, pipe.bottom, (pipe.x - self.x), (pipe.bottom - self.y), self.angle])
        if output[0] > 0.5:
            self.jump()

        self.y += self.velocity
        self.velocity += 0.01
        if self.angle > -75:
            self.angle -= 0.3

        self.genome.fitness += 0.1

    def draw(self, window):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)

        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def die(self):
        self.genome.fitness -= 1