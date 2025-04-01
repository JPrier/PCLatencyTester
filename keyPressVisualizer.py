import pygame
import sys

# Initialize Pygame
pygame.init()

# Create a resizable window
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Latency Test Screen")
clock = pygame.time.Clock()

# Start with a black background
current_color = (0, 0, 0)
screen.fill(current_color)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Toggle the screen color on any keypress.
        elif event.type == pygame.KEYDOWN:
            current_color = (255, 255, 255) if current_color == (0, 0, 0) else (0, 0, 0)
            screen.fill(current_color)
            pygame.display.flip()
    clock.tick(240)  # Run the loop at a high tick rate for minimal added latency.

