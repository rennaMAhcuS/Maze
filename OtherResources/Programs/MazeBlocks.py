import random
import heapq


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

ExampleMaze = Maze(10, 10)
ExampleMaze.print_maze()
print(ExampleMaze.solve_maze_a_star())
