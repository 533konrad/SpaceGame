#https://www.youtube.com/watch?v=jO6qQDNa2UY
# 29:00

import pygame

#drukowane, bo to stałe wartości
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

TLO = (255,255,255)

FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40

YELLOW_SPACESHIP_IMAGE = pygame.image.load('spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load('spaceship_red.png')
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),270)
SPACE_IMAGE = pygame.image.load('space.png')

pygame.display.set_caption("Pierwsza gra!")

def draw_window():
    WIN.fill(TLO)
    WIN.blit(YELLOW_SPACESHIP, (100,200))
    WIN.blit(RED_SPACESHIP, (800,200))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()