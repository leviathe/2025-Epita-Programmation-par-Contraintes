import random

from sims.utils import Tile
import sims.generator as generator

def generate_labyrinth_roads(grid_width : int, grid_height : int) -> list[list[int]]: 
    grid = [[Tile.NONE for _ in range(grid_width)] for _ in range(grid_height)]

    start_x, start_y = 1, 1
    grid[start_y][start_x] = Tile.ROAD
    walls = [(start_x + dx, start_y + dy) for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]]
    
    while walls:
        wx, wy = random.choice(walls)
        walls.remove((wx, wy))

        if 0 < wx < grid_width-1 and 0 < wy < grid_height-1:
            neighbors = []
            if wx >= 2 and grid[wy][wx - 2] == Tile.ROAD:
                neighbors.append((wx - 2, wy))
            if wx < grid_width - 2 and grid[wy][wx + 2] == Tile.ROAD:
                neighbors.append((wx + 2, wy))
            if wy >= 2 and grid[wy - 2][wx] == Tile.ROAD:
                neighbors.append((wx, wy - 2))
            if wy < grid_width - 2 and grid[wy + 2][wx] == Tile.ROAD:
                neighbors.append((wx, wy + 2))

            if len(neighbors) == 1:
                nx, ny = neighbors[0]
                grid[wy][wx] = Tile.ROAD
                grid[(wy + ny)//2][(wx + nx)//2] = Tile.ROAD

                for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                    new_wx, new_wy = wx + dx, wy + dy
                    if 0 <= new_wx < grid_width and 0 <= new_wy < grid_height:
                        if grid[new_wy][new_wx] == Tile.NONE:
                            walls.append((new_wx, new_wy))
    return grid

generator.register_road_generation_func('Labyrinth', generate_labyrinth_roads)