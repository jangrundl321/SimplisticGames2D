import sys

import numpy as np
import pygame

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREY = (211, 211, 211)
RED = (255, 0, 0)

WINDOW_HEIGHT = 400
WINDOW_WIDTH = WINDOW_HEIGHT
BLOCK_SIZE = 40
REFRESH_TIME = 10
ARRAY_SIZE = WINDOW_HEIGHT // BLOCK_SIZE

NUMBER_OF_MINES = 10
TRACKING_GRID = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH))

MINE = 10


def moore_neighborhood(grid, row, col):
    neighborhood = []
    for x, y in (
            (row - 1, col), (row + 1, col), (row, col - 1),
            (row, col + 1), (row - 1, col - 1), (row - 1, col + 1),
            (row + 1, col - 1), (row + 1, col + 1)):
        if not (0 <= x < len(grid) and 0 <= y < len(grid[x])):
            # out of bounds
            continue
        else:
            neighborhood.append((x, y))
    return neighborhood


def generate_grid():
    grid = np.zeros((ARRAY_SIZE, ARRAY_SIZE))

    if NUMBER_OF_MINES > 0:
        for i in range(NUMBER_OF_MINES):
            random_col = np.random.randint(0, ARRAY_SIZE)
            random_row = np.random.randint(0, ARRAY_SIZE)

            grid[random_col, random_row] = MINE

    for col in range(ARRAY_SIZE):
        for row in range(ARRAY_SIZE):
            if grid[col, row] == MINE:
                continue
            else:
                neighbors = moore_neighborhood(grid, col, row)

                k = 0
                for n in neighbors:
                    if grid[n] == MINE:
                        k += 1

                grid[col, row] = k

    return grid


def checkWinningCondition(grid):
    won = True

    for col in range(ARRAY_SIZE):
        for row in range(ARRAY_SIZE):
            if not grid[col, row] == MINE and TRACKING_GRID[col, row] == 0:
                won = False

    return won


def draw(grid, screen):
    grid_used_for_drawing = grid
    rects = []

    for x_window in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y_window in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x_window, y_window, BLOCK_SIZE, BLOCK_SIZE)
            rects.append(rect)
            x_grid = x_window // BLOCK_SIZE
            y_grid = y_window // BLOCK_SIZE

            if TRACKING_GRID[x_grid, y_grid] == 0:
                pygame.draw.rect(screen, GREY, rect, 1)
            else:
                if grid_used_for_drawing[x_grid, y_grid] < 10:
                    pygame.draw.rect(screen, WHITE, rect, 0)

                    my_font = pygame.font.SysFont(None, 50)
                    text_surface = my_font.render(str(int(grid_used_for_drawing[x_grid, y_grid])), False,
                                                  (200, 200, 200), BLACK)
                    screen.blit(text_surface, [x_window, y_window])
                elif grid_used_for_drawing[x_grid, y_grid] == 10:
                    pygame.draw.rect(screen, RED, rect, 0)
                else:
                    pygame.draw.rect(screen, WHITE, rect, 0)

    return rects


def run():
    global TRACKING_GRID, NUMBER_OF_MINES
    grid = generate_grid()
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("MineSweeper")
    CLOCK = pygame.time.Clock
    hitMine = False

    while True:
        SCREEN.fill(BLACK)
        pygame.time.wait(REFRESH_TIME)
        rects = draw(grid, SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for rect in rects:
                        if rect.collidepoint(event.pos):
                            TRACKING_GRID[rect.x // BLOCK_SIZE, rect.y // BLOCK_SIZE] = 1
                            if grid[rect.x // BLOCK_SIZE, rect.y // BLOCK_SIZE] == 10:
                                hitMine = True
        if hitMine:
            hitMine = False
            draw(grid, SCREEN)
            pygame.display.update()
            pygame.time.wait(1000)
            TRACKING_GRID = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH))
            grid = generate_grid()

        if checkWinningCondition(grid):
            draw(grid, SCREEN)
            pygame.display.update()
            pygame.time.wait(1000)
            NUMBER_OF_MINES += 1
            TRACKING_GRID = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH))
            grid = generate_grid()

        pygame.display.update()


run()
