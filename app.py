import pygame
from game import Game
import time

pygame.init()
screen = pygame.display.set_mode((900, 645))
clock = pygame.time.Clock()
running = True

LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)


game = Game(80)
game.board.initialize_pieces()

checkmate = False

def display_checkmate_message(screen, message):
    font = pygame.font.SysFont(None, 75)
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)

while running:
    if game.first_move_made:  
        current_time = time.time()
        elapsed_time = current_time - game.last_move_time
        if game.turn == 'white':
            game.white_time -= elapsed_time
        else:
            game.black_time -= elapsed_time
        game.last_move_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            square = game.get_square_under_mouse()
            if square is not None:
                row, col = square
                game.handle_piece_selection(row, col, screen=screen)
                if game.is_checkmate(game.turn):
                    checkmate = True

    screen.fill((0, 0, 0))  
    game.draw(screen)
    if checkmate:
        display_checkmate_message(screen, "Checkmate")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()