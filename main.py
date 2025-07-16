import sys
import pygame
from settings import SCREEN_DIMENSIONS, FONT_SIZE, WIDTH, HEIGHT
from game_objects import Player, Wall, Hazard, Pellet
import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API.", category=UserWarning)

# Initialize Pygame
pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_DIMENSIONS)
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont(None, FONT_SIZE)  # Create font after Pygame is initialized


def draw_status_bar(screen, player_score, player_health):
    # Render score and health
    score_surface = FONT.render(f"{player_score}", True, "gray")
    health_surface = FONT.render(f"{player_health}", True, "crimson")

    # Calculate total width for positioning
    total_width = score_surface.get_width() + health_surface.get_width() + 40  # Extra space for padding

    # Positioning score and health in the center of the status bar
    score_x = (WIDTH - total_width) // 2
    health_x = score_x + score_surface.get_width() + 20  # 20 pixels of space between them

    # Draw the score and health side by side
    screen.blit(score_surface, (score_x, 10))  # Y position is 10 pixels from the top
    screen.blit(health_surface, (health_x, 10))  # Y position is 10 pixels from the top


# Game objects
walls = [Wall(300, 200, 100, 20), Wall(500, 400, 100, 20)]
hazards = [Hazard(300, 300, 30, 5)]  # Add a hazard at (300, 300) with radius 30 and 5 damage
pellet_size = 10
pellets = [Pellet(0, 0, pellet_size) for _ in range(5)]  # Create pellet instances
for pellet in pellets:
    pellet.spawn(walls, hazards)  # Spawn pellets in valid locations
player = Player()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 1. Player Movement
    # Handle touch events (for mobile)
    if event.type == pygame.FINGERDOWN:
        touch_x, touch_y = event.x * WIDTH, event.y * HEIGHT

        # Calculate dx and dy based on touch position
        dx = player.x_speed if touch_x > player.x else -player.x_speed
        dy = player.y_speed if touch_y > player.y else -player.y_speed

        player.move(dx, dy, walls)

    # Handle mouse click events (for laptop)
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
        # Calculate dx and dy based on mouse position
        dx = player.x_speed if mouse_x > player.x else -player.x_speed
        dy = player.y_speed if mouse_y > player.y else -player.y_speed
        player.move(dx, dy, walls)

    # Handle keyboard events (for laptop)
    keys_pressed = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys_pressed[pygame.K_UP]:
        dy = -player.y_speed
    if keys_pressed[pygame.K_DOWN]:
        dy = player.y_speed
    if keys_pressed[pygame.K_LEFT]:
        dx = -player.x_speed
    if keys_pressed[pygame.K_RIGHT]:
        dx = player.x_speed
    player.move(dx, dy, walls)

    # Check for hazard interaction (reduce health if player touches hazard)
    for hazard in hazards:
        hazard.check_hazard_effect(player)
    # Collision Detection with pellets and updating player score
    for pellet in pellets[:]:
        if player.get_rect().colliderect(pellet.rect):
            player.player_score += 1
            pellet.spawn(walls, hazards)

    # 3. Clear the screen
    SCREEN.fill("Black")

    # 4. Rendering
    player.draw(SCREEN)  # Draw player
    for wall in walls:
        wall.draw(SCREEN)  # Draw walls
    for pellet in pellets:
        pellet.draw(SCREEN)  # Draw pellets
    for hazard in hazards:
        hazard.draw(SCREEN)  # Draw hazards

    # Display player score and health
    draw_status_bar(SCREEN, player.player_score, player.health)

    pygame.display.update()
    CLOCK.tick(60)
