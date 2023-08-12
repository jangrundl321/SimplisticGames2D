import sys

import numpy as np
import pygame

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WINDOW_HEIGHT = 120
WINDOW_WIDTH = WINDOW_HEIGHT
BLOCK_SIZE = 40
REFRESH_TIME = 10
ARRAY_SIZE = WINDOW_HEIGHT // BLOCK_SIZE

NUMBER_OF_MINES = 10
TRACKING_GRID = np.zeros((ARRAY_SIZE, ARRAY_SIZE))

MINE = 10
PLAYER1 = 1
PLAYER2 = 2

TURN = 0


def checkWinningCondition(grid):
    won = False

    if (grid[0, 0] == grid[0, 1] == grid[0, 2] == PLAYER1
            or grid[1, 0] == grid[1, 1] == grid[1, 2] == PLAYER1
            or grid[2, 0] == grid[2, 1] == grid[2, 2] == PLAYER1

            or grid[0, 0] == grid[1, 0] == grid[2, 0] == PLAYER1
            or grid[1, 0] == grid[1, 1] == grid[2, 1] == PLAYER1
            or grid[0, 2] == grid[1, 2] == grid[2, 2] == PLAYER1

            or grid[0, 0] == grid[1, 1] == grid[2, 2] == PLAYER1
            or grid[0, 2] == grid[1, 1] == grid[2, 0] == PLAYER1):
        print("Player 1 won")
        won = True
    if (grid[0, 0] == grid[0, 1] == grid[0, 2] == PLAYER2
            or grid[1, 0] == grid[1, 1] == grid[1, 2] == PLAYER2
            or grid[2, 0] == grid[2, 1] == grid[2, 2] == PLAYER2

            or grid[0, 0] == grid[1, 0] == grid[2, 0] == PLAYER2
            or grid[1, 0] == grid[1, 1] == grid[2, 1] == PLAYER2
            or grid[0, 2] == grid[1, 2] == grid[2, 2] == PLAYER2

            or grid[0, 0] == grid[1, 1] == grid[2, 2] == PLAYER2
            or grid[0, 2] == grid[1, 1] == grid[2, 0] == PLAYER2):
        print("Player 2 won")
        won = True
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
                pygame.draw.rect(screen, WHITE, rect, 1)
            else:
                if grid_used_for_drawing[x_grid, y_grid] == PLAYER1:
                    pygame.draw.rect(screen, RED, rect, 0)
                elif grid_used_for_drawing[x_grid, y_grid] == PLAYER2:
                    pygame.draw.rect(screen, BLUE, rect, 0)
    return rects


def checkStalemate(grid):
    for col in range(ARRAY_SIZE):
        for row in range(ARRAY_SIZE):
            if grid[col, row] == 0:
                return False

    return True


def run():
    global TRACKING_GRID, TURN
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("TicTacToe")
    CLOCK = pygame.time.Clock

    while True:
        SCREEN.fill(BLACK)
        pygame.time.wait(REFRESH_TIME)
        rects = draw(TRACKING_GRID, SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for rect in rects:
                        if rect.collidepoint(event.pos):
                            if TURN % 2 == 0 and TRACKING_GRID[rect.x // BLOCK_SIZE, rect.y // BLOCK_SIZE] == 0:
                                TRACKING_GRID[rect.x // BLOCK_SIZE, rect.y // BLOCK_SIZE] = PLAYER1
                                TURN += 1
                            if TURN % 2 == 1 and TRACKING_GRID[rect.x // BLOCK_SIZE, rect.y // BLOCK_SIZE] == 0:
                                TRACKING_GRID[rect.x // BLOCK_SIZE, rect.y // BLOCK_SIZE] = PLAYER2
                                TURN += 1

        if checkWinningCondition(TRACKING_GRID):
            draw(TRACKING_GRID, SCREEN)
            pygame.display.update()
            pygame.time.wait(1000)
            TRACKING_GRID = np.zeros((ARRAY_SIZE, ARRAY_SIZE))

        if checkStalemate(TRACKING_GRID):
            draw(TRACKING_GRID, SCREEN)
            pygame.display.update()
            pygame.time.wait(1000)
            TRACKING_GRID = np.zeros((ARRAY_SIZE, ARRAY_SIZE))

        pygame.display.update()


run()
