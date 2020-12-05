import pygame
import pygame.locals
import os.path
import math

class SpriteManager():
    """ A utility class for this file that loads a tileset from the harddrive """

    def __init__(self):
        """ Initializes this class """
        self.tileset = self._load_tile_table("tileset.png", 16, 16, 2, False)

    def get_main_sprites(self):
        """ Returns a dictionary of mappings from labels to sprites """
        return {
            "floor": self.tileset[1][1],
            "chest.closed": self.tileset[4][5],
            "chest.opened": self.tileset[5][5],
            "player.anim.1": self.tileset[5][10],
            "player.anim.2": self.tileset[5][11],
            "player.anim.3": self.tileset[5][12],
            "player.anim.4": self.tileset[5][13],
            "player.dead": self.tileset[3][11],
            "empty": self.tileset[1][8],
            "stone": self.tileset[2][5]
        }

    def _load_tile_table(self, filename, width, height, scaling=1, flat_list=False):
        """ Loads a tilesheet and splits it into individual tiles

        ADAPTED FROM: http://sheep.art.pl/Tiled%20Map%20in%20PyGame
        
        Args:
            filename (str): The name of the file to load
            width (int): The desired width of each tile
            height (int): The desired height of each tile
            scaling (int): The amount to scale the images by (default 1)
            flat_list (bool): Whether to return a list or a 2D list (default False)
        """
        image = pygame.image.load(os.path.join(os.path.dirname(__file__), filename)).convert_alpha()
        image_width, image_height = image.get_size()

        tile_table = []

        for tile_x in range(0, int(image_width / width)):
            line = [] if not flat_list else tile_table

            if not flat_list:
                tile_table.append(line)

            for tile_y in range(0, int(image_height / height)):
                rect = (tile_x * width, tile_y * height, width, height)
                line.append(pygame.transform.scale(image.subsurface(rect), (scaling * width, scaling * height)))

        return tile_table

class MapTile(pygame.sprite.Sprite):
    """ A basic, static, map tile. Inherits from Sprite """
    def __init__(self, image, x, y):
        """ Initializes this class
        
        Args:
            image (Surface): The image for this tile
            x (int): The x position of this tile
            y (int): The y position of this tile
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PgPlayer(pygame.sprite.Sprite):
    """ A sprite to represent the player. Inherits from Sprite """
    def __init__(self, player):
        """ Initializes this class

        Args:
            player (Player): The player object this sprite is representing
        """
        super().__init__()
        sprites = SpriteManager().get_main_sprites()

        self.player = player

        self.img_idx = 0
        self.images = [sprites[f"player.anim.{x}"] for x in range(1, 5)]
        self.image = self.images[self.img_idx]

        self.rect = self.image.get_rect()
        self.rect.x = self.player.pos[0] * 16 * 4 + 16
        self.rect.y = self.player.pos[1] * 16 * 4 + 16
    
    def update(self):
        """ Generic sprite update function. Moves and animates """
        self.img_idx += 0.1 if self.img_idx < 3 else -3
        self.image = self.images[math.floor(self.img_idx)]

        self.rect.x = self.player.pos[0] * 16 * 4 + 16
        self.rect.y = self.player.pos[1] * 16 * 4 + 16

class Chest(pygame.sprite.Sprite):
    """ A sprite to represent game items. Inherits from Sprite """
    def __init__(self, images, x, y, map_x, map_y):
        """ Initializes this class

        Args:
            image (Surface): The image for this sprite
            x (int): The x position of this sprite
            y (int): The y position of this sprite
            map_x (int): The x index of this sprite on the map
            map_y (int): The y index of this sprite on the map
        """
        super().__init__()
        self.pos = (map_x, map_y)

        self.images = images
        self.image = images[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, current_map):
        """ Generic sprite update function. Changes image depending on state
        
        Args:
            current_map (list): The current map state
        """
        if current_map[self.pos[0]][self.pos[1]] != "I":
            self.image = self.images[1]
        else:
            self.image = self.images[0]


class Finish(pygame.sprite.Sprite):
    """ A sprite to represent the end flag. Inherits from Sprite """
    def __init__(self, current_map):
        """ Initializes this class

        Args:
            current_map (list): The current map state
        """
        super().__init__()
        self.image = SpriteManager().get_main_sprites()["player.dead"]

        self.rect = self.image.get_rect()

        for y in range(len(current_map[0])):
            for x in range(len(current_map)):
                if current_map[x][y] == "E":
                    self.rect.x = x*16*4 + 16
                    self.rect.y = y*16*4 + 16

class ChestBuilder():
    """ Builds and returns a sprite group with the map chests """
    @classmethod
    def build(self, current_map):
        """ Returns a Group of sprites containing all the map items """
        sprites = SpriteManager().get_main_sprites()
        chests = pygame.sprite.Group()

        for y in range(len(current_map[0])):
            for x in range(len(current_map)):
                if current_map[x][y] == "I":
                    chests.add(Chest([sprites["chest.closed"], sprites["chest.opened"]], x*16*4 + 16, y*16*4 + 16, x, y))
        
        return chests

class MapBuilder():
    """ Builds and returns a sprite group with the map tiles """
    @classmethod
    def build(self, current_map):
        """ Returns a Group of sprites containing all the map tiles """
        map_tiles = pygame.sprite.Group()

        character_mapping = {
            "#": "stone",
            "P": "floor", 
            "I": "floor", 
            "-": "floor", 
            "E": "floor"
        }

        sprite_manager = SpriteManager()

        for y in range(len(current_map[0])):
            for x in range(len(current_map)):
                image = sprite_manager.get_main_sprites()[character_mapping[current_map[x][y]]]
                map_tiles.add(MapTile(image, x*16*4, y*16*4))
                map_tiles.add(MapTile(image, x*16*4 + 16*2, y*16*4))
                map_tiles.add(MapTile(image, x*16*4, y*16*4 + 16*2))
                map_tiles.add(MapTile(image, x*16*4 + 16*2, y*16*4 + 16*2))
        
        return map_tiles