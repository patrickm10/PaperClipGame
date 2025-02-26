import pygame
import time

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paperclip Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
BLUE = (70, 130, 180)
DARK_BLUE = (50, 90, 140)
GREEN = (60, 179, 113)
DARK_GREEN = (34, 139, 34)
YELLOW = (255, 204, 0)
DARK_YELLOW = (204, 170, 0)
GRAY = (169, 169, 169)

# Font
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

# Game variables
score = 0
balance = 0
rps = 0  # Rate per second
last_update_time = time.time()

# Costs
point_value = 10
upgrade_cost = 50
worker_cost = 200
grand_worker_cost = 500
estate_cost = 1000

# Counts
upgrade_count = 0
worker_count = 0
grand_worker_count = 0
total_estates = 0

# Worker Rates
worker_rps = 1
grand_worker_rps = 5

# Time tracking
last_worker_update = time.time()

# Achievements
achievements = {
    "1000_points": {"score": 1000, "unlocked": False, "message": "Achievement Unlocked: 1000 Points!"},
    "first_worker": {"achieved": False, "condition": lambda: worker_count > 0, "message": "Achievement Unlocked: Hired a worker!"},
    "first_grand_worker": {"achieved": False, "condition": lambda: grand_worker_count > 0, "message": "Achievement Unlocked: Hired a grand worker!"},
    "first_estate": {"achieved": False, "condition": lambda: total_estates > 0, "message": "Achievement Unlocked: Purchased an estate!"},
    "ten_workers": {"achieved": False, "condition": lambda: worker_count >= 10, "message": "Achievement Unlocked: Hired 10 workers!"},
    "five_grand_workers": {"achieved": False, "condition": lambda: grand_worker_count >= 5, "message": "Achievement Unlocked: Hired 5 grand workers!"},
    "fifty_thousand_points": {"score": 50000, "unlocked": False, "message": "Achievement Unlocked: 50,000 Points!"},
    "one_million_points": {"score": 1000000, "unlocked": False, "message": "Achievement Unlocked: 1 Million Points!"},
}

# Track active achievement displays
active_achievements = []  # List of tuples: (message, start_time)

# Buttons
create_button_rect = pygame.Rect(20, 120, 180, 50)
upgrade_button_rect = pygame.Rect(20, 210, 180, 50)
worker_button_rect = pygame.Rect(20, 300, 180, 50)
grand_worker_button_rect = pygame.Rect(20, 390, 180, 50)
estate_button_rect = pygame.Rect(20, 480, 180, 50)


def display_score():
    """Displays the total score and balance."""
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 40))
    score_text = font.render(f"Total Score: {score:.1f}", True, WHITE)
    score_text_rect = score_text.get_rect(center=(WIDTH // 2, 20))
    screen.blit(score_text, score_text_rect)

    balance_text = small_font.render(f"Balance: ${balance:.1f}", True, BLACK)
    screen.blit(balance_text, (20, 50))

    rps_text = small_font.render(f"RPS: {rps:.1f}", True, BLACK)
    screen.blit(rps_text, (20, 80))


def draw_buttons():
    """Draws all buttons dynamically."""
    pygame.draw.rect(screen, DARK_BLUE, create_button_rect, border_radius=10)
    screen.blit(font.render("CREATE", True, WHITE), (create_button_rect.x + 10, create_button_rect.y + 10))

    pygame.draw.rect(screen, DARK_GREEN, upgrade_button_rect, border_radius=10)
    screen.blit(font.render("UPGRADE", True, WHITE), (upgrade_button_rect.x + 10, upgrade_button_rect.y + 10))
    screen.blit(small_font.render(f"Cost: ${upgrade_cost}", True, BLACK), (upgrade_button_rect.x, upgrade_button_rect.y + 60))
    screen.blit(small_font.render(f"Count: {upgrade_count}", True, BLACK), (upgrade_button_rect.x + 200, upgrade_button_rect.y + 10))

    pygame.draw.rect(screen, DARK_YELLOW, worker_button_rect, border_radius=10)
    screen.blit(font.render("WORKER", True, BLACK), (worker_button_rect.x + 10, worker_button_rect.y + 10))
    screen.blit(small_font.render(f"Cost: ${worker_cost}", True, BLACK), (worker_button_rect.x, worker_button_rect.y + 60))
    screen.blit(small_font.render(f"Count: {worker_count}", True, BLACK), (worker_button_rect.x + 200, worker_button_rect.y + 10))

    pygame.draw.rect(screen, DARK_BLUE, grand_worker_button_rect, border_radius=10)
    screen.blit(font.render("GRAND", True, BLACK), (grand_worker_button_rect.x + 10, grand_worker_button_rect.y + 10))
    screen.blit(small_font.render(f"Cost: ${grand_worker_cost}", True, BLACK), (grand_worker_button_rect.x, grand_worker_button_rect.y + 60))
    screen.blit(small_font.render(f"Count: {grand_worker_count}", True, BLACK), (grand_worker_button_rect.x + 200, grand_worker_button_rect.y + 10))

    pygame.draw.rect(screen, DARK_YELLOW, estate_button_rect, border_radius=10)
    screen.blit(font.render("ESTATE", True, BLACK), (estate_button_rect.x + 10, estate_button_rect.y + 10))
    screen.blit(small_font.render(f"Cost: ${estate_cost}", True, BLACK), (estate_button_rect.x, estate_button_rect.y + 60))
    screen.blit(small_font.render(f"Count: {total_estates}", True, BLACK), (estate_button_rect.x + 200, estate_button_rect.y + 10))


def update_workers():
    """Adds balance and score from workers every second."""
    global last_worker_update, balance, rps, score
    current_time = time.time()
    if current_time - last_worker_update >= 1:
        balance += rps  # Add balance based on the rate per second
        score += rps    # Add to score based on the same rate
        last_worker_update = current_time


def check_achievements():
    """
    Checks and unlocks achievements based on game progress.
    """
    global active_achievements
    for key, achievement in achievements.items():
        if not achievement.get("achieved", False):
            if "score" in achievement and score >= achievement["score"]:
                achievement["achieved"] = True
                active_achievements.append((achievement["message"], time.time()))
            elif "condition" in achievement and achievement["condition"]():
                achievement["achieved"] = True
                active_achievements.append((achievement["message"], time.time()))


def display_achievements():
    """Displays active achievements on the screen."""
    global active_achievements
    y_offset = HEIGHT - 50
    for message, start_time in active_achievements:
        elapsed_time = time.time() - start_time
        if elapsed_time < 4:  # Display for 4 seconds
            achievement_text = small_font.render(message, True, BLACK)
            screen.blit(achievement_text, (WIDTH // 2 - achievement_text.get_width() // 2, y_offset))
            y_offset += 30  # Move the next achievement 30 units lower
        else:
            active_achievements.remove((message, start_time))


def handle_button_click(mouse_x, mouse_y):
    """Handles button clicks and updates the game state accordingly."""
    global balance, score, point_value, upgrade_cost, worker_cost, grand_worker_cost, estate_cost
    global upgrade_count, worker_count, grand_worker_count, total_estates, rps

    # CREATE button
    if create_button_rect.collidepoint(mouse_x, mouse_y):
        balance += point_value
        score += point_value

    # UPGRADE button
    elif upgrade_button_rect.collidepoint(mouse_x, mouse_y) and balance >= upgrade_cost:
        balance -= upgrade_cost
        point_value *= 2
        upgrade_count += 1
        upgrade_cost *= 2

    # WORKER button
    elif worker_button_rect.collidepoint(mouse_x, mouse_y) and balance >= worker_cost:
        balance -= worker_cost
        worker_count += 1
        rps += worker_rps  # Update the rate per second (rps)

    # GRAND WORKER button
    elif grand_worker_button_rect.collidepoint(mouse_x, mouse_y) and balance >= grand_worker_cost:
        balance -= grand_worker_cost
        grand_worker_count += 1
        rps += grand_worker_rps  # Update the rate per second (rps)

    # ESTATE button
    elif estate_button_rect.collidepoint(mouse_x, mouse_y) and balance >= estate_cost:
        balance -= estate_cost
        total_estates += 1


def main():
    """Main game loop."""
    global score, balance, last_update_time, rps

    running = True
    while running:
        screen.fill(WHITE)
        display_score()
        draw_buttons()
        check_achievements()
        display_achievements()

        # Update workers (affect balance)
        update_workers()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(*event.pos)

    pygame.quit()


if __name__ == "__main__":
    main()
