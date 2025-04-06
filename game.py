import pygame
import random
import os
import sys

pygame.init()

# Game Window
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
BOUNDARY_MARGIN = 50

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Initialize display
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Load Sounds
BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
eat_sound = pygame.mixer.Sound(os.path.join(BASE_PATH, "assets", "eat.wav"))
gameover_sound = pygame.mixer.Sound(os.path.join(BASE_PATH, "assets", "gameover.wav"))

# Game Variables
difficulty_options = ["Low", "Medium", "High"]
difficulty_index = 1  # Default Medium
speed_levels = {"Low": 5, "Medium": 10, "High": 15}

# Function to draw text
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    display.blit(text_surface, text_rect)

# Function to draw boundary
def draw_boundary():
    pygame.draw.rect(display, WHITE, (BOUNDARY_MARGIN, BOUNDARY_MARGIN, WIDTH - 2 * BOUNDARY_MARGIN, HEIGHT - 2 * BOUNDARY_MARGIN), 3)

# Main Menu
def main_menu():
    global difficulty_index
    while True:
        display.fill(BLACK)
        draw_text("Select Difficulty", 50, WHITE, WIDTH // 2, HEIGHT // 5)
        draw_text("Use UP/DOWN to navigate, ENTER to select", 25, WHITE, WIDTH // 2, HEIGHT // 5 + 40)
        
        for i, option in enumerate(difficulty_options):
            color = WHITE if i != difficulty_index else BLUE
            draw_text(option, 40, color, WIDTH // 2, HEIGHT // 3 + i * 50)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    difficulty_index = (difficulty_index - 1) % len(difficulty_options)
                elif event.key == pygame.K_DOWN:
                    difficulty_index = (difficulty_index + 1) % len(difficulty_options)
                elif event.key == pygame.K_RETURN:
                    return difficulty_index  # Return selected difficulty

# Game Over Screen
def game_over():
    gameover_sound.play()
    display.fill(BLACK)
    draw_text("Game Over!", 50, WHITE, WIDTH // 2, HEIGHT // 2 - 40)
    draw_text("Press R to Restart or Q to Quit", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 20)
    pygame.display.flip()
    pygame.time.delay(2000)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart game
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Game Loop
def game_loop():
    global difficulty_index
    difficulty_index = main_menu()  # Get selected difficulty
    difficulty = difficulty_options[difficulty_index]
    FPS = speed_levels[difficulty]
    clock = pygame.time.Clock()
    speed_increment = 0.1
    
    snake = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2 - BLOCK_SIZE, HEIGHT // 2), (WIDTH // 2 - 2 * BLOCK_SIZE, HEIGHT // 2)]
    snake_dir = (BLOCK_SIZE, 0)
    apple = (random.randint((BOUNDARY_MARGIN + BLOCK_SIZE) // BLOCK_SIZE, (WIDTH - BOUNDARY_MARGIN - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
             random.randint((BOUNDARY_MARGIN + BLOCK_SIZE) // BLOCK_SIZE, (HEIGHT - BOUNDARY_MARGIN - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
    score = 0
    paused = False
    
    while True:
        display.fill(BLACK)
        draw_boundary()
        draw_text("Press P to Hold", 20, WHITE, WIDTH - 100, 20)
        draw_text(f"Score: {score}", 30, WHITE, BOUNDARY_MARGIN + 50, 30)
        draw_text(f"Level: {difficulty}", 30, WHITE, WIDTH // 2, 30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != (0, BLOCK_SIZE):
                    snake_dir = (0, -BLOCK_SIZE)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -BLOCK_SIZE):
                    snake_dir = (0, BLOCK_SIZE)
                elif event.key == pygame.K_LEFT and snake_dir != (BLOCK_SIZE, 0):
                    snake_dir = (-BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-BLOCK_SIZE, 0):
                    snake_dir = (BLOCK_SIZE, 0)
                elif event.key == pygame.K_p:
                    paused = not paused
        
        if not paused:
            new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
            snake.insert(0, new_head)
            
            if new_head in snake[1:] or not (BOUNDARY_MARGIN < new_head[0] < WIDTH - BOUNDARY_MARGIN - BLOCK_SIZE and BOUNDARY_MARGIN < new_head[1] < HEIGHT - BOUNDARY_MARGIN - BLOCK_SIZE):
                if game_over():
                    game_loop()
                    return
            
            if new_head == apple:
                eat_sound.play()
                apple = (random.randint((BOUNDARY_MARGIN + BLOCK_SIZE) // BLOCK_SIZE, (WIDTH - BOUNDARY_MARGIN - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randint((BOUNDARY_MARGIN + BLOCK_SIZE) // BLOCK_SIZE, (HEIGHT - BOUNDARY_MARGIN - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
                score += 1
                FPS += speed_increment
            else:
                snake.pop()
        
        for block in snake:
            pygame.draw.rect(display, GREEN, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(display, RED, pygame.Rect(apple[0], apple[1], BLOCK_SIZE, BLOCK_SIZE))
        draw_text("Created by Ameer Hamza", 20, WHITE, WIDTH // 2, HEIGHT - 30)
        pygame.display.flip()
        clock.tick(FPS)

game_loop()
