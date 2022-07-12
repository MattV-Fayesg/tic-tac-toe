import numpy as np
import pygame
import sys

pygame.init()

# constants
screen_width = 600
screen_height = 600
line_width = 15
board_rows = 3
board_cols = 3
screen_size = screen_width // board_cols
circle_radius = screen_size // 3
circle_width = 15
cross_width = 25
space = screen_size // 4
player = 1
game_over = False

# Colors (RGB)
df_green = (10, 145, 90)
bg_color = (28, 150, 100)
circle_color = (200, 200, 255)
cross_color = (10, 30, 10)

# board
board = np.zeros((board_rows, board_cols))

# Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Jogo da Idosa')
screen.fill(bg_color)


def draw_lines():
    # Horizontal
    pygame.draw.line(screen, df_green, (0, screen_size), (screen_width, screen_size), line_width)
    pygame.draw.line(screen, df_green, (0, 2 * screen_size), (screen_width, 2 * screen_size), line_width)
    # vertical
    pygame.draw.line(screen, df_green, (screen_size, 0), (screen_size, screen_height), line_width)
    pygame.draw.line(screen, df_green, (2 * screen_size, 0), (2 * screen_size, screen_height), line_width)


def draw_figures():
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 1:
                circle_center = (int(col * screen_size + screen_size // 2), int(row * screen_size + screen_size // 2))
                pygame.draw.circle(screen, circle_color, circle_center, circle_radius, circle_width)
            elif board[row][col] == 2:
                # Drawing 'X'
                start_pos_right = (col * screen_size + space, row * screen_size + screen_size - space)
                end_pos_left = (col * screen_size + screen_size - space, row * screen_size + space)
                pygame.draw.line(screen, cross_color, start_pos_right, end_pos_left, cross_width)  # Left to Right

                start_pos_left = (col * screen_size + space, row * screen_size + space)
                end_pos_right = (col * screen_size + screen_size - space, row * screen_size + screen_size - space)
                pygame.draw.line(screen, cross_color, start_pos_left, end_pos_right, cross_width)  # Right to left


def mark_square(row, col):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0


def is_board_full():
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 0:
                return False
    return True


def check_win():
    # vertical
    for col in range(board_cols):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col)
            return True

    # horizontal
    for row in range(board_rows):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row)
            return True

    # asc diagonal
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal()
        return True

    # desc diagonal
    if board[2][2] == player and board[1][1] == player and board[0][0] == player:
        draw_desc_diagonal()
        return True

    return False


def draw_vertical_winning_line(col):
    posX = col * screen_size + screen_size // 2
    if player == 1:
        color = circle_color
        pygame.draw.line(screen, color, (posX, 15), (posX, screen_height - 15), 15)
    elif player == 2:
        color = cross_color
        pygame.draw.line(screen, color, (posX, 15), (posX, screen_height - 15), 15)


def draw_horizontal_winning_line(row):
    posY = row * screen_size + screen_size // 2
    if player == 1:
        color = circle_color
        pygame.draw.line(screen, color, (15, posY), (screen_width - 15, posY), 15)
    elif player == 2:
        color = cross_color
        pygame.draw.line(screen, color, (15, posY), (screen_width - 15, posY), 15)


def draw_asc_diagonal():
    if player == 1:
        color = circle_color
        pygame.draw.line(screen, color, (15, screen_height - 15), (screen_width - 15, 15), 25)
    elif player == 2:
        color = cross_color
        pygame.draw.line(screen, color, (15, screen_height - 15), (screen_width - 15, 15), 25)


def draw_desc_diagonal():
    if player == 1:
        color = circle_color
        pygame.draw.line(screen, color, (15, 15), (screen_width - 15, screen_height - 15), 25)
    elif player == 2:
        color = cross_color
        pygame.draw.line(screen, color, (15, 15), (screen_width - 15, screen_height - 15), 25)


def restart():
    screen.fill(bg_color)
    draw_lines()
    for row in range(board_rows):
        for col in range(board_cols):
            board[row][col] = 0


draw_lines()

# Mainloop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            X = event.pos[0]  # x
            Y = event.pos[1]  # y
            clicked_row = int(Y // screen_size)
            clicked_col = int(X // screen_size)

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col)
                if check_win():
                    game_over = True
                player = player % 2 + 1

                draw_figures()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                game_over = False

        pygame.display.update()
