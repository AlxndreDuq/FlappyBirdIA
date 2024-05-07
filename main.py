import sys

import neat
import pygame
import os
from Bird import *
from Pipe import *


pygame.init()
gen = 0
STAT_FONT = pygame.font.SysFont("Arial", 50)
END_FONT = pygame.font.SysFont("Arial", 50)
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption('Flappy Bird IA')
pygame.display.set_icon(pygame.image.load('images/flappybird.png'))
pygame.time.Clock().tick(60)


def draw_window(win, birds, pipes, score, generation, pipe_ind):

    if generation == 0:
        generation = 1

    for pipe in pipes:
        pipe.draw(win)

    for bird in birds:
        pygame.draw.line(screen, (255, 0, 0), (bird.x + bird.image.get_width() / 2, bird.y + bird.image.get_height() / 2), (pipes[pipe_ind].x, pipes[pipe_ind].bottom), 2)
        bird.draw(win)

    # score
    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (600 - score_label.get_width() - 15, 10))

    # generations
    score_label = STAT_FONT.render("Gens: " + str(generation - 1), 1, (255, 255, 255))
    win.blit(score_label, (10, 10))

    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
    win.blit(score_label, (10, 50))



    pygame.display.update()


def run(genomes, config):
    global gen

    gen += 1

    birds = []
    for genome_id, genome in genomes:
        birds.append(Bird(230, 350, genome, config))

    pipes = [Pipe(700)]
    score = 0

    running = True
    while running and len(birds) > 0:
        screen.fill((119, 181, 254))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        for bird in birds:
            bird.move(pipes[pipe_ind])

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # Verifier les collisions
            for bird in birds:
                if pipe.collide(bird, screen):
                    bird.die()
                    birds.pop(birds.index(bird))

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        for r in rem:
            pipe_ind = 0
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.image.get_height() - 10 >= 900 or bird.y < -100:
                bird.die()
                birds.pop(birds.index(bird))

        draw_window(screen, birds, pipes, score, generation=gen, pipe_ind=pipe_ind)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config-feedforward.txt')

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Créer la population
    p = neat.Population(config)


    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run
    winner = p.run(run, None)

    # stats final
    print('\nBest genome:\n{!s}'.format(winner))
