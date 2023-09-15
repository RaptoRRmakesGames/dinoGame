import pygame, pickle
pygame.init()

class World:
    
    def __init__(self, tile_size_x =16, tile_size_y = 16):
        
        self.tiles = {}
        
        self.tile_size_x = tile_size_x
        self.tile_size_y = tile_size_y
        
        self.tile_imgs = self.load_tile_images()
        
    def load(self, filename):
        
        with open(f'assets/worlds/{filename}', 'rb') as f:
            
            self.tiles = pickle.load(f)
        
    def load_tile_images(self):

        tileset = pygame.image.load('assets/images/tileset/tiles.png').convert()
        
        iter = tileset.get_width() // self.tile_size_x
        
        surfs = []
        
        for i in range(iter):
            
            surf = tileset.subsurface(pygame.Rect(i * self.tile_size_x, 0, self.tile_size_x, self.tile_size_y))
            
            surf.convert_alpha()
            
            surfs.append(surf)
            
        return surfs 
        
    def add_tile(self, tile_pos , tile_tuple):
        
        self.tiles[tile_pos]= tile_tuple
        
    def draw_world(self):
        
        world_surface = pygame.Surface((2400,2400)).convert_alpha()
        
        for tile in self.tiles:
            
            tile_tuple = self.tiles[tile]
            
            tile_cord_x, tile_cord_y = int(tile.split(':')[0]),int(tile.split(':')[1])
            
            cord_x, cord_y = tile_cord_x * self.tile_size_x, tile_cord_y * self.tile_size_y
            
            tile_surf = self.tile_imgs[tile_tuple[0]]
            
            world_surface.blit(tile_surf, (cord_x, cord_y))
            
        world_surface.set_colorkey((0,0,0))
            
        return world_surface
            
            
        

        
        
        