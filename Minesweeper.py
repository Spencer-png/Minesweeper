import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 6
MINES_COUNT = 2
CELL_SIZE = 40
MARGIN = 5
WINDOW_SIZE = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * MARGIN
FONT_SIZE = CELL_SIZE // 2

# Colors
BACKGROUND_COLOR = (0, 0, 0)  # Changed to black
CELL_COLOR = (0, 0, 0)        # Unrevealed cells also black
REVEALED_CELL_COLOR = (0, 0, 0)  # Revealed cells black
MINE_COLOR = (255, 0, 0)      # Mines red
TEXT_COLOR = (255, 255, 255)  # Text color white
GAME_OVER = (137, 207, 240) # Game over color

# Initialize the window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Minesweeper")
font = pygame.font.SysFont(None, FONT_SIZE)

def initialize_grid(size, mines):
    grid = [['1' for _ in range(size)] for _ in range(size)]
    mine_positions = set()
    while len(mine_positions) < mines:
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        mine_positions.add((x, y))
    for (x, y) in mine_positions:
        grid[x][y] = 'M'
    return grid

def count_adjacent_mines(grid, x, y):
    size = len(grid)
    mine_count = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and grid[nx][ny] == 'M':
                mine_count += 1
    return mine_count

def reveal_grid(grid):
    revealed_grid = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == 'M':
                continue
            mine_count = count_adjacent_mines(grid, x, y)
            grid[x][y] = '1'  # All numbers set to '1'
    return revealed_grid

def draw_grid(screen, grid, revealed_grid, game_over):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(
                x * CELL_SIZE + (x + 1) * MARGIN,
                y * CELL_SIZE + (y + 1) * MARGIN,
                CELL_SIZE, CELL_SIZE
            )

            if revealed_grid[x][y] or (game_over and grid[x][y] == 'M'):
                # Reveal all cells if game is over or cell is already revealed
                color = REVEALED_CELL_COLOR if grid[x][y] != 'M' else MINE_COLOR
                pygame.draw.rect(screen, color, rect)  # Fill cell for revealed cells
                pygame.draw.rect(screen, TEXT_COLOR, rect, 1)  # Draw border around revealed cells
                if grid[x][y] != ' ' and grid[x][y] != 'M':  # Draw text if cell is a number
                    text_surface = font.render(grid[x][y], True, TEXT_COLOR)
                    text_rect = text_surface.get_rect(center=rect.center)
                    screen.blit(text_surface, text_rect)
            else:
                pygame.draw.rect(screen, TEXT_COLOR, rect, 1)  # Draw only the border for unrevealed cells


def main():
    def reset_game():
        nonlocal grid, revealed_grid, game_over
        grid = initialize_grid(GRID_SIZE, MINES_COUNT)
        revealed_grid = reveal_grid(grid)
        game_over = False

    grid = initialize_grid(GRID_SIZE, MINES_COUNT)
    revealed_grid = reveal_grid(grid)
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = event.pos
                grid_x = mouse_x // (CELL_SIZE + MARGIN)
                grid_y = mouse_y // (CELL_SIZE + MARGIN)
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    revealed_grid[grid_x][grid_y] = True
                    if grid[grid_x][grid_y] == 'M':
                        game_over = True  # Set game over to true when a mine is clicked
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()

        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen, grid, revealed_grid, game_over)  # Pass game_over flag to draw_grid
        if game_over:
            game_over_text = font.render("Game Over! Press SPACE to reset", True, GAME_OVER)
            screen.blit(game_over_text, game_over_text.get_rect(center=screen.get_rect().center))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
