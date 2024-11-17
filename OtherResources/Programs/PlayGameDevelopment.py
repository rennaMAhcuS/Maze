from random import choice
import pygame
import heapq


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}

    def check_neighbors(self, grid):
        neighbors = []
        if self.y - 1 >= 0 and not grid[self.y - 1][self.x].visited:
            neighbors.append(grid[self.y - 1][self.x])
        if self.x + 1 < len(grid[0]) and not grid[self.y][self.x + 1].visited:
            neighbors.append(grid[self.y][self.x + 1])
        if self.y + 1 < len(grid) and not grid[self.y + 1][self.x].visited:
            neighbors.append(grid[self.y + 1][self.x])
        if self.x - 1 >= 0 and not grid[self.y][self.x - 1].visited:
            neighbors.append(grid[self.y][self.x - 1])
        return neighbors if neighbors else None


def remove_walls(Current, Next):
    dx = Next.x - Current.x
    dy = Next.y - Current.y
    if dx == 1 and dy == 0:
        Current.walls['right'] = False
        Next.walls['left'] = False
    elif dx == -1 and dy == 0:
        Current.walls['left'] = False
        Next.walls['right'] = False
    elif dx == 0 and dy == 1:
        Current.walls['bottom'] = False
        Next.walls['top'] = False
    elif dx == 0 and dy == -1:
        Current.walls['top'] = False
        Next.walls['bottom'] = False


def heuristic(current, goal):
    # Manhattan distance
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(x, y) for x in range(cols)] for y in range(rows)]
        self.stack = []
        self.current_cell = choice(choice(self.grid))
        self.solution = []
        self.solution_path = ""
        self.maze()

    # Maze Generation using Recursive BackTracking
    def generate_maze(self):
        self.current_cell.visited = True
        while True:
            next_cell_possibilities = self.current_cell.check_neighbors(self.grid)
            if next_cell_possibilities:
                self.stack.append(self.current_cell)
                next_cell = choice(next_cell_possibilities)
                remove_walls(self.current_cell, next_cell)
                self.current_cell = next_cell
                self.current_cell.visited = True
            elif self.stack:
                self.current_cell = self.stack.pop()
            else:
                break

    def solve_maze(self):
        self.solution = [[False for _ in range(self.cols)] for _ in range(self.rows)]  # Initialize the solution matrix
        self.solve_maze_a_star()

    def solve_maze_a_star(self):
        start = (0, 0)
        goal = (self.cols - 1, self.rows - 1)

        # The priority queue
        open_set = []
        heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))  # (f, g, position)

        # Costs from start to a node
        g_score = {start: 0}

        # For path reconstruction
        came_from = {}

        while open_set:
            _, g, current = heapq.heappop(open_set)

            if current == goal:
                self.ReconstructPath_SolutionGrid(came_from, current)
                self.ReconstructPath_PathString(came_from, current)
                return True

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g + 1  # Assuming cost from one cell to another is always 1

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, tentative_g_score, neighbor))

        return False

    def get_neighbors(self, position):
        x, y = position
        neighbors = []
        if not self.grid[y][x].walls['right']:
            neighbors.append((x + 1, y))
        if not self.grid[y][x].walls['left']:
            neighbors.append((x - 1, y))
        if not self.grid[y][x].walls['top']:
            neighbors.append((x, y - 1))
        if not self.grid[y][x].walls['bottom']:
            neighbors.append((x, y + 1))
        return neighbors

    def ReconstructPath_PathString(self, came_from, current):
        path = []
        while current in came_from:
            next_current = came_from[current]
            dx = current[0] - next_current[0]
            dy = current[1] - next_current[1]
            if dx == 1:
                path.append('L')
            elif dx == -1:
                path.append('R')
            elif dy == 1:
                path.append('D')
            elif dy == -1:
                path.append('U')
            current = next_current
        path.reverse()  # Reverse the path to start from the beginning
        self.solution_path = ''.join(path)  # Save the path as a string

    def ReconstructPath_SolutionGrid(self, came_from, current):
        while current in came_from:
            x, y = current
            self.solution[y][x] = True
            current = came_from[current]
        self.solution[0][0] = True  # Mark the start as part of the solution

    def maze(self):
        self.generate_maze()
        self.solve_maze()

    def draw_maze(self, Screen):
        cell_width = Screen.get_width() // self.cols
        cell_height = Screen.get_height() // self.rows

        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.grid[y][x]
                rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)

                if cell.visited:
                    pygame.draw.rect(Screen, (255, 255, 255), rect)  # White for visited cells

                if cell.walls['top']:
                    pygame.draw.line(Screen, (0, 0, 0), rect.topleft, rect.topright)  # Black for walls
                if cell.walls['right']:
                    pygame.draw.line(Screen, (0, 0, 0), rect.topright, rect.bottomright)
                if cell.walls['bottom']:
                    pygame.draw.line(Screen, (0, 0, 0), rect.bottomright, rect.bottomleft)
                if cell.walls['left']:
                    pygame.draw.line(Screen, (0, 0, 0), rect.bottomleft, rect.topleft)

    def Draw_SolvedMaze(self, Screen):
        cell_width = Screen.get_width() // self.cols
        cell_height = Screen.get_height() // self.rows

        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.grid[y][x]
                rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)

                if self.solution[y][x]:  # Check if the cell is part of the solution path
                    pygame.draw.rect(Screen, (0, 255, 0), rect)  # Draw solution path cells in green
                elif cell.visited:
                    pygame.draw.rect(Screen, (255, 255, 255), rect)  # White for visited cells

                if cell.walls['top']:
                    pygame.draw.line(Screen, (0, 0, 0), rect.topleft, rect.topright)  # Black for walls
                if cell.walls['right']:
                    pygame.draw.line(Screen, (0, 0, 0), rect.topright, rect.bottomright)
                if cell.walls['bottom']:
                    pygame.draw.line(Screen, (0, 0, 0), rect.bottomright, rect.bottomleft)
                if cell.walls['left']:
                    pygame.draw.line(Screen, (0, 0, 0), rect.bottomleft, rect.topleft)


# Player's Class
class Player:
    def __init__(self, Screen: pygame.Surface, image_path):
        self.screen = Screen
        self.image = {
            'up': [(pygame.image.load(f"{image_path}/up/{i}.png").convert_alpha()) for i in range(13, 17)],
            'down': [pygame.image.load(f"{image_path}/down/{i}.png").convert_alpha() for i in range(1, 5)],
            'left': [pygame.image.load(f"{image_path}/left/{i}.png").convert_alpha() for i in range(5, 9)],
            'right': [pygame.image.load(f"{image_path}/right/{i}.png").convert_alpha() for i in range(9, 13)]
        }
        self.direction = 'down'
        self.is_pressed = False

    def animate(self, keys, TimePassed, PlayerWidth, Position):
        if keys[pygame.K_UP]:
            self.direction = 'up'
            self.is_pressed = True
        elif keys[pygame.K_DOWN]:
            self.direction = 'down'
            self.is_pressed = True
        elif keys[pygame.K_LEFT]:
            self.direction = 'left'
            self.is_pressed = True
        elif keys[pygame.K_RIGHT]:
            self.direction = 'right'
            self.is_pressed = True
        else:
            self.is_pressed = False
        rect = [pygame.transform.scale(self.image[self.direction][i], (int(PlayerWidth * 9 / 10), int(PlayerWidth * 9 / 10))).get_rect(center=Position) for i in range(4)]
        if self.is_pressed:
            frame_index = int((int(TimePassed) % 400) / 100)
            self.screen.blit(self.image[self.direction][frame_index], rect[frame_index])
        else:
            self.screen.blit(self.image[self.direction][0], rect[0])


# GamePlay
class GamePlay:
    def __init__(self, screen: pygame.Surface, PlayerName: str, PlayerImagesPath: str, MazeImagesPath: str, MazeCellVisibility: int = 10):
        self.screen = screen
        self.PlayerName = PlayerName
        self.Player = Player(self.screen, PlayerImagesPath)

        self.is_active = False

        self.LevelScreen = True
        self.GameScreen = False
        self.GameOverScreen = False

        self.Level = 0
        self.MazeGame = None
        self.GameStatus = 0  # 0 = Playing, 1 = Won, -1 = Lost

        self.PlayerCellCoordinates = (0, 0)
        self.MazeVisibility = MazeCellVisibility
        self.MazeImagesPath = MazeImagesPath
        self.ShiftX = int(self.screen.get_width() / 100)
        self.CellWidth = int(self.screen.get_height() / self.MazeVisibility)

    # To be called only once.
    def SetMazeLevel(self):
        if self.MazeGame is None:
            if self.Level == 1:
                self.MazeGame = Maze(20, 20)
            elif self.Level == 2:
                self.MazeGame = Maze(30, 30)
            elif self.Level == 3:
                self.MazeGame = Maze(40, 40)
            self.PlayerCellCoordinates = (0, 0)

    def PlayerCellCoordinatesMover(self, keys):
        isActive = False
        TrialNewCoordinates = ()
        if keys[pygame.K_UP]:
            TrialNewCoordinates = (self.PlayerCellCoordinates[0], self.PlayerCellCoordinates[1] - 1)
            isActive = True
        elif keys[pygame.K_DOWN]:
            TrialNewCoordinates = (self.PlayerCellCoordinates[0], self.PlayerCellCoordinates[1] + 1)
            isActive = True
        elif keys[pygame.K_LEFT]:
            TrialNewCoordinates = (self.PlayerCellCoordinates[0] - 1, self.PlayerCellCoordinates[1])
            isActive = True
        elif keys[pygame.K_RIGHT]:
            TrialNewCoordinates = (self.PlayerCellCoordinates[0] + 1, self.PlayerCellCoordinates[1])
            isActive = True

        if isActive:
            if not self.MazeGame.check_walls(self.PlayerCellCoordinates, TrialNewCoordinates):
                self.PlayerCellCoordinates = TrialNewCoordinates

