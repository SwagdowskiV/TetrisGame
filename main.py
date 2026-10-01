import pygame
from pieces import create_new_piece, get_random_color, rotate_piece
from board import can_move_down, can_move_horizontal, clear_lines, is_game_over

pygame.init()

# Board settings
CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Position of the board inside the window
BOARD_X = 150
BOARD_Y = 50

# Window settings
WIDTH = 800
HEIGHT = 700

#Misc
score = 0
game_over = False

#UI score display
font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")


# Create the first piece
piece = create_new_piece()
piece_color = get_random_color()

# Keeps track of when the piece last moved down
last_fall_time = pygame.time.get_ticks()

# How many milliseconds between each fall
FALL_SPEED = 500

# Blocks that have already landed
landed_blocks = []



running = True

#===========INSIDE GAME LOOP========================

while running:
    # Quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
             if can_move_horizontal(piece, landed_blocks, -1):
                piece = [(col - 1, row) for col, row in piece]

            if event.key in (pygame.K_RIGHT, pygame.K_d):
                if can_move_horizontal(piece, landed_blocks, 1):
                    piece = [(col + 1, row) for col, row in piece]

            if event.key in (pygame.K_DOWN, pygame.K_s):
                if can_move_down(piece, landed_blocks):
                    lowest_row = max(row for col, row in piece)

                    if lowest_row < BOARD_HEIGHT - 1 and can_move_down(piece, landed_blocks):
                      piece = [(col, row + 1) for col, row in piece]

            if event.key in (pygame.K_UP, pygame.K_w) and not game_over:
                 piece = rotate_piece(piece)

            if event.key == pygame.K_r and game_over:
              piece = create_new_piece()
              piece_color = get_random_color()
              landed_blocks = []
              score = 0
              game_over = False




    # Fill background with black
    screen.fill((0, 0, 0))

    # Draw the Tetris grid
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            x = BOARD_X + col * CELL_SIZE
            y = BOARD_Y + row * CELL_SIZE

            pygame.draw.rect(
                screen,
                (80, 80, 80),
                (x, y, CELL_SIZE, CELL_SIZE),
                1
            )

    # Draw the current falling Tetris piece
    for col, row in piece:
        x = BOARD_X + col * CELL_SIZE
        y = BOARD_Y + row * CELL_SIZE

        pygame.draw.rect(
            screen,
            piece_color,
            (x, y, CELL_SIZE, CELL_SIZE)
        )

    # Draw blocks that have already landed
    for col, row, color in landed_blocks:
     pygame.draw.rect(
        screen,
        color,
        (
            BOARD_X + col * CELL_SIZE,
            BOARD_Y + row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
     )

   
    # Get the current time
    current_time = pygame.time.get_ticks()

    # Check if enough time has passed
    if current_time - last_fall_time >= FALL_SPEED:


        # Check if the piece can move down without hitting the floor
        if can_move_down(piece, landed_blocks):
          piece = [(col, row + 1) for col, row in piece]
    
        else:
            # The piece has landed
            for block in piece:
                 col, row = block
                 landed_blocks.append((col, row, piece_color))

            # Check for completed lines
            landed_blocks, lines_cleared = clear_lines(landed_blocks)

            # Update score for cleared lines
            score += lines_cleared * 100 

            # Create a new piece at the top
            piece = create_new_piece()
            piece_color = get_random_color()

            if is_game_over(piece, landed_blocks):
                game_over = True

        # Reset the timer
        last_fall_time = current_time
       
    #Draw the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (500, 100))

    #Game over screen
    game_over_text = font.render(
          "GAME OVER",
          True,
          (255, 255, 255)
    )

    restart_text = font.render(
        "Press R to restart",
        True,
        (255, 255, 255)
    )

    if game_over:

         # Dark overlay
         overlay = pygame.Surface((WIDTH, HEIGHT))
         overlay.set_alpha(180)
         overlay.fill((0, 0, 0))
         screen.blit(overlay, (0, 0))

         screen.blit(game_over_text, (390, 300))
         screen.blit(restart_text, (350, 340))

    # Update the display
    pygame.display.flip()

    # Small delay so the loop doesn't run unnecessarily fast
    pygame.time.delay(10)







pygame.quit()