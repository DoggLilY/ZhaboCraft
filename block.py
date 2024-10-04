import pygame
import random
import math


class center:
    def __init__(self, name: str, durability: int, actionate: bool):
        self.sprite = pygame.transform.scale(pygame.image.load("resoursepacks\\def\\" + name + ".png"), (48, 48))
        self.durability = durability
        self.name = name
        self.actionate = actionate

    def action(self):
        if self.actionate:
            print(self.name + " action")


stone = center("Stone", 10, False)
grass = center("Grass", 0, False)
frog = center("frog_front_g", 0, False)
tree = center("Tree", 0, False)  # Example top layer object
rock = center("Rock", 0, False)  # Example top layer object


class chunk:
    l = {}  # Dictionary that stores all chunks by their positions

    def __init__(self, pos: tuple, base_layer: list, top_layer: list):
        self.pos = pos
        self.base_layer = base_layer  # First layer (terrain)
        self.top_layer = top_layer  # Second layer (objects on top of terrain)
        chunk.l[self.pos] = (self.base_layer, self.top_layer)  # Add chunk to global dictionary

    @staticmethod
    def generate(pos: tuple):
        # Create two layers: one for the base and one for the top
        base_layer = [[None for _ in range(13)] for _ in range(13)]
        top_layer = [[None for _ in range(13)] for _ in range(13)]

        for y in range(13):
            for x in range(13):
                # Base layer: terrain (grass, stone)
                base_layer[y][x] = random.choice([grass, stone])

                # Top layer: decorative objects (random chance for tree, rock, or nothing)
                if random.random() < 0.2:  # 20% chance of placing a tree or rock
                    top_layer[y][x] = random.choice([tree, rock, None])

        chunk(pos, base_layer, top_layer)

    @staticmethod
    def drawchunkson(win, w, h, player_x, player_y):
        # Calculate the current chunk coordinates and player's offset within the chunk
        chunk_x = math.floor(player_x / 13)
        chunk_y = math.floor(player_y / 13)

        # Generate chunks if they don't exist
        for y in (-1, 0, 1):
            for x in (-1, 0, 1):
                if (x + chunk_x, y + chunk_y) not in chunk.l:
                    chunk.generate((x + chunk_x, y + chunk_y))

        # Calculate player offset inside the chunk (modulo by 13, multiplied by block size 48)
        offset_x = (player_x % 13) * 48
        offset_y = (player_y % 13) * 48

        # Get blocks from the current and neighboring chunks (3x3 grid of chunks)
        base_blocks, top_blocks = chunk.calcuchunks(player_x, player_y)

        # Starting coordinates for drawing (center of the screen minus the player's offset)
        x_start = w // 2 - 6.5 * 48 - offset_x
        y_start = h // 2 - 6.5 * 48 - offset_y

        # Draw base layer (terrain)
        for i, row in enumerate(base_blocks):
            for j, block in enumerate(row):
                if block is not None:
                    win.blit(block.sprite, (x_start + i * 48, y_start + j * 48))

        # Draw top layer (objects) on top of the base layer
        for i, row in enumerate(top_blocks):
            for j, block in enumerate(row):
                if block is not None:
                    win.blit(block.sprite, (x_start + i * 48, y_start + j * 48))

    @staticmethod
    def calcuchunks(player_x, player_y):
        # Calculate the player's current chunk coordinates
        chunk_x = math.floor(player_x / 13)
        chunk_y = math.floor(player_y / 13)

        # Create empty arrays for storing blocks from 3x3 chunks
        base_blocks = [[None for _ in range(39)] for _ in range(39)]  # Base layer blocks
        top_blocks = [[None for _ in range(39)] for _ in range(39)]  # Top layer blocks

        # Loop through neighboring chunks (-1, 0, 1) relative to the current chunk
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                chunk_pos = (chunk_x + dx, chunk_y + dy)

                # Check if the chunk exists
                if chunk_pos in chunk.l:
                    base_layer, top_layer = chunk.l[chunk_pos]

                    # Copy blocks from the base layer
                    for i in range(13):
                        for j in range(13):
                            base_blocks[i + (dx + 1) * 13][j + (dy + 1) * 13] = base_layer[i][j]

                    # Copy blocks from the top layer
                    for i in range(13):
                        for j in range(13):
                            top_blocks[i + (dx + 1) * 13][j + (dy + 1) * 13] = top_layer[i][j]

        return base_blocks, top_blocks
