import pygame
import time

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paperclip Clicker")

# Colors
BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)
BLUE = (70, 130, 180)
DARK_BLUE = (50, 90, 140)
GREEN = (60, 179, 113)
DARK_GREEN = (34, 139, 34)
YELLOW = (255, 204, 0)
DARK_YELLOW = (204, 170, 0)
RED = (200, 50, 50)
GRAY = (169, 169, 169)

# Font
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

# Game variables
score = 0
click_value = 10
upgrade_cost = 50
worker_cost = 200
upgrade_count = 0
worker_count = 0
last_worker_update = time.time()

# Worker stick figure positions
worker_positions = []
worker_update_rate = 1  # Normal worker earns 1 point per second

# Buttons
click_button_rect = pygame.Rect(320, 250, 180, 60)
upgrade_button_rect = pygame.Rect(50, 250, 210, 40)
worker_button_rect = pygame.Rect(50, 320, 210, 40)

# Click effects
clicking = False
upgrading = False
hiring_worker = False
animation_timer = 0

def draw_stick_figure(x, y, color=BLACK, size=20):
    """Draw a simple stick figure at the given coordinates with adjustable size and color."""
    # Head (circle)
    pygame.draw.circle(screen, color, (x, y - size), size)

    # Body (line)
    pygame.draw.line(screen, color, (x, y - size), (x, y + size * 2), 5)

    # Arms (lines)
    pygame.draw.line(screen, color, (x - size, y), (x + size, y), 5)

    # Legs (lines)
    pygame.draw.line(screen, color, (x, y + size * 2), (x - size, y + size * 3), 5)  # Left leg
    pygame.draw.line(screen, color, (x, y + size * 2), (x + size, y + size * 3), 5)  # Right leg

def display_score():
    """Display the score at the top center of the screen."""
    score_text = font.render(f"Score: {score}", True, DARK_GRAY)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 50))

def draw_buttons():
    """Draw buttons with updated UI styles."""
    global clicking, upgrading, hiring_worker, animation_timer

    # Click button (blue)
    pygame.draw.rect(screen, DARK_BLUE if clicking else BLUE, click_button_rect, border_radius=15)
    click_text = font.render("Click", True, WHITE)
    screen.blit(click_text, (click_button_rect.x + 75, click_button_rect.y + 15))

    # Upgrade button (green)
    if score >= upgrade_cost or upgrade_count > 0:
        pygame.draw.rect(screen, DARK_GREEN if upgrading else GREEN, upgrade_button_rect, border_radius=15)
        upgrade_text = font.render(f"Upgrade ({upgrade_cost})", True, WHITE)
        screen.blit(upgrade_text, (upgrade_button_rect.x + 20, upgrade_button_rect.y + 10))

    # Worker button (yellow)
    if score >= worker_cost or worker_count > 0:
        pygame.draw.rect(screen, DARK_YELLOW if hiring_worker else YELLOW, worker_button_rect, border_radius=15)
        worker_text = font.render(f"Worker ({worker_cost})", True, DARK_GRAY)
        screen.blit(worker_text, (worker_button_rect.x + 20, worker_button_rect.y + 10))

def draw_worker_ticker():
    """Draw a ticker showing how many points are earned by workers."""
    worker_ticker_text = small_font.render(f"Workers: {worker_count}", True, DARK_GRAY)
    pygame.draw.rect(screen, LIGHT_GRAY, pygame.Rect(0, 100, WIDTH, 40))  # Ticker background
    screen.blit(worker_ticker_text, (WIDTH // 2 - worker_ticker_text.get_width() // 2, 110))

def update_workers():
    """Add score based on the number of workers every second."""
    global last_worker_update, score, worker_count
    current_time = time.time()
    
    if current_time - last_worker_update >= 1:  # 1-second interval
        for i in range(worker_count):
            # Every 10th worker earns 20 points per second, others earn 1 point
            if (i + 1) % 10 == 0:
                score += 20  # Green worker earns 20 points
            else:
                score += 1  # Regular workers earn 1 point
        last_worker_update = current_time

def main():
    """Main game loop."""
    global score, click_value, upgrade_cost, worker_cost, upgrade_count, worker_count
    global clicking, upgrading, hiring_worker, animation_timer, worker_positions

    # Constants
    figure_spacing = 40  # Horizontal spacing between stick figures
    max_x = WIDTH - 50  # Maximum x-position (to keep stick figures within screen width)
    line_height = 100  # Space between rows of workers

    running = True
    while running:
        screen.fill(WHITE)
        display_score()
        draw_buttons()
        draw_worker_ticker()

        # Draw mini stick figures for each worker
        green_worker_placed = False  # Flag to place only one green worker at a time
        for i, (x, y) in enumerate(worker_positions):
            # Every 10th worker becomes green and replaces the last 9 black workers
            if (i + 1) % 10 == 0 and not green_worker_placed:
                draw_stick_figure(x, y, color=GREEN)  # Draw green worker
                green_worker_placed = True
            elif (i + 1) % 10 != 0:
                draw_stick_figure(x, y)  # Regular workers are black

        pygame.display.flip()
        update_workers()

        current_time = pygame.time.get_ticks()

        # Animation effects: reset button color after animation time has passed
        if upgrading and current_time - animation_timer >= 200:  # Animation time for upgrade button
            upgrading = False
        if hiring_worker and current_time - animation_timer >= 200:  # Animation time for worker button
            hiring_worker = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Click button logic
                if click_button_rect.collidepoint(mouse_x, mouse_y):
                    score += click_value
                    clicking = True

                # Upgrade button logic
                if score >= upgrade_cost and upgrade_button_rect.collidepoint(mouse_x, mouse_y):
                    score -= upgrade_cost
                    click_value *= 2
                    upgrade_count += 1
                    upgrade_cost *= 2
                    upgrading = True

                # Worker button logic
                if score >= worker_cost and worker_button_rect.collidepoint(mouse_x, mouse_y):
                    score -= worker_cost
                    worker_count += 1
                    worker_cost += 100
                    hiring_worker = True

                    # Add worker position with x, y coordinates
                    if len(worker_positions) == 0:
                        worker_positions.append((100, 70))  # First worker at (x=100, y=70)
                    else:
                        # Get the x and y of the last worker
                        last_x, last_y = worker_positions[-1]

                        # Calculate new x, y position
                        new_x = last_x + figure_spacing
                        new_y = last_y

                        # If new_x goes beyond the width of the screen, go to the next line
                        if new_x > max_x:
                            new_x = 100  # Reset to start from the left
                            new_y += line_height  # Move to the next row

                        # Add the new position to worker_positions
                        worker_positions.append((new_x, new_y))

            elif event.type == pygame.MOUSEBUTTONUP:
                clicking = False

    pygame.quit()

if __name__ == "__main__":
    main()
