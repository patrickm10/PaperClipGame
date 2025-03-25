import pygame
import time
import random

pygame.init()
pygame.font.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

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

# Fonts
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

class Player:
    """Class to manage the player's score, balance, and rate per second (rps)."""
    
    def __init__(self):
        self.score = 0
        self.balance = 0
        self.rps = 0  # Rate per second
        self.upgrade_count = 0  # Number of times upgrade has been purchased
        self.estates = 0  # Number of estates owned
        self.create_value = 0  # Value for create button
        self.level = 0 # Player level

    def update(self, time_diff):
        """Update the score and balance based on time."""
        self.balance += self.rps * time_diff
        self.score += self.rps * time_diff

class Worker:
    """Class to manage workers and their effects on the game."""    
    def __init__(self, cost, rps, name):
        self.cost = cost
        self.rps = rps
        self.count = 0
        self.name = name

    def hire(self):
        """Hire a worker and increase rps."""
        self.count += 1
        return self.rps

class Achievement:
    """Class to manage and check achievements."""    
    def __init__(self, name, condition, message, score_requirement=None):
        self.name = name
        self.condition = condition
        self.message = message
        self.score_requirement = score_requirement
        self.achieved = False

    def check(self, player, active_achievements):
        """Check if an achievement is unlocked."""
        if not self.achieved:
            if (self.score_requirement and player.score >= self.score_requirement) or self.condition():
                self.achieved = True
                active_achievements.append((self.message, time.time()))

class Game:
    """Main game class that handles game logic and UI.""" 
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Paperclip Game")
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.workers = {
            'worker': Worker(200, 1, 'Worker'),
            'grand_worker': Worker(500, 5, 'Grand Worker')
        }
        self.estates = {
            'estate': Worker(1000, 10, 'Estate'),
            'grand_estate': Worker(5000, 50, 'Grand Estate')
        }
        self.achievements = [
            Achievement("1000_points", lambda: self.player.score >= 1000, "Achievement Unlocked: 1000 Points!", 1000),
            Achievement("first_worker", lambda: self.workers['worker'].count > 0, "Achievement Unlocked: Hired a Worker!"),
            Achievement("first_grand_worker", lambda: self.workers['grand_worker'].count > 0, "Achievement Unlocked: Hired a Grand Worker!"),
            Achievement("10_workers", lambda: self.workers['worker'].count >= 10, "Achievement Unlocked: 10 Workers!"),
            Achievement("100_workers", lambda: self.workers['worker'].count >= 100, "Achievement Unlocked: 100 Workers!"),
            Achievement("1000_workers", lambda: self.workers['worker'].count >= 1000, "Achievement Unlocked: 1000 Workers!"),
            Achievement("10_grand_workers", lambda: self.workers['grand_worker'].count >= 10, "Achievement Unlocked: 10 Grand Workers!"),
            Achievement("100_grand_workers", lambda: self.workers['grand_worker'].count >= 100, "Achievement Unlocked: 100 Grand Workers!"),
            Achievement("1000_grand_workers", lambda: self.workers['grand_worker'].count >= 1000, "Achievement Unlocked: 1000 Grand Workers!"),
            Achievement("10_estates", lambda: self.estates['estate'].count >= 10, "Achievement Unlocked: 10 Estates!"),
            Achievement("10_grand_estates", lambda: self.estates['grand_estate'].count >= 10, "Achievement Unlocked: 10 Grand Estates!")
        ]
        self.active_achievements = []
        self.last_update_time = time.time()
        self.mouse_click = False  # Track if a mouse click is currently active
        self.spin_in_progress = False  # Track if the roulette wheel is spinning
        self.bet_amount = 0  # Amount player has bet on roulette
        self.upgrade_cost = 500  # Starting upgrade cost
        self.upgrade_count = 0  # Track how many upgrades the player has purchased

    def update_game(self):
        """Update the game logic."""
        current_time = time.time()
        time_diff = current_time - self.last_update_time
        self.last_update_time = current_time

        # Recalculate RPS based on worker count
        self.player.rps = sum(worker.count * worker.rps for worker in self.workers.values())

        # Update balance and score using the correct RPS value
        self.player.update(time_diff)

        # Check for achievements
        for achievement in self.achievements:
            achievement.check(self.player, self.active_achievements)

    def draw_ui(self):
        """Draw the game UI including score, balance, and buttons."""
        self.screen.fill(WHITE)
        self.display_score()
        self.draw_buttons()
        self.draw_achievements()  # Call the method to display active achievements
        self.draw_achievement_history()  # Call the method to display achievement history

    def draw_achievements(self):
        """Display the unlocked achievements on the screen."""
        y_offset = HEIGHT - 150  # Starting Y position for the first achievement
        x_offset = WIDTH // 2   # Starting X position for the first achievement
        for achievement, unlock_time in self.active_achievements:
            achievement_text = small_font.render(achievement, True, BLACK)
            self.screen.blit(achievement_text, (x_offset, y_offset))
            y_offset += 30  # Space out the achievements vertically

    def draw_achievement_history(self):
        """Draw a list of all unlocked achievements."""
        button_rect = pygame.Rect(WIDTH - 250, HEIGHT - 50, 200, 40)
        pygame.draw.rect(self.screen, DARK_BLUE, button_rect, border_radius=10)
        self.screen.blit(small_font.render("Achievements", True, WHITE), (button_rect.x + 10, button_rect.y + 10))

        if button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and not self.mouse_click:  # Left click
                self.mouse_click = True
                self.show_achievement_history()
        elif not pygame.mouse.get_pressed()[0]:
            self.mouse_click = False

    def show_achievement_history(self):
        """Display the achievement history in a new window."""
        history_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        history_screen.fill(WHITE)
        y_offset = 50
        for achievement in self.active_achievements:
            text = small_font.render(achievement[0], True, GREEN)
            history_screen.blit(text, (WIDTH // 2 - 150, y_offset))
            y_offset += 30  # Add space between achievements
        pygame.display.update()
        time.sleep(3)  # Display the history for 3 seconds

    def display_score(self):
        """Display score, balance, and rate per second."""
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, 40))
        score_text = font.render(f"Total Score: {self.player.score:.1f}", True, WHITE)
        score_text_rect = score_text.get_rect(center=(WIDTH // 2, 20))
        self.screen.blit(score_text, score_text_rect)

        balance_text = small_font.render(f"Balance: ${int(self.player.balance)}", True, BLACK)
        self.screen.blit(balance_text, (20, 50))

        rps_text = small_font.render(f"RPS: {self.player.rps:.1f}", True, BLACK)
        self.screen.blit(rps_text, (20, 80))

    def draw_buttons(self):
        """Draw all the buttons for player actions."""
        self.draw_worker_button("REG ELF", (20, 280), self.workers['worker'])
        self.draw_worker_button("GRAND ELF", (20, 360), self.workers['grand_worker'])
        self.draw_button("CREATE", (20, 120), lambda: self.create_points())
        self.draw_upgrade_button("UPGRADE", (20, 200), lambda: self.upgrade_points())
        self.draw_estate_button("ESTATE", (20, 440), self.estates['estate'])
        self.draw_estate_button("GRAND ESTATE", (20, 520), self.estates['grand_estate'])
        self.draw_roulette_button("BET & SPIN", (WIDTH // 2 - 100, HEIGHT // 2 - 25), lambda: self.place_bet())

    def draw_worker_button(self, label, position, worker):
        """Helper method to draw a worker button with cost and count."""
        button_rect = pygame.Rect(position[0], position[1], 200, 50)
        pygame.draw.rect(self.screen, DARK_BLUE, button_rect, border_radius=10)
        self.screen.blit(font.render(label, True, WHITE), (button_rect.x + 10, button_rect.y + 10))
        self.screen.blit(small_font.render(f"Cost: ${worker.cost}", True, BLACK), (button_rect.x + 5, button_rect.y + 55))
        self.screen.blit(small_font.render(f"Count: {worker.count}", True, BLACK), (button_rect.x + 210, button_rect.y + 15))

        if button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and not self.mouse_click:  # Left click
                self.mouse_click = True
                self.hire_worker(worker)
        elif not pygame.mouse.get_pressed()[0]:
            self.mouse_click = False

    def draw_button(self, label, position, action):
        """Helper method to draw a generic button."""
        button_rect = pygame.Rect(position[0], position[1], 200, 50)
        pygame.draw.rect(self.screen, DARK_BLUE, button_rect, border_radius=10)
        self.screen.blit(font.render(label, True, WHITE), (button_rect.x + 10, button_rect.y + 10))

        if button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and not self.mouse_click:  # Left click
                self.mouse_click = True
                action()
        elif not pygame.mouse.get_pressed()[0]:
            self.mouse_click = False

    def draw_upgrade_button(self, label, position, action):
        """Helper method to draw the upgrade button."""
        button_rect = pygame.Rect(position[0], position[1], 200, 50)
        pygame.draw.rect(self.screen, GREEN, button_rect, border_radius=10)
        self.screen.blit(font.render(label, True, WHITE), (button_rect.x + 10, button_rect.y + 10))
        self.screen.blit(small_font.render(f"Cost: ${self.upgrade_cost}", True, BLACK), (button_rect.x + 5, button_rect.y + 55))
        self.screen.blit(small_font.render(f"Upgrades: {self.upgrade_count}", True, BLACK), (button_rect.x + 210, button_rect.y + 15))

        if button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and not self.mouse_click:  # Left click
                self.mouse_click = True
                action()
        elif not pygame.mouse.get_pressed()[0]:
            self.mouse_click = False

    def draw_estate_button(self, label, position, estate):
        """Helper method to draw an estate button with cost and count.""" 
        button_rect = pygame.Rect(position[0], position[1], 200, 50)
        pygame.draw.rect(self.screen, DARK_GREEN, button_rect, border_radius=10)
        self.screen.blit(font.render(label, True, WHITE), (button_rect.x + 10, button_rect.y + 10))
        self.screen.blit(small_font.render(f"Cost: ${estate.cost}", True, BLACK), (button_rect.x + 5, button_rect.y + 55))
        self.screen.blit(small_font.render(f"Count: {estate.count}", True, BLACK), (button_rect.x + 210, button_rect.y + 15))

        if button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and not self.mouse_click:  # Left click
                self.mouse_click = True
                self.hire_worker(estate)
        elif not pygame.mouse.get_pressed()[0]:
            self.mouse_click = False

    def draw_roulette_button(self, label, position, action):
        """Helper method to draw the roulette button.""" 
        button_rect = pygame.Rect(WIDTH - 240, 120, 200, 50)
        pygame.draw.rect(self.screen, DARK_YELLOW, button_rect, border_radius=10)
        self.screen.blit(font.render(label, True, WHITE), (button_rect.x + 10, button_rect.y + 10))

        if button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and not self.mouse_click:  # Left click
                self.mouse_click = True
                action()
        elif not pygame.mouse.get_pressed()[0]:
            self.mouse_click = False

    def hire_worker(self, worker):
        """Hire the worker and deduct cost.""" 
        if self.player.balance >= worker.cost:
            self.player.balance -= worker.cost
            worker.hire()
            self.player.rps += worker.rps

    def create_points(self):
        """Method to create points.""" 
        self.player.balance += 100  # Add a fixed amount of balance
        self.player.score += 100    # Add a fixed amount of score
        self.player.create_value += 1  # Add a fixed amount of create value

    def upgrade_points(self):
        """Method to upgrade the points creation.""" 
        if self.player.balance >= self.upgrade_cost:
            self.player.balance -= self.upgrade_cost
            self.upgrade_count += 1
            self.upgrade_cost = int(self.upgrade_cost * 1.5)  # Increase upgrade cost
            self.player.create_value += 1

    def upgrade_worker(self, worker):
        """Upgrade the worker and deduct cost.""" 
        if self.player.balance >= worker.cost:
            self.player.balance -= worker.cost
            worker.hire()
            self.player.rps += worker.rps
            worker.cost = int(worker.cost * 1.5)  # Increase worker's cost by 1.5 times

    def upgrade_estate(self, estate):
        """Upgrade the estate and deduct cost.""" 
        if self.player.balance >= estate.cost:
            self.player.balance -= estate.cost
            estate.hire()
            self.player.rps += estate.rps
            estate.cost = int(estate.cost * 1.5)  # Increase estate's cost by 1.5 times

    def check_evolution(self):
        """Check if the player can evolve.""" 
        if self.player.create_value >= 100:
            self.evolve()

    def evolve(self):
        """Method to evolve the player.""" 
        if self.player.create_value >= 100:
            self.player.create_value = 1
            self.player.rps += 10
            self.upgrade_cost = 500 
            self.upgrade_count = 0
            self.player.balance += 1000
            self.player.score += 1000
            self.player.estates += 1
            self.player.level += 1
            # add other evolution effects here

    def roulette_spin(self):
        """Simulate the roulette spin.""" 
        if self.spin_in_progress:
            spin_result = random.randint(0, 12)  # Simulate a spin result
            if spin_result == 10:
                self.player.balance += self.bet_amount * 35
            elif spin_result == 11:
                self.player.balance += self.bet_amount * 2
            elif spin_result == 12:
                self.player.balance += self.bet_amount * 5
            self.spin_in_progress = False
            self.bet_amount = 0

        else:
            print("Spin is already in progress.")

    def run(self):
        """Main game loop.""" 
        running = True
        while running:
            self.update_game()
            self.draw_ui()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
