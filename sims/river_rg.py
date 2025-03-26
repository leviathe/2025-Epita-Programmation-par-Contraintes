from noise import pnoise2
from sims.utils import Tile
import random

TRESH = 0.97
SCALE = 50

def generate_river(grid : list[list[int]], grid_width : int, grid_height : int) -> list[list[int]]:
    seed = random.randint(0, 1000)

    # Génération du bruit Perlin et transformation en ridge noise
    for i in range(grid_height):
        for j in range(grid_width):
            # Génération du bruit Perlin
            noise_value = pnoise2(i / SCALE, j / SCALE, octaves=2, persistence=0.5, lacunarity=2.0, base=seed)
            # Application du ridge noise (inverser la valeur absolue)
            ridge = 1 - abs(noise_value)

            if ridge > TRESH and grid[i][j] == Tile.NONE:
                grid[i][j] = Tile.WATER
    
    return grid
