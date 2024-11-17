import pygame
import random
import numpy as np
import matplotlib.pyplot as plt

# Define the grid size and cell size
n = 50
cell_size = 10
width, height = n * cell_size, n * cell_size

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((width, height))

# Define the colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the possible moves
moves = [(0, 1), (1, 0), (-1, 0), (0, -1)]

# Initialize the stack and the set of visited cells
stack = [(0, 0)]
visited = {(0, 0)}

# Create a clock object
clock = pygame.time.Clock()


def draw_grid():
    for X in range(0, width, cell_size):
        for Y in range(0, height, cell_size):
            rect = pygame.Rect(X, Y, cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect, 1)


def draw_cell(X, Y):
    rect = pygame.Rect(X * cell_size, Y * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, RED, rect)


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if stack:
        x, y = stack[-1]
        random.shuffle(moves)

        if (x, y) == (n - 1, n - 1):
            break

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < n and ((nx, ny) not in visited):
                stack.append((nx, ny))
                visited.add((nx, ny))
                break
        else:
            stack.pop()

    screen.fill((0, 0, 0))
    draw_grid()

    for x, y in stack:
        draw_cell(x, y)

    pygame.display.flip()

# Generate the Matplotlib graph
grid = np.zeros((n, n))

for x, y in stack:
    grid[y, x] = 1

plt.imshow(grid, cmap='binary')
plt.show()

while True:
    if input() == "YES":
        pygame.quit()
        break