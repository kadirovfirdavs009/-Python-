import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions & Setup
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Car Racer")
CLOCK = pygame.time.Clock()

# Color Definitions
GRAY = (40, 40, 40)
GREEN = (30, 130, 40)
WHITE = (255, 255, 255)
YELLOW = (240, 240, 0)
BLACK = (20, 20, 20)
BLUE = (30, 100, 220)
RED = (220, 30, 30)

# Track Boundaries & Lanes
ROAD_LEFT = 60
ROAD_RIGHT = 340
LANES = [110, 200, 290]

# Function to procedurally draw realistic cars without external images
def generate_car_surface(main_color, is_player=True):
    surf = pygame.Surface((44, 80), pygame.SRCALPHA)
    
    DARK_GLASS = (30, 40, 50, 230)
    LIGHT_COLOR = (240, 240, 240)
    YELLOW_LIGHT = (255, 235, 120)
    RED_LIGHT = (230, 30, 30)

    # 1. Wheels (4 Outer Tires)
    pygame.draw.rect(surf, BLACK, (1, 8, 5, 14))   # Top Left
    pygame.draw.rect(surf, BLACK, (38, 8, 5, 14))  # Top Right
    pygame.draw.rect(surf, BLACK, (1, 58, 5, 14))  # Bottom Left
    pygame.draw.rect(surf, BLACK, (38, 58, 5, 14)) # Bottom Right

    # 2. Main Aerodynamic Chassis
    pygame.draw.rect(surf, main_color, (5, 4, 34, 72), border_radius=8)

    # 3. Windshield & Roof Architecture
    pygame.draw.polygon(surf, DARK_GLASS, [(10, 26), (34, 26), (30, 38), (14, 38)])
    pygame.draw.polygon(surf, DARK_GLASS, [(12, 54), (32, 54), (30, 64), (14, 64)])
    pygame.draw.rect(surf, main_color, (11, 38, 22, 16))

    # 4. Racing Stripe Detail
    stripe_color = LIGHT_COLOR if main_color != LIGHT_COLOR else BLACK
    pygame.draw.rect(surf, stripe_color, (19, 4, 6, 72))

    # 5. Headlights & Taillights
    if is_player:
        pygame.draw.circle(surf, YELLOW_LIGHT, (10, 6), 3)
        pygame.draw.circle(surf, YELLOW_LIGHT, (34, 6), 3)
        pygame.draw.rect(surf, RED_LIGHT, (8, 74, 8, 2))
        pygame.draw.rect(surf, RED_LIGHT, (28, 74, 8, 2))
    else:
        pygame.draw.circle(surf, YELLOW_LIGHT, (10, 74), 3)
        pygame.draw.circle(surf, YELLOW_LIGHT, (34, 74), 3)
        pygame.draw.rect(surf, RED_LIGHT, (8, 5, 8, 2))
        pygame.draw.rect(surf, RED_LIGHT, (28, 5, 8, 2))

    return surf

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = generate_car_surface(BLUE, is_player=True)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 90))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT + 5:
            self.rect.x -= 6
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT - 5:
            self.rect.x += 6
        if keys[pygame.K_UP] and self.rect.top > 50:
            self.rect.y -= 4
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT - 20:
            self.rect.y += 4

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = generate_car_surface(RED, is_player=False)
        self.reset_position()

    def reset_position(self):
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))

    def update(self, current_speed):
        self.rect.y += current_speed
        if self.rect.top > HEIGHT:
            self.reset_position()

# Helper Function to Draw UI Text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

# Game Loop Setup
def run_game():
    player = Player()
    enemy = Enemy()
    
    all_sprites = pygame.sprite.Group(player, enemy)
    enemies = pygame.sprite.Group(enemy)

    score = 0
    speed = 6
    line_y = 0
    game_over = False

    font_medium = pygame.font.SysFont("arial", 28)
    font_large = pygame.font.SysFont("arial", 42)

    while True:
        CLOCK.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    run_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            # Update Scrolling Road Position
            line_y = (line_y + speed) % 80

            # Update Sprites
            player.update()
            enemy.update(speed)

            # Check if Enemy Passed Successfully
            if enemy.rect.top > HEIGHT:
                score += 1
                if score % 5 == 0:
                    speed += 1  # Gradually increase difficulty

            # Check Collisions
            if pygame.sprite.spritecollideany(player, enemies):
                game_over = True

        # Render Background Grass & Asphalt
        SCREEN.fill(GREEN)
        pygame.draw.rect(SCREEN, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

        # Render Road Borders
        pygame.draw.rect(SCREEN, WHITE, (ROAD_LEFT - 10, 0, 10, HEIGHT))
        pygame.draw.rect(SCREEN, WHITE, (ROAD_RIGHT, 0, 10, HEIGHT))

        # Render Dynamic Lane Dividers
        for y in range(-80, HEIGHT + 80, 80):
            pygame.draw.rect(SCREEN, YELLOW, (155, y + line_y, 4, 40))
            pygame.draw.rect(SCREEN, YELLOW, (245, y + line_y, 4, 40))

        # Render Sprites
        all_sprites.draw(SCREEN)

        # Render HUD
        draw_text(f"Score: {score}", font_medium, WHITE, SCREEN, 15, 10)
        draw_text(f"Speed: {speed * 10} km/h", font_medium, WHITE, SCREEN, 220, 10)

        # Render Game Over Screen Overlay
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            SCREEN.blit(overlay, (0, 0))

            draw_text("CRASHED!", font_large, RED, SCREEN, WIDTH // 2 - 95, HEIGHT // 2 - 80)
            draw_text(f"Final Score: {score}", font_medium, WHITE, SCREEN, WIDTH // 2 - 75, HEIGHT // 2 - 20)
            draw_text("Press 'R' to Restart", font_medium, YELLOW, SCREEN, WIDTH // 2 - 105, HEIGHT // 2 + 40)
            draw_text("Press 'Q' to Quit", font_medium, WHITE, SCREEN, WIDTH // 2 - 85, HEIGHT // 2 + 80)

        pygame.display.flip()

# Start Game
if __name__ == "__main__":
    run_game()
