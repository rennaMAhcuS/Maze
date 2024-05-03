import random
import heapq
import time
from sys import setrecursionlimit

import pygame

setrecursionlimit(100000)  # To ensure that generate_maze_main function doesn't give an error


# For solving A*
def heuristic(x, y):
    # Manhattan distance
    return abs(x - 1) + abs(y - 1)


class Maze:
    def __init__(self, Width, Height):
        self.width = Width
        self.height = Height
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.generate_maze()

    def carve_maze(self, x, y, maze):
        ValidDirections = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(ValidDirections)
        for dx, dy in ValidDirections:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < self.width and 0 <= ny < self.height and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[ny - dy][nx - dx] = 0
                self.carve_maze(nx, ny, maze)

    def generate_maze_main(self):
        self.maze[1][1] = 0
        self.carve_maze(1, 1, self.maze)

    def generate_maze(self):
        self.generate_maze_main()
        for i in self.maze:
            i += [1]
        self.maze += [[1] * (self.width + 1)]

    def print_maze(self, is_raw: bool = False):
        if not is_raw:
            for row in self.maze:
                print("".join("X " if cell else "  " for cell in row))
        else:
            for row in self.maze:
                print(row)

    def solve_maze_dfs(self, X: int = -1, Y: int = -1, path: str = ""):
        if X == -1:
            x = self.width - 1
        else:
            x = X
        if Y == -1:
            y = self.height - 1
        else:
            y = Y
        if x == 1 and y == 1:  # Found the exit
            return path

        # Mark as visited
        self.maze[y][x] = 2
        for dx, dy, Direction in [(0, -1, 'U'), (1, 0, 'L'), (0, 1, 'D'), (-1, 0, 'R')]:  # Directions to move
            nx, ny = x + dx, y + dy
            if self.width > nx >= 0 == self.maze[ny][nx] and 0 <= ny < self.height:
                result = self.solve_maze_dfs(nx, ny, path + Direction)
                if result:  # Path found
                    return result
        # Backtrack
        self.maze[y][x] = 0
        return ""

    def solve_maze_a_star(self):
        start = (self.width - 1, self.height - 1)
        goal = (1, 1)
        frontier = [(0 + heuristic(*start), start)]  # Priority queue
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                Next = (current[0] + dx, current[1] + dy)
                if self.width > Next[0] >= 0 == self.maze[Next[1]][Next[0]] and 0 <= Next[1] < self.height:
                    new_cost = cost_so_far[current] + 1
                    if Next not in cost_so_far or new_cost < cost_so_far[Next]:
                        cost_so_far[Next] = new_cost
                        priority = new_cost + heuristic(*Next)
                        heapq.heappush(frontier, (priority, Next))
                        came_from[Next] = current

        # Reconstruct path
        current = goal
        path = ""
        while current != start:
            prev = came_from[current]
            if prev:
                if current[0] - prev[0] == 1:
                    path = "R" + path
                elif current[0] - prev[0] == -1:
                    path = "L" + path
                elif current[1] - prev[1] == 1:
                    path = "D" + path
                elif current[1] - prev[1] == -1:
                    path = "U" + path
            current = prev

        return path


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

    def animate(self, keys, TimePassed, PlayerWidth, center):
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = 'up'
            self.is_pressed = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = 'down'
            self.is_pressed = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = 'left'
            self.is_pressed = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = 'right'
            self.is_pressed = True
        else:
            self.is_pressed = False
        rect = [pygame.transform.scale(self.image[self.direction][i],
                                       (int(PlayerWidth * 8 / 10), int(PlayerWidth * 8 / 10))).get_rect(center=center)
                for i in range(4)]

        if self.is_pressed:
            frame_index = int((int(TimePassed) % 400) / 100)
            self.screen.blit(pygame.transform.scale(self.image[self.direction][frame_index],
                                                    (int(PlayerWidth * 8 / 10), int(PlayerWidth * 8 / 10))),
                             rect[frame_index])
        else:
            self.screen.blit(pygame.transform.scale(self.image[self.direction][0],
                                                    (int(PlayerWidth * 8 / 10), int(PlayerWidth * 8 / 10))), rect[0])


# GamePlay
class GamePlay:
    def __init__(self, screen: pygame.Surface, PlayerName: str, PlayerImagesPath: str, MazeImagesPath: str,
                 PathAddress: str, GameOverImgAddress: str, MazeCellVisibility: int = 10):
        self.screen = screen
        self.PlayerName = PlayerName
        self.Player = Player(self.screen, PlayerImagesPath)

        self.is_active = False
        self.StopwatchValue = 0

        self.LevelScreen = True
        self.GameScreen = False
        self.GameOverScreen = False

        self.Level = 0
        self.MazeGame = None
        self.GameStartTime = 0
        self.pathAddress = PathAddress

        self.PlayerCellCoordinates = (1, 1)
        self.XShift = self.screen.get_width() / 10
        self.BackgroundType = 0
        self.TotalBackgroundTypes = 5
        self.MazeVisibility = MazeCellVisibility
        self.MazeImagesPath = MazeImagesPath
        self.CellWidth = int(self.screen.get_height() / self.MazeVisibility)
        self.MainCellCoordinates = ((self.XShift + self.screen.get_height()) / 2, self.screen.get_height() / 2)
        GO_Image = pygame.image.load(GameOverImgAddress)
        self.GameOverImage = pygame.transform.scale(GO_Image, (GO_Image.get_width() / 2, GO_Image.get_height() / 2)).convert_alpha()

    # To be called only once.
    def SetMazeLevel(self):
        if self.MazeGame is None:
            if self.Level == 1:
                self.MazeGame = Maze(20, 20)
            elif self.Level == 2:
                self.MazeGame = Maze(30, 30)
            elif self.Level == 3:
                self.MazeGame = Maze(40, 40)
            self.PlayerCellCoordinates = (self.MazeGame.width - 1, self.MazeGame.height - 1)
            self.GameStartTime = pygame.time.get_ticks()
        # print(self.MazeGame.solve_maze_a_star())
        with open(self.pathAddress, 'w') as file:
            file.write(self.MazeGame.solve_maze_a_star())

    def GamePlay(self, keys, TimePassed):

        self.DisplayMazeBackground()
        self.Player.animate(keys, TimePassed, self.CellWidth, self.MainCellCoordinates)
        self.PlayerCellCoordinatesMover(keys)

        # Timer
        self.StopwatchValue = pygame.time.get_ticks() - self.GameStartTime

        # GameOver
        self.GameOver()

    def DisplayMazeBackground(self):
        for x in range(-(self.MazeVisibility + 1), self.MazeGame.width + 1 + (self.MazeVisibility + 1)):
            for y in range(-(self.MazeVisibility + 1), self.MazeGame.height + 1 + (self.MazeVisibility + 1)):
                self.DisplayCell(x, y)

    def DisplayCell(self, x, y):
        Dest = (self.MainCellCoordinates[0] + (x - self.PlayerCellCoordinates[0]) * self.CellWidth,
                self.MainCellCoordinates[1] + (y - self.PlayerCellCoordinates[1]) * self.CellWidth)

        if abs(y - self.PlayerCellCoordinates[1]) <= (self.MazeVisibility / 2) + 1 and abs(
                x - self.PlayerCellCoordinates[0]) <= (
                (int(self.MazeVisibility * self.screen.get_width() / self.screen.get_height())) / 2) + 1:
            if 0 <= x < self.MazeGame.width and 0 <= y < self.MazeGame.height:
                path_image = pygame.transform.scale(
                    pygame.image.load(f"{self.MazeImagesPath}/{self.BackgroundType}/Path.png"),
                    (self.CellWidth, self.CellWidth)).convert_alpha()
                wall_image = pygame.transform.scale(
                    pygame.image.load(f"{self.MazeImagesPath}/{self.BackgroundType}/Wall.png"),
                    (self.CellWidth, self.CellWidth)).convert_alpha()

                if self.MazeGame.maze[y][x] == 0:
                    self.screen.blit(path_image, path_image.get_rect(center=Dest))
                else:
                    self.screen.blit(wall_image, wall_image.get_rect(center=Dest))
            else:
                wall_image = pygame.transform.scale(
                    pygame.image.load(f"{self.MazeImagesPath}/{self.BackgroundType}/Wall.png"),
                    (self.CellWidth, self.CellWidth)).convert_alpha()

                self.screen.blit(wall_image, wall_image.get_rect(center=Dest))

            if (x, y) == (1, 1):
                home_image = pygame.transform.scale(pygame.image.load(f"{self.MazeImagesPath}/Home.png"),
                                                    (self.CellWidth, self.CellWidth)).convert_alpha()
                self.screen.blit(home_image, home_image.get_rect(center=Dest))
            elif (x, y) == (self.MazeGame.width - 1, self.MazeGame.height - 1):
                start_image = pygame.transform.scale(pygame.image.load(f"{self.MazeImagesPath}/Start.png"),
                                                     (self.CellWidth, self.CellWidth)).convert_alpha()
                self.screen.blit(start_image, start_image.get_rect(center=Dest))

    def PlayerCellCoordinatesMover(self, keys):
        isActive = False
        TrialNewCoordinates = ()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            TrialNewCoordinates = (self.PlayerCellCoordinates[0], self.PlayerCellCoordinates[1] - 1)
            isActive = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            TrialNewCoordinates = (self.PlayerCellCoordinates[0], self.PlayerCellCoordinates[1] + 1)
            isActive = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            TrialNewCoordinates = (self.PlayerCellCoordinates[0] - 1, self.PlayerCellCoordinates[1])
            isActive = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            TrialNewCoordinates = (self.PlayerCellCoordinates[0] + 1, self.PlayerCellCoordinates[1])
            isActive = True

        if isActive:
            if 0 <= TrialNewCoordinates[0] < self.MazeGame.width and 0 <= TrialNewCoordinates[1] < self.MazeGame.height:
                if self.MazeGame.maze[TrialNewCoordinates[1]][TrialNewCoordinates[0]] == 0:
                    self.PlayerCellCoordinates = TrialNewCoordinates
                time.sleep(0.05)

    def GameOver(self):
        if self.PlayerCellCoordinates == (1, 1):
            time.sleep(0.5)
            self.GameScreen = False
            self.GameOverScreen = True

    def GameOverScreenDisplay(self):
        # print(self.StopwatchValue)
        self.screen.blit(self.GameOverImage, self.GameOverImage.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 4)))

    def ChangeBackground(self):
        self.BackgroundType = (self.BackgroundType + 1) % self.TotalBackgroundTypes
