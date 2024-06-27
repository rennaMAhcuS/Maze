### 1. Initialize the Open and Closed Sets

- **Open Set**: This contains nodes discovered but not yet evaluated. You start by putting the start node in this set.
- **Closed Set**: This is initially empty and will contain already evaluated nodes.

### 2. Define the Cost Scores

For each node, you need to keep track of:

- `g(n)`: The path's cost from the start node to `n`.
- `h(n)`: The heuristic estimate of the cost from `n` to the goal. A common heuristic for grid-based paths is the Manhattan distance.
- `f(n) = g(n) + h(n)`: The total estimated cost of the cheapest path going through `n`.

### 3. Loop Until the Open Set is Empty

The algorithm continues evaluating nodes in the open set until it becomes empty. If the open set is empty, the algorithm fails.

### 4. Select the Node with the Lowest `f(n)` from the Open Set

This node is considered for exploration. Let's call this node `current`.

### 5. Check if the Goal is Reached

Once the algorithm reaches the goal (`current`), it reconstructs the path by tracing back from the goal node to the start node using a `came_from` map.

### 6. Move `current` from the Open Set to the Closed Set

This marks `current` as evaluated.

### 7. For Each Neighbor of `current`

For each neighbor of `current`, do the following:

- If the neighbor is in the closed set, ignore it because it has already been evaluated.
- Calculate `tentative_g_score = g(current) + dist_between(current, neighbor)`, where `dist_between` is the distance from `current` to the neighbor (often `1` in a grid).
- If the neighbor is not in the open set, add it. This means it's a newly discovered node.
- If `tentative_g_score` is lower than `g(neighbor)`, this path to the neighbor is better than any previous one. Record it. Set `came_from[neighbor] = current` and update `g(neighbor)` and `f(neighbor)`.

### 8. Repeat

Go back to step 4 and repeat the process until the goal is reached or the open set is empty.

### Path Reconstruction

Once the goal is reached, you can reconstruct the path by tracing back from the goal node to the start node using the `came_from` map. This gives you the sequence of nodes that constitutes the shortest path found by A*.

### Efficiency and Optimality

A* is efficient because the heuristic guides the search towards the goal, reducing the number of nodes explored. It's optimal (guarantees the shortest path) if the heuristic is admissible, meaning it never overestimates the actual cost to get to the nearest goal node.

This step-by-step guide outlines the core logic of A*. Implementations can vary, especially in how neighbors are determined and how various sets and scores are managed, but the fundamental principles remain the same.
