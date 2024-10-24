import random
import pygame
from settings import *


class Player:
    def __init__(self):
        self.radius = 10  # Define the radius of the player circle
        self.color = "white"
        self.x, self.y = WIDTH // 2, HEIGHT // 2  # Player's center coordinates
        self.x_speed = 3
        self.y_speed = 3
        self.player_score = 0
        self.health = 100  # Add health attribute

    def move(self, dx, dy, walls):
        # Move along the x-axis and check for collisions
        self.x += dx
        self.x = max(self.radius, min(self.x, WIDTH - self.radius))  # Keep within bounds
        for wall in walls:
            wall.resolve_collision(self, dx, 0)  # Check for x-axis collision only

        # Move along the y-axis and check for collisions
        self.y += dy
        self.y = max(self.radius, min(self.y, HEIGHT - self.radius))  # Keep within bounds
        for wall in walls:
            wall.resolve_collision(self, 0, dy)  # Check for y-axis collision only

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def get_rect(self):
        # Return a rect for collision detection based on the circle's bounding box
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


# Circle-rectangle collision helper
def circle_rect_collision(circle_x, circle_y, circle_radius, rect):
    # Find the closest point on the rectangle to the center of the circle
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))

    # Calculate the distance between the circle's center and this closest point
    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y

    # If the distance is less than the circle's radius, there is a collision
    distance_squared = distance_x ** 2 + distance_y ** 2
    return distance_squared < circle_radius ** 2


class Hazard:
    def __init__(self, x, y, radius, damage):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = "red"
        self.damage = damage
        self.has_damaged = False  # Track if damage was applied on this entry

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def check_hazard_effect(self, player):
        # Calculate the distance between the player and the hazard center
        distance = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
        if distance < self.radius + player.radius:  # If the player is within the hazard
            if not self.has_damaged:
                player.health -= self.damage  # Reduce player health by hazard's damage
                self.has_damaged = True  # Mark that damage has been applied
                print(f"Player health reduced! Current health: {player.health}")
        else:
            # If the player leaves the hazard, reset the damage tracker
            self.has_damaged = False


class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, "beige", self.rect)

    def check_collision(self, player):
        return circle_rect_collision(player.x, player.y, player.radius, self.rect)

    def resolve_collision(self, player, dx, dy):
        if self.check_collision(player):
            if dx > 0:  # Moving right
                player.x = self.rect.left - player.radius
            if dx < 0:  # Moving left
                player.x = self.rect.right + player.radius
            if dy > 0:  # Moving down
                player.y = self.rect.top - player.radius
            if dy < 0:  # Moving up
                player.y = self.rect.bottom + player.radius


class Pellet:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)  # Pellet is represented as a rectangle
        self.color = "green"
        self.size = size

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_collision(self, walls, hazards):
        # Check collision with walls
        if any(self.rect.colliderect(wall.rect) for wall in walls):
            return True

        # Check collision with hazards
        if any(self.rect.colliderect(pygame.Rect(hazard.x - hazard.radius, hazard.y - hazard.radius,
                                                 hazard.radius * 2, hazard.radius * 2)) for hazard in hazards):
            return True

        return False

    def spawn(self, walls, hazards):
        while True:
            x = random.randint(0, WIDTH - self.size)
            y = random.randint(0, HEIGHT - self.size)
            self.rect.topleft = (x, y)  # Update the position of the pellet

            if not self.check_collision(walls, hazards):
                print(f"Pellet spawned at: {self.rect.topleft}")  # Debug: Show where pellet is spawned
                return
            else:
                print("Collision detected, retrying...")  # Debug: Show if there was a collision

